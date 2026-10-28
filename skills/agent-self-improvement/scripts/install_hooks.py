#!/usr/bin/env python3
"""Opt-in Codex hook installer. Preserves existing hooks and native trust review."""

import argparse
import copy
import json
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from learning_state import state_root

EVENTS = ("UserPromptSubmit", "PostToolUse", "Stop")
LABELS = {
    "UserPromptSubmit": "Record user prompt",
    "PostToolUse": "Record tool result",
    "Stop": "Record assistant response",
}


def needs_default_label(label, event):
    if not isinstance(label, str) or not label.strip():
        return True
    if label == "WebDev: " + LABELS[event].lower():
        return True
    # Recover the observed lossy-encoding label without replacing custom names.
    prefix, separator, suffix = label.partition(":")
    return (separator and prefix == "WebDev" and bool(suffix.strip())
            and set(suffix.strip()) <= {"?", " ", "\ufffd"})


def bridge_path():
    return Path(__file__).resolve().parents[1] / "assets" / "integrations" / "hook_bridge.py"


def handler(event, state=None):
    args = [sys.executable, str(bridge_path()), "--client", "codex"]
    if state is not None:
        args.extend(["--state", str(state)])
    return {
        "type": "command",
        "statusMessage": LABELS[event],
        "command": shlex.join(args),
        "commandWindows": subprocess.list2cmdline(args),
        "timeout": 5,
        "async": True,
    }


def is_owned(entry):
    if not isinstance(entry, dict) or entry.get("type") != "command":
        return False
    try:
        args = shlex.split(entry.get("command", ""))
    except (ValueError, TypeError):
        return False
    # The generated portable command uses shlex.join even on Windows. Match
    # its exact argument structure, independent of the Python executable path.
    return ((len(args) == 4 or (len(args) == 6 and args[4] == "--state")) and args[1] == str(bridge_path())
            and args[2:4] == ["--client", "codex"]
            and (Path(args[0].replace("\\", "/")).name.lower().startswith("python")
                 or args[0] == sys.executable))


def update_hooks(path, remove, state=None):
    if path.exists():
        obj = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(obj, dict):
            raise ValueError("Existing hooks.json must be an object")
    else:
        obj = {}
    original = copy.deepcopy(obj)
    if remove and "hooks" not in obj:
        return obj, False
    hooks = obj.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError("Existing hooks property must be an object")
    for event in EVENTS:
        expected = handler(event, state)
        groups = hooks.get(event, [])
        if not isinstance(groups, list):
            raise ValueError(f"Existing hook groups must be an array: {event}")
        retained = []
        found = False
        for group in groups:
            if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
                retained.append(group)
                continue
            entries = []
            removed_owned = False
            for entry in group["hooks"]:
                # Match a generated bridge invocation, not a substring in an
                # unrelated shell command. Preserve custom handler/group fields.
                owned = is_owned(entry)
                if not owned:
                    entries.append(entry)
                    continue
                found = True
                if remove:
                    removed_owned = True
                    continue
                entry = dict(entry)
                if state is not None:
                    entry["command"] = expected["command"]
                    entry["commandWindows"] = expected["commandWindows"]
                label = entry.get("statusMessage")
                if needs_default_label(label, event):
                    entry["statusMessage"] = LABELS[event]
                entries.append(entry)
            if entries or not removed_owned:
                retained.append({**group, "hooks": entries})
        if not remove and not found:
            retained.append({"hooks": [expected]})
        if event in hooks or retained:
            hooks[event] = retained
    return obj, obj != original


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--state", type=Path)
    parser.add_argument("--approve", action="store_true")
    parser.add_argument("--remove", action="store_true")
    args = parser.parse_args()
    root = Path(args.project).expanduser().resolve(strict=True)
    target = root / ".codex" / "hooks.json"
    if target.is_symlink() or target.parent.is_symlink():
        raise ValueError("Hook target cannot be a symlink")
    resolved = state_root(root, args.state)
    selected = resolved
    data, changed = update_hooks(target, args.remove, selected)
    if not args.approve:
        print(json.dumps({"target": str(target), "changed": changed,
                          "approved": False, "preview": data}, ensure_ascii=False))
        return
    if changed:
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
