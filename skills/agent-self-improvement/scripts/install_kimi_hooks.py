#!/usr/bin/env python3
"""Preview or install project-filtered Kimi hooks without rewriting user TOML."""
import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path


def update(text, project, remove=False):
    parsed = tomllib.loads(text)
    if parsed.get("hooks") == [] and not remove:
        # Only replace a root-level empty array declaration, never nested keys.
        text = re.sub(r"(?m)^hooks\s*=\s*\[\s*\][ \t]*(?:#[^\n]*)?\n?", "", text, count=1)
    key = hashlib.sha256(str(project).encode()).hexdigest()[:16]
    start = "# BEGIN WEBDEV KIMI " + key
    end = "# END WEBDEV KIMI " + key
    if text.count(start) != text.count(end) or text.count(start) > 1:
        raise ValueError("Ambiguous WebDev hook markers")
    original_hooks = parsed.get("hooks", [])
    if not isinstance(original_hooks, list):
        raise ValueError("Hooks must be an array")
    owned = []
    if start in text:
        # Only whole comment lines delimit generated content.
        pattern = re.compile(r"(?m)^" + re.escape(start) + r"\n(.*?)^" + re.escape(end) + r"(?:\n|$)", re.S)
        matches = list(pattern.finditer(text))
        if len(matches) != 1:
            raise ValueError("Ambiguous WebDev hook markers")
        match = matches[0]
        block = tomllib.loads(match.group(1))
        owned = block.get("hooks", [])
        if set(block) != {"hooks"} or not owned or any(
            set(hook) != {"event", "command", "timeout"}
            or "hook_bridge.py" not in hook["command"] for hook in owned
        ):
            raise ValueError("Managed hook block was customized; reconcile it manually")
        text = text[:match.start()] + text[match.end():]
    retained = list(original_hooks)
    for hook in owned:
        retained.remove(hook)
    if remove:
        expected = dict(parsed)
        if retained:
            expected["hooks"] = retained
        else:
            expected.pop("hooks", None)
        actual = tomllib.loads(text)
        if actual.get("hooks") == []:
            actual.pop("hooks")
        if actual != expected:
            raise ValueError("Removing hooks would change unrelated TOML; reconcile manually")
        return text
    bridge = Path(__file__).resolve().parents[1] / "assets/integrations/hook_bridge.py"
    args = [sys.executable, str(bridge), "--client", "kimi", "--project", str(project)]
    if os.name == "nt" and any(any(c in arg for c in '&|<>^%!()\r\n') for arg in args):
        raise ValueError("Windows hook paths must not contain cmd shell metacharacters; use a plain path")
    command = subprocess.list2cmdline(args) if os.name == "nt" else shlex.join(args)
    block = start + "\n"
    for event in ("UserPromptSubmit", "PostToolUse", "PostToolUseFailure", "Stop"):
        block += '\n[[hooks]]\nevent = ' + json.dumps(event) + '\ncommand = ' + json.dumps(command) + '\ntimeout = 5\n'
    result = text.rstrip() + "\n\n" + block + end + "\n"
    try:
        tomllib.loads(result)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError("Convert inline hooks arrays to [[hooks]] tables before installation; configuration was not changed") from exc
    expected = dict(parsed)
    added = tomllib.loads(block.removeprefix(start + "\n"))["hooks"]
    expected["hooks"] = retained + added
    if tomllib.loads(result) != expected:
        raise ValueError("Updating hooks would change unrelated TOML; reconcile manually")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--approve", action="store_true")
    parser.add_argument("--remove", action="store_true")
    args = parser.parse_args()
    project = args.project.expanduser().resolve(strict=True)
    target = args.config or Path((os.environ.get("KIMI_CODE_HOME") or str(Path.home() / ".kimi-code"))) / "config.toml"
    if target.is_symlink() or target.parent.is_symlink():
        raise ValueError("Config target cannot be a symlink")
    original = target.read_text(encoding="utf-8") if target.exists() else ""
    updated = update(original, project, args.remove)
    changed = updated != original
    if args.approve and changed:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            fd, _backup = tempfile.mkstemp(prefix="config.toml.wdk-backup-", dir=target.parent)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(original)
        fd, temporary = tempfile.mkstemp(prefix=".wdk-kimi-", dir=target.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(updated)
            os.replace(temporary, target)
        finally:
            Path(temporary).unlink(missing_ok=True)
    # Never print user configuration: it may contain provider credentials.
    print(json.dumps({"target": str(target), "project": str(project),
                      "changed": changed, "approved": args.approve,
                      "events": ["UserPromptSubmit", "PostToolUse", "PostToolUseFailure", "Stop"],
                      "capture": "Requires separate learning.py on opt-in"}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError):
        print("Kimi hook setup failed. Check TOML syntax (use [[hooks]] tables), plain Windows paths and non-symlink config/backup paths. No successful installation is claimed.", file=sys.stderr)
        sys.exit(1)
