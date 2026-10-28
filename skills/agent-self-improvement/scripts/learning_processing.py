"""Versioned processing decisions. Knowledge acceptance remains in memory_records."""
import hashlib
import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path


class LearningBusy(ValueError):
    """Another operation owns the resource; not a corrupt database or bad config."""


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def connect(state):
    state.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(state / "experience.sqlite3", timeout=10)
    conn.execute("""CREATE TABLE IF NOT EXISTS learning_decisions (
        sequence INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id TEXT NOT NULL, repo TEXT NOT NULL, record_id TEXT NOT NULL,
        record_digest TEXT NOT NULL, skill_digest TEXT NOT NULL,
        outcome TEXT NOT NULL, proposal TEXT NOT NULL, updated_at TEXT NOT NULL,
        reason TEXT NOT NULL, recheck_when TEXT NOT NULL, details TEXT NOT NULL)""")
    conn.execute("CREATE INDEX IF NOT EXISTS learning_decisions_lookup ON learning_decisions "
                 "(project_id,repo,record_id,record_digest,skill_digest,sequence)")
    # Preserve the old table. Import once; 'reviewed' proves no individual decision.
    conn.execute("CREATE TABLE IF NOT EXISTS learning_migrations (name TEXT PRIMARY KEY)")
    if not conn.execute("SELECT 1 FROM learning_migrations WHERE name='decisions-v2'").fetchone():
        if conn.execute("SELECT 1 FROM sqlite_master WHERE name='learning_processing'").fetchone():
            conn.execute("""INSERT INTO learning_decisions
                (project_id,repo,record_id,record_digest,skill_digest,outcome,proposal,
                 updated_at,reason,recheck_when,details)
                SELECT project_id,repo,record_id,record_digest,skill_digest,
                CASE WHEN outcome='reviewed' THEN 'deferred' ELSE outcome END,
                proposal,updated_at,'Legacy receipt; inspect original evidence',
                'explicit_review','{"legacy":true}' FROM learning_processing""")
        conn.execute("INSERT INTO learning_migrations VALUES ('decisions-v2')")
    conn.commit()
    return conn


@contextmanager
def lock(state, repo):
    """Repository-wide OS lock, released by the OS even after process death."""
    folder = state / "locks"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (digest(str(Path(repo).resolve()).casefold()) + ".v2.lock")
    with path.open("a+b") as handle:
        handle.seek(0, 2)
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise LearningBusy("Learning repository is locked by another operation") from exc
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)


def append(state, receipt, proposal, decisions, details=None):
    conn = connect(state)
    try:
        with conn:
            for record in receipt["records"]:
                decision = decisions.get(record["id"])
                if decision is None:
                    continue
                values = (receipt["project_id"], receipt["repo"], record["id"], record["digest"],
                          record.get("skill_digest", receipt["skill_digest"]), decision["outcome"],
                          str(proposal), decision["reason"], decision.get("recheck_when", ""),
                          json.dumps(details or {}, sort_keys=True))
                previous = conn.execute("SELECT outcome,proposal,reason,recheck_when,details FROM "
                    "learning_decisions WHERE project_id=? AND repo=? AND record_id=? AND "
                    "record_digest=? AND skill_digest=? ORDER BY sequence DESC LIMIT 1", values[:5]).fetchone()
                if previous == values[5:]:
                    continue
                conn.execute("INSERT INTO learning_decisions (project_id,repo,record_id,record_digest,"
                    "skill_digest,outcome,proposal,reason,recheck_when,details,updated_at) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?)", values + (datetime.now(UTC).isoformat(),))
    finally:
        conn.close()


def eligible(state, receipt):
    conn = connect(state)
    result = []
    try:
        for record in receipt["records"]:
            latest = conn.execute("SELECT outcome,recheck_when FROM learning_decisions WHERE "
                "project_id=? AND repo=? AND record_id=? ORDER BY sequence DESC LIMIT 1",
                (receipt["project_id"], receipt["repo"], record["id"])).fetchone()
            if latest == ("deferred", "explicit_review"):
                continue
            row = conn.execute("SELECT outcome,proposal FROM learning_decisions WHERE project_id=? "
                "AND repo=? AND record_id=? AND record_digest=? AND skill_digest=? "
                "ORDER BY sequence DESC LIMIT 1", (receipt["project_id"], receipt["repo"], record["id"],
                record["digest"], record.get("skill_digest", receipt["skill_digest"]))).fetchone()
            if not row or row[0] in {"failed", "analyzing"}:
                result.append(record["id"])
            elif row[0] == "pending":
                path = Path(row[1])
                try:
                    proposal = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    raise ValueError(f"Pending proposal missing or invalid; restore it before analysis: {path}")
                # Failed checks should be resumed, not replaced by another proposal.
                if proposal.get("state") == "rejected":
                    result.append(record["id"])
        return result
    finally:
        conn.close()


def fail_attempt(state, project_id, repo, error):
    """Called under the repository lock; preserve the failed attempt for diagnosis."""
    conn = connect(state)
    try:
        rows = conn.execute("SELECT record_id,record_digest,skill_digest FROM learning_decisions d "
            "WHERE project_id=? AND repo=? AND outcome='analyzing' AND sequence=(SELECT MAX(sequence) "
            "FROM learning_decisions x WHERE x.project_id=d.project_id AND x.repo=d.repo "
            "AND x.record_id=d.record_id)", (project_id, repo)).fetchall()
    finally:
        conn.close()
    if rows:
        receipt = {"project_id": project_id, "repo": repo, "skill_digest": "",
                   "records": [{"id": r[0], "digest": r[1], "skill_digest": r[2]} for r in rows]}
        append(state, receipt, "", {r[0]: {"outcome": "failed", "reason": str(error)[:1200]} for r in rows})
