"""Bounded project telemetry export; immutable archives and disposable run context."""
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path

from learning import redact
from learning_processing import lock
from learning_project import read_config, write_json


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Telemetry timestamps require a timezone")
    return parsed.astimezone(UTC)


def sanitize(value):
    if isinstance(value, dict):
        return {k: "[REDACTED]" if re.search(r"(?i)(authorization|password|secret|api.?key|access.?token|cookie)", k)
                else sanitize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize(v) for v in value]
    if isinstance(value, str):
        safe = re.sub(r'(?i)\bBasic\s+[A-Za-z0-9+/=]{16,}', 'Basic [REDACTED]', redact(value))
        return safe + (" [TRUNCATED]" if len(value) > 65536 else "")
    return value


def assess(row, config):
    """Mechanical suitability screen, not a semantic verdict or verified lesson."""
    spec = config["telemetry"]
    tags = set(row.get("tags") or [])
    required = set(spec.get("required_tags") or [])
    stable = {t for t in tags if t.startswith("project-id:")}
    matched = (bool(required) and required <= tags and (not stable or stable == {"project-id:" + config["project_id"]}))
    if matched and required and spec.get('stable_tag') and not stable:
        # Friendly-tag compatibility ends at project initialization. New traces
        # require stable identity; missing dates cannot prove historical scope.
        try:
            matched = (spec.get('historical_tag') in tags and
                       timestamp(row['startTime']) < timestamp(config['created_at']))
        except (KeyError, TypeError, ValueError):
            matched = False
    if not required:
        matched = bool(spec.get("project_metadata_key")) and row.get("metadata", {}).get(spec["project_metadata_key"]) == spec.get("project_metadata_value")
    reasons = []
    synthetic = 'learning:validation' in tags
    if synthetic:
        reasons.append('synthetic_validation_not_learning')
    if not matched:
        reasons.append("project_unverified")
    if not row.get("id") or not row.get("startTime"):
        reasons.append("missing_identity_or_time")
    if "[TRUNCATED]" in json.dumps(row):
        reasons.append("truncated")
    outcome = row.get("type") in {"TOOL", "EVALUATOR"} and row.get("output") is not None
    return {"project_match": matched, "context_candidate": matched and not synthetic and bool(row.get("input") or row.get("output")),
            "outcome_candidate": matched and not synthetic and outcome, "verified": False,
            "semantic_review": "required", "reasons": reasons,
            "independence_key": row.get("traceId") or row.get("id")}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None  # Never forward authorization to another host.


def request_page(spec, start, end, cursor=None, *, authorization=None):
    base = spec["base_url"].rstrip("/")
    if urllib.parse.urlparse(base).scheme != "https":
        raise ValueError("Telemetry requires HTTPS")
    auth = authorization or os.environ.get(spec["authorization_env"])
    if not auth:
        raise RuntimeError("not_connected")
    filters = ([{"type": "arrayOptions", "column": "tags", "operator": "all of", "value": spec["required_tags"]}]
               if spec.get("required_tags") else [{"type": "stringObject", "column": "metadata", "key": spec["project_metadata_key"],
                "operator": "=", "value": spec["project_metadata_value"]}])
    query = {"fromStartTime": start, "toStartTime": end, "limit": spec.get("page_size", 10),
             "fields": spec.get("fields", "core,basic,metadata,io,usage,trace_context"), "filter": json.dumps(filters)}
    if cursor:
        query["cursor"] = cursor
    req = urllib.request.Request(base + "/api/public/v2/observations?" + urllib.parse.urlencode(query),
                                 headers={"Authorization": auth, "Accept": "application/json"})
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=20) as response:
            content = response.read(8 * 1024 * 1024 + 1)
            if len(content) > 8 * 1024 * 1024:
                raise RuntimeError("response_too_large")
            return json.loads(content)
    except urllib.error.HTTPError as exc:
        # Do not expose URLs, payloads or credentials in diagnostics.
        raise RuntimeError("http_" + str(exc.code)) from None
    except urllib.error.URLError:
        raise RuntimeError("network_unavailable") from None


def normalize_windows(windows):
    normalized = sorted({(timestamp(start), timestamp(end)) for start, end in windows})
    result = []
    for start, end in normalized:
        if start >= end:
            raise ValueError('Invalid telemetry interval')
        if result and start <= result[-1][1]:
            result[-1] = (result[-1][0], max(end, result[-1][1]))
        else:
            result.append((start, end))
    return result


