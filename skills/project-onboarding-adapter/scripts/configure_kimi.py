#!/usr/bin/env python3
"""Preview or merge a project-scoped Kimi instruction pointer."""

import argparse
import json
import os
import tempfile
from pathlib import Path

START = "<!-- BEGIN WEBDEV KIMI -->"
END = "<!-- END WEBDEV KIMI -->"


def update_pointer(text, root, remove=False):
    lines = text.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.strip() == START]
    ends = [i for i, line in enumerate(lines) if line.strip() == END]
    if len(starts) != len(ends) or len(starts) > 1 or (starts and starts[0] >= ends[0]):
        raise ValueError("Ambiguous WebDev pointer markers; reconcile them manually")
    block = (
        START
        + "\n"
        + "For work in this project, read "
        + json.dumps(str(root / ".agents/AGENTS.md"))
        + " and "
        + json.dumps(str(root / ".agents/adapters/kimi.md"))
        + ". Resolve bundle paths under "
        + json.dumps(str(root / ".agents"))
        + ". Preserve other host instructions and their scope.\n"
        + END
        + "\n"
    )
    if starts:
        lines[starts[0] : ends[0] + 1] = [] if remove else [block]
        return "".join(lines)
    if remove:
        return text
    return text + ("\n" if text and not text.endswith("\n") else "") + block


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--approve", action="store_true")
    parser.add_argument("--remove", action="store_true")
    args = parser.parse_args()
    root = args.project.expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Project must be a directory")
    if not args.remove and not all(
        (root / ".agents" / name).is_file() for name in ("AGENTS.md", "adapters/kimi.md")
    ):
        raise ValueError("Extract the project Kimi archive before configuring its pointer")
    target = root / ".kimi-code/AGENTS.md"
    if target.is_symlink() or target.parent.is_symlink():
        raise ValueError("Kimi instruction target cannot be a symlink")
    original = target.read_text(encoding="utf-8") if target.exists() else ""
    updated = update_pointer(original, root, args.remove)
    changed = updated != original
    if args.approve and changed:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            fd, _backup = tempfile.mkstemp(prefix="AGENTS.md.wdk-backup-", dir=target.parent)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(original)
        fd, name = tempfile.mkstemp(prefix=".wdk-pointer-", dir=target.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(updated)
            os.replace(name, target)
        finally:
            Path(name).unlink(missing_ok=True)
    print(
        json.dumps(
            {
                "target": str(target),
                "changed": changed,
                "approved": args.approve,
                "remove": args.remove,
            }
        )
    )


if __name__ == "__main__":
    main()
