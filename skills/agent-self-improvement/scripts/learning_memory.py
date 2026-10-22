#!/usr/bin/env python3
"""Project-scoped structured experience and explicit, manual GitHub exchange."""
import argparse
import base64
import hashlib
import json
import re
import sqlite3
import subprocess
import sys
import uuid
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

from learning import create_store, default_root, project_id, redact

VERSION = 2
KINDS = {"episode", "evidence", "requirement", "finding", "lesson", "evaluation", "application"}
STATUSES = {"candidate", "verified", "accepted", "disputed", "stale", "superseded"}
FIELDS = {
    "episode": {"task", "expected_result", "initial_state", "constraints", "actions", "feedback", "outcome", "checks", "open_questions", "coverage", "source_event_ids"},
    "evidence": {"source_type", "source_ref", "summary", "availability", "observed_at"},
    "requirement": {"statement", "authority", "applicability", "evidence_ids"},
    "finding": {"observation", "cause", "cause_status", "alternatives", "evidence_ids", "counterevidence_ids"},
    "lesson": {"instruction", "applicability", "exceptions", "finding_ids", "evidence_ids", "scope", "recheck_when", "last_verified_commit"},
    "evaluation": {"lesson_ids", "baseline", "candidate", "scenario", "held_out", "environment", "result", "checks"},
    "application": {"lesson_ids", "task", "outcome", "regressions"},
}
SCHEMA = """
CREATE TABLE IF NOT EXISTS memory_projects (
 id TEXT PRIMARY KEY, name TEXT NOT NULL, source_repository TEXT NOT NULL DEFAULT '',
 sync_repository TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS memory_bindings (
 local_id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES memory_projects(id));
CREATE TABLE IF NOT EXISTS memory_records (
 id TEXT NOT NULL, revision INTEGER NOT NULL CHECK(revision > 0),
 project_id TEXT NOT NULL REFERENCES memory_projects(id),
 episode_id TEXT NOT NULL, kind TEXT NOT NULL CHECK(kind IN
 ('episode','evidence','requirement','finding','lesson','evaluation','application')),
 status TEXT NOT NULL CHECK(status IN
 ('candidate','verified','accepted','disputed','stale','superseded')),
 payload TEXT NOT NULL, provenance TEXT NOT NULL, created_at TEXT NOT NULL,
 digest TEXT NOT NULL, PRIMARY KEY(project_id,id,revision));
CREATE INDEX IF NOT EXISTS memory_scope ON memory_records(project_id,kind,status);
CREATE INDEX IF NOT EXISTS memory_episode ON memory_records(project_id,episode_id);
CREATE TABLE IF NOT EXISTS memory_packages (
 digest TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES memory_projects(id),
 imported_at TEXT NOT NULL);
"""


def now():
    return datetime.now(UTC).isoformat()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,100}", value):
        raise ValueError("Invalid portable identifier")
    return value


def open_store(state):
    state = Path(state)
    database = state / "experience.sqlite3"
    if database.exists():
        with closing(sqlite3.connect(database)) as old:
            version = old.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, VERSION):
                raise ValueError(f"Unsupported database schema {version}")
            if version == 0:
                backup = state / ("experience.pre-v2-" + uuid.uuid4().hex + ".sqlite3")
                with closing(sqlite3.connect(backup)) as target:
                    old.backup(target)
                backup.chmod(0o600)
    conn = create_store(state)
    conn.execute("PRAGMA foreign_keys=ON")
    # One atomic migration; legacy collection tables and IDs remain untouched.
    conn.executescript("BEGIN IMMEDIATE;\n" + SCHEMA + f"\nPRAGMA user_version={VERSION};\nCOMMIT;")
    expected = {
        "memory_projects": {"id", "name", "source_repository", "sync_repository", "created_at"},
        "memory_bindings": {"local_id", "project_id"},
        "memory_records": {"id", "revision", "project_id", "episode_id", "kind", "status", "payload", "provenance", "created_at", "digest"},
        "memory_packages": {"digest", "project_id", "imported_at"},
    }
    with closing(sqlite3.connect(":memory:")) as reference:
        reference.executescript(SCHEMA)
        for table, fields in expected.items():
            actual = conn.execute(f"PRAGMA table_info({table})").fetchall()
            desired = reference.execute(f"PRAGMA table_info({table})").fetchall()
            if actual != desired or {r[1] for r in actual} != fields:
                conn.close()
                raise ValueError(f"Invalid database fields/types/constraints in {table}")
            if conn.execute(f"PRAGMA foreign_key_list({table})").fetchall() != reference.execute(f"PRAGMA foreign_key_list({table})").fetchall():
                conn.close()
                raise ValueError(f"Invalid foreign keys in {table}")
        for index in ("memory_scope", "memory_episode"):
            if conn.execute(f"PRAGMA index_info({index})").fetchall() != reference.execute(f"PRAGMA index_info({index})").fetchall():
                conn.close()
                raise ValueError(f"Invalid index {index}")
    return conn