def export_selected(project, windows, fetch=request_page, now=None):
    """Export only selected incident windows, with bounded resumable readback."""
    config = read_config(project)
    spec = config['telemetry']
    state = Path(project).resolve() / '.agents/learning'
    if not spec.get('enabled'):
        return {'status': 'disabled', 'database_only': True}
    if not (spec.get('required_tags') or (spec.get('project_metadata_key') and spec.get('project_metadata_value'))):
        return {'status': 'project_mapping_unavailable', 'database_only': True}
    ranges = normalize_windows(windows)
    if not ranges:
        return {'status': 'unmatched', 'database_only': True}
    now = now or datetime.now(UTC)
    floor = now - timedelta(days=min(30, spec.get('access_days', 30)))
    pages, accepted, cached, missing = 0, 0, 0, 0
    deadline = time.monotonic() + 120
    status = 'complete'
    with lock(state, state / 'telemetry'):
        try:
            for start, end in ranges:
                if start < floor or end > now:
                    missing += 1
                start, end = max(start, floor), min(end, now)
                if start >= end:
                    continue
                key = hashlib.sha256(json.dumps([config['project_id'], spec, start.isoformat(), end.isoformat()], sort_keys=True).encode()).hexdigest()
                receipt = state / 'telemetry-windows' / (key + '.json')
                saved = json.loads(receipt.read_text(encoding='utf-8')) if receipt.exists() else {}
                if saved.get('complete'):
                    cached += 1
                    continue
                cursor, seen = saved.get('cursor'), set()
                while True:
                    if pages >= min(1000, spec.get('max_pages', 100)):
                        raise RuntimeError('page_budget_exhausted')
                    if time.monotonic() >= deadline:
                        raise RuntimeError('time_budget_exhausted')
                    pages += 1
                    response = fetch(spec, start.isoformat(), end.isoformat(), cursor)
                    if not isinstance(response.get('data'), list) or not isinstance(response.get('meta'), dict):
                        raise RuntimeError('invalid_response')
                    for raw in response['data']:
                        if not raw.get('startTime') or not raw.get('id') or not assess(raw, config)['project_match']:
                            continue
                        at = timestamp(raw['startTime'])
                        if not start <= at < end:
                            continue
                        value = sanitize(raw)
                        payload = dict(project_id=config['project_id'], observation=value, assessment=assess(value, config))
                        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
                        path = state / 'archive' / at.strftime('%Y-%m') / (digest + '.json')
                        if not path.exists():
                            write_json(path, payload)
                        accepted += 1
                    following = response['meta'].get('cursor')
                    if following and (following == cursor or following in seen):
                        raise RuntimeError('repeated_cursor')
                    write_json(receipt, dict(complete=not following, cursor=following))
                    if not following:
                        break
                    seen.add(following)
                    cursor = following
        except (RuntimeError, ValueError, OSError) as exc:
            status = str(exc) if isinstance(exc, RuntimeError) else 'invalid_or_unavailable'
    result = dict(status=status if status != 'complete' or accepted or cached else 'empty_unknown_reason',
                  pages=pages, accepted=accepted, cached_windows=cached, unavailable_windows=missing,
                  coverage_complete=status == 'complete' and not missing,
                  database_only=not accepted and not cached)
    write_json(state / 'telemetry-status.json', result)
    return result


