"""Content-free capture health and explicit storage-pressure previews."""
import sqlite3
from contextlib import closing
from datetime import UTC, datetime

from learning_state import check_owner, state_root


def capture_health(project, status, reason=""):
    state = state_root(project)
    try:
        check_owner(project, state)
        if not (state / "experience.sqlite3").is_file():
            return False
        with closing(sqlite3.connect(state / "capture-health.sqlite3", timeout=0.05)) as conn, conn:
            conn.execute("CREATE TABLE IF NOT EXISTS health (status TEXT PRIMARY KEY, count INTEGER, last_at TEXT, reason TEXT)")
            # Fixed vocabulary: never persist exception messages or source payloads.
            if status not in {"recorded", "duplicate", "skipped", "error"}:
                status = "error"
            if reason not in {"disabled", "paused", "invalid", "oversize", "timeout", "storage", "client_failure", "unknown"}:
                reason = "unknown"
            conn.execute("INSERT INTO health VALUES (?,1,?,?) ON CONFLICT(status) DO UPDATE SET count=count+1,last_at=excluded.last_at,reason=excluded.reason",
                         (status, datetime.now(UTC).isoformat(), reason))
        return True
    except (OSError, ValueError, sqlite3.Error):
        return False


def health_status(project):
    path = state_root(project) / "capture-health.sqlite3"
    try:
        with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as conn:
            return {"status": "observed", "counters": [dict(status=r[0], count=r[1], last_at=r[2], reason=r[3])
                    for r in conn.execute("SELECT status,count,last_at,reason FROM health")]}
    except (OSError, sqlite3.Error):
        return {"status": "unverified", "reason": "diagnostics_unavailable"}


def usage(project):
    from learning import retain_raw
    from learning_project import read_config
    state = state_root(project)
    config = read_config(project)
    limits = config.get("storage_limits", {})
    event_limit = limits.get("events", 50000)
    byte_limit = limits.get("database_bytes", 250 * 1024 * 1024)
    if any(type(v) is not int or v <= 0 for v in (event_limit, byte_limit)):
        raise ValueError("Storage limits must be positive integers")
    with closing(sqlite3.connect(state / "experience.sqlite3")) as conn:
        events = conn.execute("SELECT COUNT(*) FROM events WHERE project_id=?", (config['capture_project_id'],)).fetchone()[0]
        records = conn.execute("SELECT COUNT(DISTINCT id) FROM memory_records WHERE project_id=?", (config['project_id'],)).fetchone()[0]
        preview = retain_raw(conn, project, 30, processed_only=True)
    size = sum(p.stat().st_size for p in (state / 'experience.sqlite3', state / 'experience.sqlite3-wal') if p.is_file())
    directories = {name: sum(p.stat().st_size for p in (state / name).rglob('*') if p.is_file() and not p.is_symlink())
                   for name in ('blobs', 'archive', 'outbox', 'snapshots')}
    return {"status": "checked", "events": events, "structured_records": records, "database_bytes": size,
            "other_bytes": directories, "limits": {"events": event_limit, "database_bytes": byte_limit},
            "cleanup_permission_required": events >= event_limit or size >= byte_limit,
            "preview": preview, "capture": health_status(project),
            "action": "Ask before cleanup; retain --days 30 --processed-only previews, --apply requires consent"}
