#!/usr/bin/env python3
"""Non-blocking, consent-gated Codex/Claude lifecycle hook bridge.

Install manually with an absolute path. Does not fetch arbitrary transcript paths.
"""
import json
import subprocess
import sys
from pathlib import Path


def main():
    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict):
            return
        source = "codex" if event.get("hook_event_name") else "claude-code"
        name = str(event.get("hook_event_name") or event.get("hook_event") or "event")
        project = event.get("cwd")
        session = event.get("session_id")
        if not isinstance(project, str) or not isinstance(session, str):
            return
        if name in {"UserPromptSubmit", "user_prompt_submit"}:
            kind = "user"
            content = str(event.get("prompt") or "")
        elif name in {"PostToolUse", "post_tool_use"}:
            kind = "tool"
            content = str(event.get("tool_name") or "tool")[:160] + " completed"
        else:
            kind = "system_event"
            content = name
        identifier = str(event.get("turn_id") or event.get("tool_use_id") or name)[:180]
        canonical = {"client": source, "session_id": session,
                     "message_id": identifier, "kind": kind, "content": content}
        cli = Path(__file__).resolve().parents[2] / "scripts" / "learning.py"
        subprocess.run([sys.executable, str(cli), "capture", "--project", project],
                       input=json.dumps(canonical), text=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=2, check=False)
    except (Exception, KeyboardInterrupt):
        # A recorder must never prevent the host agent from working.
        return


if __name__ == "__main__":
    main()
