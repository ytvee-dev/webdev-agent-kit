#!/usr/bin/env python3
"""Private, opt-in, standard-library-only experience recorder and offline triage."""
import argparse
import base64
import binascii
import hashlib
import json
import os
import re
import sqlite3
import sys
import tempfile
import uuid
from datetime import UTC, datetime
from pathlib import Path

MAX_EVENT_BYTES = 262144
MAX_TEXT = 65536
MAX_ATTACHMENT = 20 * 1024 * 1024
MAX_TOTAL_BLOBS = 2 * 1024 * 1024 * 1024
KINDS = {"user", "assistant", "tool", "user_correction", "system_event"}
TOKEN_PATTERNS = [
    re.compile(r"(?i)(bearer\s+)[a-z0-9._~+/\-]{10,}"),
    re.compile(r"(?i)\b(sk-[a-z0-9_-]{12,})\b"),
    re.compile(r"(?i)((?:api[_-]?key|secret|password|token)\s*[:=]\s*)[^\s,;\"']+"),
]


def utc_now():
    return datetime.now(UTC).isoformat()


def default_root():
    override = os.environ.get("AGENT_LEARNING_STATE")
    if override:
        return Path(override).expanduser()
    if sys.platform == "win32":
        return Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "agent-self-improvement"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "agent-self-improvement"
    return Path(os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local" / "state"))) / "agent-self-improvement"


def project_id(root):
    canonical = os.path.normcase(str(Path(root).expanduser().resolve()))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:24]


def redact(text):
    value = str(text)[:MAX_TEXT]
    for pattern in TOKEN_PATTERNS:
        value = pattern.sub(lambda m: (m.group(1) if m.lastindex and m.lastindex > 1 else "") + "[REDACTED]", value)
    return value