def binding(conn, project):
    row = conn.execute("SELECT project_id FROM memory_bindings WHERE local_id=?", (project_id(project),)).fetchone()
    if not row:
        raise ValueError("Project memory is unbound; run bind first")
    return row[0]


def bind(conn, project, pid=None, name=None):
    local = project_id(project)
    old = conn.execute("SELECT project_id FROM memory_bindings WHERE local_id=?", (local,)).fetchone()
    if old and pid and old[0] != pid:
        raise ValueError("Existing project binding differs; refusing implicit reassignment")
    pid = identifier(pid or (old[0] if old else uuid.uuid4().hex))
    with conn:
        conn.execute("INSERT OR IGNORE INTO memory_projects(id,name,created_at) VALUES(?,?,?)", (pid, name or Path(project).name, now()))
        conn.execute("INSERT OR IGNORE INTO memory_bindings VALUES(?,?)", (local, pid))
    return pid


def gh(*args, input_data=None):
    result = subprocess.run(["gh", "api", *args], input=input_data, text=True, capture_output=True, timeout=60, check=False)
    if result.returncode:
        raise ValueError("GitHub request failed; check gh authentication, repository access and network")
    return json.loads(result.stdout) if result.stdout.strip() else {}


def repository(value):
    value = value.removeprefix("https://github.com/").removesuffix("/").removesuffix(".git")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value):
        raise ValueError("Use a GitHub owner/repository or HTTPS repository URL")
    return value


def configure(conn, pid, remote):
    remote = repository(remote)
    info = gh("repos/" + remote)
    if not info.get("private") or not info.get("permissions", {}).get("push"):
        raise ValueError("Structured experience requires a private repository with write access")
    with conn:
        conn.execute("UPDATE memory_projects SET sync_repository=? WHERE id=?", (remote, pid))
    return remote


