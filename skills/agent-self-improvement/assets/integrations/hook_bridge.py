#!/usr/bin/env python3
"""Nonblocking Codex/Claude lifecycle event bridge; no transcript file access."""
import argparse
import json
import subprocess
import sys
import uuid
from pathlib import Path


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
        content = event.get("last_assistant_message") or ""
    elif name == "PostToolUse":
        kind = "tool"
        tool = str(event.get("tool_name") or "tool")[:160]
        response = event.get("tool_response")
        result = json.dumps(response, ensure_ascii=False)[:3000] if response is not None else ""
        content = f"Tool: {tool}\nOutcome: {result}"
    else:
        kind = "system_event"
        content = name
    if not isinstance(content, str):
        content = json.dumps(content, ensure_ascii=False)
    identifier = event.get("tool_use_id") or event.get("turn_id")
    if not identifier:
        identifier = event.get("message_id") or name + "-" + uuid.uuid4().hex
    return project, {
        "client": client,
        "session_id": session,
        "message_id": str(identifier)[:180],
        "kind": kind,
        "content": content,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", choices=("codex", "claude-code"), required=True)
    args = parser.parse_args()
    event_name = None
    try:
        payload = json.load(sys.stdin)
        event_name = payload.get("hook_event_name") if isinstance(payload, dict) else None
        entry = normalize(payload, args.client)
        if entry is None:
            return
        project, data = entry
        cli = Path(__file__).resolve().parents[2] / "scripts" / "learning.py"
        subprocess.run(
            [sys.executable, str(cli), "capture", "--project", project],
            input=json.dumps(data, ensure_ascii=False),
            text=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=3, check=False,
        )
    except (OSError, ValueError, TypeError, subprocess.TimeoutExpired, json.JSONDecodeError):
        # Collection errors must never block a user's primary agent.
        pass
    finally:
        # Codex Stop requires JSON on stdout even when nothing is recorded.
        if args.client == "codex" and event_name == "Stop":
            print("{}")


if __name__ == "__main__":
    main()