def create_store(root):
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    if root.is_symlink():
        raise ValueError("State directory cannot be a symbolic link")
    db = root / "experience.sqlite3"
    conn = sqlite3.connect(str(db), timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=10000")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY, path TEXT NOT NULL, recording INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY, project_id TEXT NOT NULL, client TEXT NOT NULL,
            session_id TEXT NOT NULL, message_id TEXT NOT NULL, part_id TEXT NOT NULL,
            kind TEXT NOT NULL, timestamp TEXT NOT NULL, source_url TEXT,
            content TEXT NOT NULL, skills_json TEXT NOT NULL, attachments_json TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_events_project ON events(project_id, timestamp);
        CREATE TABLE IF NOT EXISTS blobs (
            digest TEXT PRIMARY KEY, size INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS attachments (
            id TEXT PRIMARY KEY, project_id TEXT NOT NULL, client TEXT NOT NULL,
            session_id TEXT NOT NULL, digest TEXT NOT NULL, display_name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS runs (
            id TEXT PRIMARY KEY, project_id TEXT NOT NULL, timestamp TEXT NOT NULL,
            observed INTEGER NOT NULL, findings INTEGER NOT NULL, result TEXT NOT NULL
        );
    """)
    if os.name == "posix":
        os.chmod(root, 0o700)
        os.chmod(db, 0o600)
    return conn


def opt_in(conn, project):
    row = conn.execute("SELECT recording FROM projects WHERE id=?", (project_id(project),)).fetchone()
    return bool(row and row[0])


def set_mode(conn, project, enabled):
    path = str(Path(project).expanduser().resolve())
    pid = project_id(path)
    conn.execute(
        "INSERT INTO projects(id,path,recording) VALUES(?,?,?) "
        "ON CONFLICT(id) DO UPDATE SET recording=excluded.recording",
        (pid, path, int(enabled)),
    )
    conn.commit()
    return {"project_id": pid, "recording": enabled}


def safe_input(limit=MAX_EVENT_BYTES):
    raw = sys.stdin.buffer.read(limit + 1)
    if len(raw) > limit:
        raise ValueError("Event exceeds the input size limit")
    return json.loads(raw.decode("utf-8"))


def normalize(event, project, client_override=None):
    if not isinstance(event, dict):
        raise ValueError("Event must be a JSON object")
    client = str(client_override or event.get("client") or "")[:60]
    session = str(event.get("session_id") or "")[:200]
    kind = str(event.get("kind") or "")
    if not client or not session or kind not in KINDS:
        raise ValueError("Event requires client, session_id and supported kind")
    text = event.get("content", "")
    if not isinstance(text, str):
        text = json.dumps(text, ensure_ascii=False)
    text = redact(text)
    message = str(event.get("message_id") or hashlib.sha256(text.encode()).hexdigest())[:200]
    part = str(event.get("part_id") or "")[:200]
    skills = event.get("skills", [])
    if not isinstance(skills, list):
        skills = []
    skills = [redact(item)[:120] for item in skills if isinstance(item, str)][:50]
    attachments = event.get("attachments", [])
    if not isinstance(attachments, list):
        attachments = []
    metadata = [
        {"name": redact(a.get("name", ""))[:120], "mime": str(a.get("mime", ""))[:100],
         "status": "metadata_only"}
        for a in attachments[:50] if isinstance(a, dict)
    ]
    source = event.get("source_url")
    source = str(source)[:2048] if source else None
    pid = project_id(project)
    identity = json.dumps([pid, client, session, message, part, kind], ensure_ascii=False)
    eid = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    timestamp = str(event.get("timestamp") or utc_now())[:60]
    return (eid, pid, client, session, message, part, kind, timestamp, source, text,
            json.dumps(skills, ensure_ascii=False), json.dumps(metadata, ensure_ascii=False))


def capture(conn, project, event, client_override=None):
    if not opt_in(conn, project):
        return {"recorded": False, "reason": "collection_disabled"}
    record = normalize(event, project, client_override)
    cur = conn.execute(
        "INSERT OR IGNORE INTO events VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", record
    )
    conn.commit()
    return {"recorded": bool(cur.rowcount), "id": record[0], "duplicate": not bool(cur.rowcount)}


def ingest_file(conn, project, file):
    counts = {"inserted": 0, "duplicates": 0}
    if not opt_in(conn, project):
        raise PermissionError("Collection is off for this project")
    with Path(file).open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            if len(line.encode("utf-8")) > MAX_EVENT_BYTES:
                raise ValueError(f"Line {number} exceeds size limit")
            result = capture(conn, project, json.loads(line))
            counts["inserted" if result["recorded"] else "duplicates"] += 1
    return counts


def store_bytes(conn, state, project, client, session, filename, data):
    if not opt_in(conn, project):
        raise PermissionError("Collection is off for this project")
    exists = conn.execute(
        "SELECT 1 FROM events WHERE project_id=? AND client=? AND session_id=? LIMIT 1",
        (project_id(project), client, session),
    ).fetchone()
    if not exists:
        raise ValueError("Cannot attach without a recorded session")
    if len(data) > MAX_ATTACHMENT:
        raise ValueError("Attachment exceeds 20 MiB")
    digest = hashlib.sha256(data).hexdigest()
    total = conn.execute("SELECT COALESCE(SUM(size),0) FROM blobs").fetchone()[0]
    known = conn.execute("SELECT 1 FROM blobs WHERE digest=?", (digest,)).fetchone()
    if not known and total + len(data) > MAX_TOTAL_BLOBS:
        raise ValueError("Private attachment storage exceeds 2 GiB quota")
    dest = state / "blobs" / digest[:2] / digest
    dest.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not dest.exists():
        with tempfile.NamedTemporaryFile(dir=dest.parent, delete=False) as temporary:
            temporary.write(data)
            temp_path = Path(temporary.name)
        os.chmod(temp_path, 0o600)
        os.replace(temp_path, dest)
    identity = json.dumps([project_id(project), client, session, digest])
    aid = hashlib.sha256(identity.encode()).hexdigest()
    conn.execute("INSERT OR IGNORE INTO blobs VALUES(?,?)", (digest, len(data)))
    conn.execute(
        "INSERT OR IGNORE INTO attachments VALUES(?,?,?,?,?,?)",
        (aid, project_id(project), client, session, digest, str(filename)[:180]),
    )
    conn.commit()
    return {"attachment_id": aid, "sha256": digest, "bytes": len(data)}


def attach(conn, state, project, client, session, file):
    path = Path(file).expanduser()
    if path.is_symlink() or not path.is_file():
        raise ValueError("Attachment must be a regular non-symlink file")
    if path.stat().st_size > MAX_ATTACHMENT:
        raise ValueError("Attachment exceeds 20 MiB")
    return store_bytes(conn, state, project, client, session, path.name, path.read_bytes())


def attach_data(conn, state, project, item):
    if not isinstance(item, dict):
        raise ValueError("Inline attachment must be a JSON object")
    uri = item.get("data_url")
    if not isinstance(uri, str) or len(uri) > MAX_ATTACHMENT * 2:
        raise ValueError("Invalid inline attachment")
    head, separator, encoded = uri.partition(",")
    if not separator or not head.startswith("data:") or not head.endswith(";base64"):
        raise ValueError("Only base64 inline data URLs are supported")
    mime = head[5:-7].lower()
    if not re.fullmatch(r"[a-z0-9.+-]+/[a-z0-9.+-]+", mime):
        raise ValueError("Unsupported inline attachment MIME format")
    try:
        payload = base64.b64decode(encoded, validate=True)
    except binascii.Error as exc:
        raise ValueError("Malformed inline base64 attachment") from exc
    return store_bytes(
        conn, state, project, str(item.get("client", ""))[:60],
        str(item.get("session_id", ""))[:200],
        str(item.get("name", "attachment"))[:180], payload,
    )


def run_triage(conn, state, project):
    pid = project_id(project)
    records = conn.execute(
        "SELECT id, content, client, session_id FROM events "
        "WHERE project_id=? AND kind='user_correction' ORDER BY timestamp", (pid,)
    ).fetchall()
    groups = {}
    for event_id, content, client, session in records:
        key = re.sub(r"\s+", " ", content.strip().casefold())[:180]
        if not key:
            continue
        group = groups.setdefault(key, {"sample": content[:320], "evidence_ids": [],
                                        "sessions": set()})
        group["evidence_ids"].append(event_id)
        group["sessions"].add((client, session))
    findings = [
        {"observation": group["sample"], "evidence_ids": group["evidence_ids"],
         "distinct_sessions": len(group["sessions"]),
         "status": "candidate_for_review" if len(group["sessions"]) >= 2 else "single_observation"}
        for group in groups.values()
    ]
    rid = str(uuid.uuid4())
    outcome = "needs_review" if findings else "no_change"
    report = {"run_id": rid, "project_id": pid, "created_at": utc_now(),
              "result": outcome, "evidence_events": len(records),
              "findings": findings,
              "limitations": "Exact-text clustering only; no model evaluation or skill edits were performed."}
    directory = state / "runs"
    directory.mkdir(mode=0o700, exist_ok=True)
    output = directory / (rid + ".json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if os.name == "posix":
        os.chmod(output, 0o600)
    conn.execute("INSERT INTO runs VALUES(?,?,?,?,?,?)",
                 (rid, pid, report["created_at"], len(records), len(findings), outcome))
    conn.commit()
    return {"run_id": rid, "result": outcome, "findings": len(findings), "report": str(output)}


def purge(conn, state, project, session=None):
    pid = project_id(project)
    if session:
        conn.execute("DELETE FROM events WHERE project_id=? AND session_id=?", (pid, session))
        conn.execute("DELETE FROM attachments WHERE project_id=? AND session_id=?", (pid, session))
    else:
        conn.execute("DELETE FROM events WHERE project_id=?", (pid,))
        conn.execute("DELETE FROM attachments WHERE project_id=?", (pid,))
        conn.execute("DELETE FROM projects WHERE id=?", (pid,))
    if conn.execute("SELECT 1 FROM sqlite_master WHERE name='memory_bindings'").fetchone():
        row = conn.execute("SELECT project_id FROM memory_bindings WHERE local_id=?", (pid,)).fetchone()
        if row:
            shared_pid = row[0]
            if session:
                episodes = {r[0] for r in conn.execute(
                    "SELECT episode_id FROM memory_records WHERE project_id=? AND json_extract(provenance,'$.session_id')=?",
                    (shared_pid, session))}
                for episode in episodes:
                    conn.execute("DELETE FROM memory_records WHERE project_id=? AND episode_id=?", (shared_pid, episode))
            else:
                conn.execute("DELETE FROM memory_records WHERE project_id=?", (shared_pid,))
            conn.execute("DELETE FROM memory_packages WHERE project_id=?", (shared_pid,))
    # Derived reports must be removed too; they can contain purged source text.
    prior_runs = [row[0] for row in conn.execute("SELECT id FROM runs WHERE project_id=?", (pid,))]
    for run_id in prior_runs:
        (state / "runs" / (run_id + ".json")).unlink(missing_ok=True)
    conn.execute("DELETE FROM runs WHERE project_id=?", (pid,))
    # Derived proposals and diffs can quote removed conversation content.
    for candidate in (state / "proposals").glob("*.json"):
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if data.get("project_id") == pid:
            candidate.with_suffix(".diff").unlink(missing_ok=True)
            candidate.unlink(missing_ok=True)
    for checkpoint in (state / "checkpoints").glob("*.json"):
        try:
            data = json.loads(checkpoint.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if data.get("project_id") == pid:
            checkpoint.unlink(missing_ok=True)
    used = {row[0] for row in conn.execute("SELECT DISTINCT digest FROM attachments")}
    for (digest,) in conn.execute("SELECT digest FROM blobs").fetchall():
        if digest not in used:
            (state / "blobs" / digest[:2] / digest).unlink(missing_ok=True)
            conn.execute("DELETE FROM blobs WHERE digest=?", (digest,))
    conn.commit()
    retained = [str(p) for p in state.glob("experience.pre-v2-*.sqlite3")]
    return {"purged": True, "project_id": pid, "session": session,
            "retained_migration_backups": retained,
            "warning": "Local migration backups and remote packages may still contain this project's data; purge does not erase Git history or external copies."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=default_root(), help="Private local state directory")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    for name in ("on", "off", "status", "sessions", "capture", "capture-batch", "import", "attach", "attach-data", "run", "purge"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--project", required=True, help="Project root; must be explicitly enabled")
        if name == "capture":
            cmd.add_argument("--client", help="Override event client when the hook supplies a common format")
        if name == "import":
            cmd.add_argument("--file", required=True)
        if name == "attach":
            cmd.add_argument("--client", required=True)
            cmd.add_argument("--session", required=True)
            cmd.add_argument("--file", required=True)
        if name == "purge":
            cmd.add_argument("--session")
    args = parser.parse_args()
    state = args.state.expanduser().resolve()
    from learning_memory import open_store
    conn = open_store(state)
    try:
        if args.command == "init":
            result = {"state": str(state), "recording": False}
        elif args.command in {"on", "off"}:
            result = set_mode(conn, args.project, args.command == "on")
        elif args.command == "status":
            pid = project_id(args.project)
            count = conn.execute("SELECT COUNT(*) FROM events WHERE project_id=?", (pid,)).fetchone()[0]
            attachments = conn.execute(
                "SELECT COUNT(*) FROM attachments WHERE project_id=?", (pid,)
            ).fetchone()[0]
            result = {"project_id": pid, "recording": opt_in(conn, args.project),
                      "events": count, "attachments": attachments}
        elif args.command == "sessions":
            pid = project_id(args.project)
            rows = conn.execute(
                "SELECT client, session_id, COUNT(*), MAX(timestamp) FROM events "
                "WHERE project_id=? GROUP BY client, session_id ORDER BY MAX(timestamp) DESC LIMIT 100",
                (pid,),
            ).fetchall()
            result = {"project_id": pid, "sessions": [
                {"client": row[0], "session_id": row[1],
                 "events": row[2], "last_at": row[3]} for row in rows
            ]}
        elif args.command == "capture":
            result = capture(conn, args.project, safe_input(), args.client)
        elif args.command == "capture-batch":
            payload = safe_input(3 * 1024 * 1024)
            if not isinstance(payload, list) or len(payload) > 500:
                raise ValueError("capture-batch requires an array of <=500 events")
            counts = {"recorded": 0, "duplicates": 0}
            for item in payload:
                outcome = capture(conn, args.project, item)
                if outcome.get("recorded"):
                    counts["recorded"] += 1
                elif outcome.get("duplicate"):
                    counts["duplicates"] += 1
            result = counts
        elif args.command == "attach-data":
            result = attach_data(conn, state, args.project, safe_input(28 * 1024 * 1024))
        elif args.command == "import":
            result = ingest_file(conn, args.project, args.file)
        elif args.command == "attach":
            result = attach(conn, state, args.project, args.client, args.session, args.file)
        elif args.command == "run":
            result = run_triage(conn, state, args.project)
        else:
            result = purge(conn, state, args.project, args.session)
        print(json.dumps(result, ensure_ascii=False))
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, PermissionError, sqlite3.Error, json.JSONDecodeError) as exc:
        print(f"agent-learning: {exc}", file=sys.stderr)
        sys.exit(1)