def validate_record(record, pid):
    required = {"id", "revision", "project_id", "episode_id", "kind", "status", "payload", "provenance", "created_at"}
    if not isinstance(record, dict) or set(record) != required:
        raise ValueError("Record has missing or unknown fields")
    for key in ("id", "episode_id", "project_id"):
        identifier(record[key])
    if record["project_id"] != pid:
        raise ValueError("Cross-project record rejected")
    if type(record["revision"]) is not int or record["revision"] < 1:
        raise ValueError("Revision must be a positive integer")
    kind = record["kind"]
    if kind not in KINDS or record["status"] not in STATUSES:
        raise ValueError("Invalid kind or status")
    payload = record["payload"]
    if not isinstance(payload, dict) or set(payload) != FIELDS[kind]:
        raise ValueError(f"Invalid {kind} payload fields; expected {sorted(FIELDS[kind])}")
    if not isinstance(record["created_at"], str):
        raise ValueError("Missing creation timestamp")
    datetime.fromisoformat(record["created_at"])
    provenance = record["provenance"]
    if not isinstance(provenance, dict) or set(provenance) != {"agent", "client", "skill_version", "session_id"} or not all(isinstance(v, str) and v for v in provenance.values()):
        raise ValueError("Missing provenance")
    for key, value in payload.items():
        if key.endswith("_ids"):
            if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
                raise ValueError("Evidence and relationship IDs must be arrays")
        elif key == "held_out":
            if type(value) is not bool:
                raise ValueError("held_out must be boolean")
        elif not isinstance(value, str):
            raise ValueError(f"{key} must be a summary string")
    if kind == "episode" and (record["id"] != record["episode_id"] or payload["coverage"] not in {"complete_available", "partial", "unknown"}):
        raise ValueError("Invalid episode identity or coverage")
    if kind == "evidence" and (payload["source_type"] not in {"user_requirement", "user_feedback", "agent_report", "diff", "command", "test"} or payload["availability"] not in {"local_only", "shared_summary", "accessible_reference"}):
        raise ValueError("Invalid evidence type or availability")
    if kind == "finding" and payload["cause_status"] not in {"hypothesis", "confirmed", "unknown"}:
        raise ValueError("Invalid cause status")
    if kind == "lesson" and payload["scope"] not in {"project", "transfer_candidate"}:
        raise ValueError("Shared memory cannot install global policy")
    if kind in {"finding", "requirement", "lesson"} and not payload["evidence_ids"]:
        raise ValueError("A claim needs evidence references")
    if kind == "evidence":
        ref = payload["source_ref"]
        if ref.startswith(("/", "file:", "\\\\")) or re.match(r"^[A-Za-z]:[\\/]", ref):
            raise ValueError("Use source IDs or accessible URLs, not absolute private paths")
    if len(canonical(record).encode()) > 128 * 1024:
        raise ValueError("Structured record exceeds 128 KiB; do not include transcripts")
    # Apply the existing conservative secret redactor without truncating summaries.
    for value in list(payload.values()) + list(provenance.values()):
        if isinstance(value, str) and (len(value) > 16000 or redact(value) != value):
            raise ValueError("Oversized or potentially secret-bearing summary; sanitize before saving")


def records(conn, pid):
    rows = conn.execute("SELECT id,revision,episode_id,kind,status,payload,provenance,created_at FROM memory_records WHERE project_id=? ORDER BY id,revision", (pid,)).fetchall()
    return [dict(id=r[0], revision=r[1], project_id=pid, episode_id=r[2], kind=r[3], status=r[4], payload=json.loads(r[5]), provenance=json.loads(r[6]), created_at=r[7]) for r in rows]


def save_records(conn, pid, items):
    # Serialize validation and insert so another writer cannot win an unchecked race.
    with conn:
        conn.execute("BEGIN IMMEDIATE")
        return _save_records(conn, pid, items)


def _save_records(conn, pid, items):
    if not isinstance(items, list) or len(items) > 10000:
        raise ValueError("Expected a bounded record list")
    known = {(r["id"], r["revision"]): r for r in records(conn, pid)}
    for item in items:
        validate_record(item, pid)
        key = (item["id"], item["revision"])
        if key in known and known[key] != item:
            raise ValueError("Revision conflict; preserve both observations under distinct IDs")
        known[key] = item
    latest = {}
    for (_, rev), item in sorted(known.items(), key=lambda pair: pair[0][1]):
        previous = latest.get(item["id"])
        if previous and (previous["kind"], previous["episode_id"]) != (item["kind"], item["episode_id"]):
            raise ValueError("Revision cannot change kind or episode")
        latest[item["id"]] = item
    for item in latest.values():
        episode = latest.get(item["episode_id"])
        if not episode or episode["kind"] != "episode":
            raise ValueError("Missing episode reference")
        for key, values in item["payload"].items():
            if not key.endswith("_ids") or key == "source_event_ids":
                continue
            expected = "evidence" if key in {"evidence_ids", "counterevidence_ids"} else key[:-4].rstrip("s")
            for ref in values:
                target = latest.get(ref)
                if not target or target["kind"] != expected:
                    raise ValueError("Missing or mistyped relationship reference")
        if item["kind"] == "finding" and item["payload"]["cause_status"] == "confirmed":
            support = [latest[r]["payload"]["source_type"] for r in item["payload"]["evidence_ids"]]
            if not any(t in {"diff", "command", "test"} for t in support):
                raise ValueError("Agent reports alone cannot confirm a technical cause")
    inserted = 0
    with conn:
        for r in items:
            cursor = conn.execute("INSERT OR IGNORE INTO memory_records VALUES(?,?,?,?,?,?,?,?,?,?)", (r["id"], r["revision"], pid, r["episode_id"], r["kind"], r["status"], canonical(r["payload"]), canonical(r["provenance"]), r["created_at"], digest(r)))
            inserted += cursor.rowcount
    return inserted


