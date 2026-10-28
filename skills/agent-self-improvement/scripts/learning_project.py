"""Project-local state migration. Copies only the selected project; never deletes legacy state."""
import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import uuid
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

from learning import legacy_has_project, project_id
from learning_memory import bind, open_store
from learning_processing import connect, lock
from learning_state import check_owner, state_root


def read_config(project):
    config = check_owner(project, state_root(project))
    if config is None:
        raise ValueError("Project state is not initialized")
    return config


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def initialize(project, legacy=None, remote=None, *, local_only=False, memory_id=None, state=None):
    project = Path(project).resolve(strict=True)
    target = state_root(project, state)
    if (target / "project.json").exists():
        return {"result": "already_initialized", "state": str(target), "config": check_owner(project, target)}
    if not legacy and legacy_has_project(project):
        raise ValueError("Legacy project memory exists; provide --legacy explicitly before initialization")
    if target.exists():
        raise ValueError("Partial state exists; inspect before migration")
    local_id = project_id(project)
    target.parent.mkdir(parents=True, exist_ok=True)
    stage = target.parent / (".learning-migrate-" + uuid.uuid4().hex)
    copied = {}
    source = Path(legacy).resolve() if legacy else None
    with lock(target.parent / ".learning-locks", project):
        if target.exists():
            raise ValueError("Project state was initialized concurrently")
        with closing(open_store(stage)) as out:
            pid = None
            if source and (source / "experience.sqlite3").is_file():
                # One read transaction provides a consistent snapshot while capture continues.
                with closing(sqlite3.connect((source / "experience.sqlite3").as_uri() + "?mode=ro", uri=True)) as old:
                    old.execute("BEGIN")
                    tables = {r[0] for r in old.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                    binding = old.execute("SELECT project_id FROM memory_bindings WHERE local_id=?", (local_id,)).fetchone() if "memory_bindings" in tables else None
                    pid = binding[0] if binding else None
                    selections = {"projects": ("id", local_id), "events": ("project_id", local_id),
                        "attachments": ("project_id", local_id), "capture_pauses": ("project_id", local_id),
                        "runs": ("project_id", local_id)}
                    if pid:
                        selections.update({"memory_projects": ("id", pid), "memory_bindings": ("local_id", local_id),
                            "memory_records": ("project_id", pid), "memory_packages": ("project_id", pid)})
                    with out:
                        for table, (key, identity) in selections.items():
                            if table not in tables:
                                continue
                            rows = old.execute(f"SELECT * FROM {table} WHERE {key}=?", (identity,)).fetchall()
                            for row in rows:
                                out.execute(f"INSERT INTO {table} VALUES ({','.join('?' for _ in row)})", row)
                            copied[table] = len(rows)
                        if "event_metadata" in tables:
                            for row in old.execute("SELECT * FROM event_metadata WHERE event_id IN (SELECT id FROM events WHERE project_id=?)", (local_id,)):
                                out.execute("INSERT INTO event_metadata VALUES (?,?,?,?,?,?)", row)
                        digests = [r[0] for r in out.execute("SELECT DISTINCT digest FROM attachments")]
                        for digest in digests:
                            row = old.execute("SELECT * FROM blobs WHERE digest=?", (digest,)).fetchone()
                            if row:
                                out.execute("INSERT INTO blobs VALUES (?,?)", row)
                            blob = source / "blobs" / digest[:2] / digest
                            if not blob.is_file() or hashlib.sha256(blob.read_bytes()).hexdigest() != digest:
                                raise ValueError("Attachment missing or corrupt; legacy store remains unchanged")
                            destination = stage / "blobs" / digest[:2] / digest
                            destination.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(blob, destination)
                    # Journal schema is independent of memory acceptance.
                    with closing(connect(stage)) as journal, journal:
                        if "learning_decisions" in tables:
                            columns = [r[1] for r in old.execute("PRAGMA table_info(learning_decisions)") if r[1] != "sequence"]
                            rows = old.execute("SELECT " + ",".join(columns) + " FROM learning_decisions WHERE project_id=?", (local_id,)).fetchall()
                            for row in rows:
                                values = dict(zip(columns, row))
                                proposal = Path(values["proposal"]) if values["proposal"] else None
                                if proposal and proposal.is_file():
                                    if proposal.parent.resolve() != (source / "proposals").resolve():
                                        raise ValueError("Proposal outside the legacy proposal store")
                                    destination = stage / "proposals" / proposal.name
                                    destination.parent.mkdir(parents=True, exist_ok=True)
                                    shutil.copy2(proposal, destination)
                                    values["proposal"] = str(target / "proposals" / proposal.name)
                                journal.execute("INSERT INTO learning_decisions (" + ",".join(columns) + ") VALUES (" + ",".join("?" for _ in columns) + ")", list(values.values()))
                            copied["learning_decisions"] = len(rows)
                        if "learning_processing" in tables and not copied.get("learning_decisions"):
                            rows = old.execute('SELECT project_id,repo,record_id,record_digest,skill_digest,outcome,proposal,updated_at FROM learning_processing WHERE project_id=?', (local_id,)).fetchall()
                            for row in rows:
                                values = list(row)
                                # Historical review is not proof of application or future behavior.
                                if values[5] == 'reviewed':
                                    values[5] = 'deferred'
                                journal.execute('INSERT INTO learning_decisions (project_id,repo,record_id,record_digest,skill_digest,outcome,proposal,updated_at,reason,recheck_when,details) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                                    values + ['Legacy receipt; inspect original evidence', 'explicit_review', '{"legacy":true}'])
                            copied['legacy_processing_receipts'] = len(rows)
                    old.rollback()
            if pid is None:
                pid = bind(out, project, pid=memory_id, name=project.name)
            if memory_id and memory_id != pid:
                raise ValueError("Explicit project identity conflicts with migrated binding")
            with out:
                out.execute("INSERT OR IGNORE INTO projects VALUES (?,?,0)", (local_id, str(project)))
            if out.execute("PRAGMA integrity_check").fetchone()[0] != "ok" or out.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("Migrated database integrity failed")
        config = {"schema_version": 1, "project_id": pid, "capture_project_id": local_id,
            "project_root": str(project), "snapshot_choice": "unresolved",
            "name": project.name, "remote": remote, "remote_folder": (re.sub(r"[^A-Za-z0-9_.-]+", "-", project.name).strip(".-") or "project") + "--" + pid,
            "auto_sync": False, "telemetry": {"enabled": False, "base_url": "https://cloud.langfuse.com",
            "authorization_env": "LANGFUSE_MCP_AUTHORIZATION", "project_metadata_key": None,
            "project_metadata_value": None, "access_days": 30, "overlap_hours": 48,
            "archive_interval_hours": 24, "max_pages": 100},
            "created_at": datetime.now(UTC).isoformat()}
        if local_only:
            config.update(remote=None, auto_sync=False)
            config['telemetry']['enabled'] = False
        write_json(stage / "project.json", config)
        write_json(stage / "migration.json", {"source": str(source) if source else None,
            "counts": copied, "legacy_preserved": True, "integrity": "ok"})
        (stage / ".gitignore").write_text("*\n", encoding="utf-8")
        for name in ("raw", "runs", "snapshots", "outbox", "archive", "queue"):
            (stage / name).mkdir(exist_ok=True)
        stage.rename(target)
    return {"result": "initialized", "state": str(target), "project_id": pid,
            "counts": copied, "tagging": {"status": "not_requested"}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--state", type=Path)
    parser.add_argument("--legacy")
    parser.add_argument("--remote", help="Legacy address hint only; verify with memory configure before exchange")
    parser.add_argument("--local-only", action="store_true",
                        help="Create local memory without telemetry, remote sync or tracing configuration")
    args = parser.parse_args()
    result = initialize(args.project, args.legacy, args.remote, local_only=args.local_only, state=args.state)
    # Existing configurations may contain private connection details.
    result.pop('config', None)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
