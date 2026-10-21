#!/usr/bin/env python3
"""Opt-in Codex hook installer. Preserves existing hooks and native trust review."""
import argparse
import json
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


EVENTS = ("UserPromptSubmit", "PostToolUse", "Stop")


def bridge_path():
    return Path(__file__).resolve().parents[1] / "assets" / "integrations" / "hook_bridge.py"


def handler():
    args = [sys.executable, str(bridge_path()), "--client", "codex"]
    return {
        "type": "command",
        "command": shlex.join(args),
        "commandWindows": subprocess.list2cmdline(args),
        "timeout": 5,
        "async": True,
    }


def update_hooks(path, remove):
    if path.exists():
        obj = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(obj, dict):
            raise ValueError("Existing hooks.json must be an object")
    else:
        obj = {}
    hooks = obj.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError("Existing hooks property must be an object")
    expected = handler()
    modified = False
    for event in EVENTS:
        groups = hooks.get(event, [])
        if not isinstance(groups, list):
            raise ValueError(f"Existing hook groups must be an array: {event}")
        retained = []
        for group in groups:
            if not isinstance(group, dict):
                retained.append(group)
                continue
            entries = group.get("hooks", [])
            if not isinstance(entries, list):
                retained.append(group)
                continue
            cleaned = [
                entry for entry in entries
                if not (
                    isinstance(entry, dict)
                    and str(bridge_path()) in str(entry.get("command", ""))
                    and "--client codex" in str(entry.get("command", ""))
                )
            ]
            if len(entries) != len(cleaned):
                modified = True
            if cleaned:
                retained.append({**group, "hooks": cleaned})
        if not remove:
            retained.append({"hooks": [expected]})
            modified = True
        hooks[event] = retained
    return obj, modified


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--approve", action="store_true")
    parser.add_argument("--remove", action="store_true")
    args = parser.parse_args()
    root = Path(args.project).expanduser().resolve(strict=True)
    target = root / ".codex" / "hooks.json"
    if target.is_symlink() or target.parent.is_symlink():
        raise ValueError("Hook target cannot be a symlink")
    data, changed = update_hooks(target, args.remove)
    if not args.approve:
        print(json.dumps({"target": str(target), "changed": changed,
                          "approved": False, "preview": data}, ensure_ascii=False))
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and changed:
        shutil.copy2(target, target.with_suffix(".json.bak"))
    if changed:
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    print(json.dumps({"target": str(target), "changed": changed,
                      "approved": True, "trust": "Review hooks in Codex /hooks"},
                     ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"learning-hook-installer: {exc}", file=sys.stderr)
        sys.exit(1)