def package(conn, pid):
    return {"schema_version": VERSION, "project_id": pid, "records": records(conn, pid)}


def import_package(conn, pid, data):
    if not isinstance(data, dict) or set(data) != {"schema_version", "project_id", "records"} or data["schema_version"] != VERSION:
        raise ValueError("Unsupported exchange schema")
    if data["project_id"] != pid:
        raise ValueError("Package belongs to another project")
    count = save_records(conn, pid, data["records"])
    with conn:
        conn.execute("INSERT OR IGNORE INTO memory_packages VALUES(?,?,?)", (digest(data), pid, now()))
    return count


def read_json(file):
    path = Path(file)
    if path.stat().st_size > 16 * 1024 * 1024:
        raise ValueError("Exchange exceeds 16 MiB; split into smaller packages")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(file, value):
    path = Path(file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    path.chmod(0o600)


def session_context(conn, project, client, session):
    rows = conn.execute("SELECT id,kind,content,timestamp FROM events WHERE project_id=? AND client=? AND session_id=? ORDER BY timestamp,rowid", (project_id(project), client, session)).fetchall()
    if not rows:
        raise ValueError("No captured events for this project/client/session")
    return {"client": client, "session_id": session, "coverage": "unknown", "limitations": "All available recorded events; host capture may be incomplete or truncated. Verify against available chat before claiming complete_available.", "events": [dict(id=r[0], kind=r[1], content=r[2], timestamp=r[3]) for r in rows]}


def recall(conn, pid, query):
    latest = {}
    for r in records(conn, pid):
        latest[r["id"]] = r
    terms = query.casefold().split()
    found = [r for r in latest.values() if r["kind"] in {"requirement", "lesson"} and r["status"] in {"accepted", "verified"}]
    found = [(sum(t in canonical(r["payload"]).casefold() for t in terms), r) for r in found]
    return [r for score, r in sorted(found, key=lambda pair: (-pair[0], pair[1]["id"])) if score][:10]


def sync(conn, pid, direction):
    remote = conn.execute("SELECT sync_repository FROM memory_projects WHERE id=?", (pid,)).fetchone()[0]
    if not remote:
        raise ValueError("No sync repository configured during adaptation")
    # Recheck privacy on every exchange; never send local events, blobs or paths.
    info = gh("repos/" + repository(remote))
    if not info.get("private"):
        raise ValueError("Sync repository is no longer private")
    prefix = "projects/" + pid + "/packages/"
    if direction == "push":
        data = package(conn, pid)
        if not data["records"]:
            return {"result": "no_change", "records": 0}
        encoded = canonical(data).encode()
        if len(encoded) > 16 * 1024 * 1024:
            raise ValueError("Project export exceeds 16 MiB")
        name = prefix + digest(data) + ".json"
        # Immutable content-addressed packages; concurrent writers never overwrite a DB.
        try:
            existing = gh("repos/" + remote + "/contents/" + name)
        except ValueError:
            existing = None
        if existing:
            if existing.get("encoding") != "base64":
                existing = gh("repos/" + remote + "/git/blobs/" + existing["sha"])
            if existing.get("encoding") != "base64" or base64.b64decode(existing["content"]) != encoded:
                raise ValueError("Remote package content mismatch")
            return {"result": "already_synced", "path": name}
        gh("repos/" + remote + "/contents/" + name, "--method", "PUT", "--input", "-", input_data=json.dumps({"message": "sync: structured project experience", "content": base64.b64encode(encoded).decode()}))
        return {"result": "uploaded", "path": name, "records": len(data["records"])}
    if info.get("size") == 0:
        return {"result": "no_change", "records": 0}
    tree = gh("repos/" + remote + "/git/trees/" + info["default_branch"] + "?recursive=1")
    if tree.get("truncated"):
        raise ValueError("Remote tree truncated; cannot claim complete synchronization")
    pending = []
    for entry in tree.get("tree", []):
        path = entry["path"]
        if entry["type"] != "blob" or not re.fullmatch(re.escape(prefix) + r"[0-9a-f]{64}\.json", path):
            continue
        if entry.get("size", 0) > 16 * 1024 * 1024:
            raise ValueError("Remote package too large")
        content = gh("repos/" + remote + "/git/blobs/" + entry["sha"])
        data = json.loads(base64.b64decode(content["content"]))
        if digest(data) != Path(path).stem:
            raise ValueError("Remote package hash mismatch")
        if data.get("schema_version") != VERSION or data.get("project_id") != pid or set(data) != {"schema_version", "project_id", "records"}:
            raise ValueError("Incompatible remote package")
        pending.extend(data["records"])
    unique = {}
    for item in pending:
        validate_record(item, pid)
        key = (item["id"], item["revision"])
        if key in unique and unique[key] != item:
            raise ValueError("Conflicting remote revisions")
        unique[key] = item
    count = save_records(conn, pid, list(unique.values()))
    return {"result": "imported", "records": count}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=default_root())
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("bind", "configure", "context", "record", "export", "import", "recall", "sync", "check", "snapshot"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--project", required=True)
        if name == "bind":
            cmd.add_argument("--project-id")
            cmd.add_argument("--name")
        if name == "configure":
            cmd.add_argument("--repository", required=True)
        if name in {"context", "record", "export", "import", "snapshot"}:
            cmd.add_argument("--file", required=True)
        if name == "context":
            cmd.add_argument("--client", required=True)
            cmd.add_argument("--session", required=True)
        if name == "recall":
            cmd.add_argument("--query", required=True)
        if name == "sync":
            cmd.add_argument("--direction", choices=("push", "pull"), required=True)
    args = parser.parse_args()
    conn = open_store(args.state)
    try:
        if args.command == "bind":
            result = {"project_id": bind(conn, args.project, args.project_id, args.name)}
        else:
            pid = binding(conn, args.project)
            if args.command == "configure":
                result = {"repository": configure(conn, pid, args.repository), "mode": "manual"}
            elif args.command == "context":
                value = session_context(conn, args.project, args.client, args.session)
                write_json(args.file, value)
                result = {"file": args.file, "events": len(value["events"]), "local_only": True}
            elif args.command in {"record", "import"}:
                value = read_json(args.file)
                count = save_records(conn, pid, value) if args.command == "record" else import_package(conn, pid, value)
                result = {"inserted": count}
            elif args.command == "export":
                value = package(conn, pid)
                write_json(args.file, value)
                result = {"records": len(value["records"]), "file": args.file}
            elif args.command == "snapshot":
                # Only structured project tables enter the portable SQLite snapshot.
                target = Path(args.file)
                if target.exists():
                    raise ValueError("Snapshot destination already exists")
                target.parent.mkdir(parents=True, exist_ok=True)
                with closing(sqlite3.connect(target)) as out:
                    out.executescript(SCHEMA + f"PRAGMA user_version={VERSION};")
                    row = conn.execute("SELECT id,name,source_repository,'',created_at FROM memory_projects WHERE id=?", (pid,)).fetchone()
                    out.execute("INSERT INTO memory_projects VALUES(?,?,?,?,?)", row)
                    out.commit()
                    save_records(out, pid, records(conn, pid))
                target.chmod(0o600)
                result = {"file": str(target), "raw_transcripts": False}
            elif args.command == "recall":
                result = {"project_id": pid, "records": recall(conn, pid, args.query), "authority": "Context only; current source and user requirements take precedence"}
            elif args.command == "sync":
                result = sync(conn, pid, args.direction)
            else:
                integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
                foreign = conn.execute("PRAGMA foreign_key_check").fetchall()
                if integrity != "ok" or foreign:
                    raise ValueError("Database integrity check failed")
                save_records(conn, pid, records(conn, pid))
                result = {"schema_version": VERSION, "integrity": integrity, "project_id": pid}
        print(json.dumps(result, ensure_ascii=False))
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, sqlite3.Error, subprocess.TimeoutExpired) as exc:
        print(f"agent-memory: {exc}", file=sys.stderr)
        sys.exit(1)
