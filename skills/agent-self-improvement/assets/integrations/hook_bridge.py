#!/usr/bin/env python3
"""Nonblocking Codex/Claude lifecycle event bridge; no transcript file access."""
import argparse
import json
import subprocess
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from learning import MAX_EVENT_BYTES  # noqa: E402
from learning_health import capture_health  # noqa: E402


def normalize(event, client):
    if not isinstance(event, dict):
        return None
    session = event.get("session_id")
    project = event.get("cwd")
    if not isinstance(session, str) or not isinstance(project, str):
        return None
    name = str(event.get("hook_event_name") or "event")
    if name == "UserPromptSubmit":
        kind = "user"
        content = event.get("prompt") or ""
    elif name == "Stop":
        kind = "assistant"
        content = event.get("last_assistant_message") or "[Assistant text unavailable in hook payload]"
    elif name == "PostToolUse":
        kind = "tool"
        tool = str(event.get("tool_name") or "tool")[:160]
        response = event.get("tool_response")
        raw = json.dumps(response, ensure_ascii=False) if response is not None else ""
        result = raw[:3000]
        if len(raw) > 3000:
            result += f"\n[TRUNCATED: retained 3000 of {len(raw)} characters]"
        content = f"Tool: {tool}\nOutcome: {result}"
    else:
        kind = "system_event"
        content = name
    if not isinstance(content, str):
        content = json.dumps(content, ensure_ascii=False)
    identifier = event.get("tool_use_id") or event.get("message_id") or event.get("turn_id")
    synthetic = not identifier
    if not identifier:
        identifier = event.get("message_id") or name + "-" + uuid.uuid4().hex
    return project, {
        "client": client,
        "session_id": session,
        "message_id": str(identifier)[:180],
        "kind": kind,
        "content": content,
        "timestamp": event.get("timestamp"),
        "id_quality": "synthetic" if synthetic else "client",
        "truncated": name == "PostToolUse" and len(raw) > 3000,
        "content_missing": name == "Stop" and not event.get("last_assistant_message"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path)
    parser.add_argument("--client", choices=("codex", "claude-code"), required=True)
    args = parser.parse_args()
    event_name = None
    project = None
    try:
        raw_input = sys.stdin.buffer.read(MAX_EVENT_BYTES + 1)
        if len(raw_input) > MAX_EVENT_BYTES:
            raise ValueError("oversize")
        payload = json.loads(raw_input.decode("utf-8"))
        event_name = payload.get("hook_event_name") if isinstance(payload, dict) else None
        entry = normalize(payload, args.client)
        if entry is None:
            return
        project, data = entry
        cli = Path(__file__).resolve().parents[2] / "scripts" / "learning.py"
        result = subprocess.run(
            [sys.executable, str(cli), *(["--state", str(args.state)] if args.state else []), "capture", "--project", project],
            input=json.dumps(data, ensure_ascii=False),
            text=True, encoding="utf-8", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=3, check=False,
        )
        if result.returncode:
            capture_health(project, "error", "client_failure")
    except (OSError, ValueError, TypeError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        # Collection errors must never block a user's primary agent.
        if project:
            capture_health(project, "error", "timeout" if isinstance(exc, subprocess.TimeoutExpired) else "invalid")
    finally:
        # Codex Stop requires JSON on stdout even when nothing is recorded.
        if args.client == "codex" and event_name == "Stop":
            print("{}")


if __name__ == "__main__":
    main()