def export(project, fetch=request_page, now=None):
    config = read_config(project)
    state = Path(project).resolve() / ".agents/learning"
    spec = config["telemetry"]
    if not spec.get("enabled") or not (spec.get("required_tags") or (spec.get("project_metadata_key") and spec.get("project_metadata_value"))):
        result = {"status": "project_mapping_unavailable", "database_only": True}
        write_json(state / "telemetry-status.json", result)
        return result
    now = now or datetime.now(UTC)
    with lock(state, state / "telemetry"):
        watermark = state / "telemetry-watermark.json"
        checkpoint = state / "telemetry-checkpoint.json"
        start = now - timedelta(days=min(30, spec.get("access_days", 30)))
        if watermark.exists():
            start = max(start, timestamp(json.loads(watermark.read_text())["complete_until"]) - timedelta(hours=spec.get("overlap_hours", 48)))
        resume_cursor = None
        signature = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()
        if checkpoint.exists():
            saved = json.loads(checkpoint.read_text())
            if saved.get('signature') == signature and timestamp(saved['start']) >= now - timedelta(days=30):
                start, now = timestamp(saved['start']), timestamp(saved['until'])
                resume_cursor = saved.get('cursor')
        initial = start
        pages, accepted, rejected = 0, 0, 0
        status = "complete"
        deadline = time.monotonic() + 120
        try:
            while start < now:
                end = min(now, start + timedelta(days=14))
                cursor, seen = resume_cursor, set()
                resume_cursor = None
                while True:
                    if time.monotonic() > deadline:
                        raise RuntimeError("time_budget_exhausted")
                    if pages >= min(1000, spec.get("max_pages", 100)):
                        raise RuntimeError("page_budget_exhausted")
                    pages += 1
                    try:
                        result = fetch(spec, start.isoformat(), end.isoformat(), cursor)
                    except RuntimeError as exc:
                        size = spec.get('page_size', 10)
                        if str(exc) == 'response_too_large' and size > 1:
                            spec = dict(spec, page_size=max(1, size // 2))
                            continue
                        raise
                    if not isinstance(result.get("data"), list) or not isinstance(result.get("meta"), dict):
                        raise RuntimeError("invalid_response")
                    for raw in result["data"]:
                        assessment = assess(raw, config)
                        if not assessment["project_match"] or not raw.get("startTime") or not raw.get("id"):
                            rejected += 1
                            continue
                        at = timestamp(raw["startTime"])
                        if not start <= at < end:
                            rejected += 1
                            continue
                        row = sanitize(raw)
                        payload = {"project_id": config["project_id"], "observation": row, "assessment": assess(row, config)}
                        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
                        path = state / "archive" / at.strftime("%Y-%m") / (digest + ".json")
                        if not path.exists():
                            write_json(path, payload)
                        accepted += 1
                    cursor = result["meta"].get("cursor")
                    write_json(checkpoint, {'signature': signature, 'start': (start if cursor else end).isoformat(),
                               'until': now.isoformat(), 'cursor': cursor})
                    if not cursor:
                        break
                    if cursor in seen:
                        raise RuntimeError("repeated_cursor")
                    seen.add(cursor)
                start = end
        except (RuntimeError, ValueError, OSError) as exc:
            status = str(exc) if isinstance(exc, RuntimeError) else "invalid_or_unavailable"
        # Only a complete, paginated window advances the watermark. Empty is not proof of quota.
        if status == "complete":
            write_json(watermark, {"complete_until": now.isoformat()})
            checkpoint.unlink(missing_ok=True)
        result = {"status": status if accepted or status != "complete" else "empty_unknown_reason",
                  "from": initial.isoformat(), "to": now.isoformat(), "pages": pages,
                  "accepted": accepted, "rejected": rejected, "database_only": accepted == 0,
                  "coverage_complete": status == "complete"}
        write_json(state / "telemetry-status.json", result)
        return result


def prepare(project, run_id, months, windows=None):
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,80}", run_id) or any(not re.fullmatch(r"\d{4}-\d{2}", m) for m in months):
        raise ValueError("Invalid run ID or month")
    state = Path(project).resolve() / ".agents/learning"
    config = read_config(project)
    destination = state / "runs" / run_id
    if destination.resolve().parent != (state / "runs").resolve():
        raise ValueError("Unsafe run directory")
    destination.mkdir(parents=True, exist_ok=True)
    rows = {}
    ranges = normalize_windows(windows) if windows is not None else None
    total_bytes = 0
    truncated = False
    for month in sorted(set(months)):
        for path in sorted((state / "archive" / month).glob("*.json")):
            value = json.loads(path.read_text(encoding="utf-8"))
            if hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest() != path.stem:
                raise ValueError("Archive digest mismatch")
            if value["project_id"] != config["project_id"]:
                raise ValueError("Wrong project archive")
            observation = value["observation"]
            if ranges is not None and (not observation.get('startTime') or not any(
                    start <= timestamp(observation['startTime']) < end for start, end in ranges)):
                continue
            if not assess(observation, config)['project_match']:
                continue
            size = len(json.dumps(value, ensure_ascii=False).encode('utf-8'))
            if total_bytes + size > 8 * 1024 * 1024:
                truncated = True
                continue
            total_bytes += size
            # Preserve revisions; identical overlap records are one entry.
            rows[path.stem] = value
    cache = destination / "telemetry.jsonl"
    cache.write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in rows.values()), encoding="utf-8")
    write_json(destination / "telemetry-manifest.json", {"months": months, "entries": len(rows),
               "sha256": hashlib.sha256(cache.read_bytes()).hexdigest(), "durable_archive_ids": list(rows)})
    return {"cache": str(cache), "entries": len(rows), "truncated": truncated}


def cleanup(project, run_id):
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,80}", run_id):
        raise ValueError("Invalid run ID")
    state = Path(project).resolve() / ".agents/learning"
    folder = state / "runs" / run_id
    if folder.resolve().parent != (state / "runs").resolve():
        raise ValueError("Unsafe run directory")
    if not (folder / "completion.json").is_file():
        raise ValueError("Save decisions and durable evidence before cleanup")
    (folder / "telemetry.jsonl").unlink(missing_ok=True)
    return {"scratch_removed": True, "archive_preserved": True}
