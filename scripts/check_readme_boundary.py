#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN_ROOTS = (
    ROOT / "AGENTS.md",
    ROOT / "common",
    ROOT / "skills",
    ROOT / "templates",
    ROOT / "examples",
)
EXCLUDED_PARTS = {"dist", "project", "node_modules", ".obsidian"}
EXCLUDED_FILES = {ROOT / "README.md"}

PROHIBITED_PATTERNS = (
    re.compile(r"\bread\s+`?README\.md`?", re.IGNORECASE),
    re.compile(r"\bopen\s+`?README\.md`?", re.IGNORECASE),
    re.compile(r"\binspect\s+`?README\.md`?", re.IGNORECASE),
    re.compile(r"\bscan\s+`?README\.md`?", re.IGNORECASE),
    re.compile(r"\bsearch\s+`?README\.md`?", re.IGNORECASE),
    re.compile(r"\buse\s+`?README\.md`?\s+for\s+project\s+context", re.IGNORECASE),
    re.compile(r"\buse\s+`?README\.md`?\s+for\s+routing", re.IGNORECASE),
    re.compile(r"\bderive\s+project\s+facts\s+from\s+`?README\.md`?", re.IGNORECASE),
    re.compile(r"\bupdate\s+`?README\.md`?\s+(?:after|during|as)", re.IGNORECASE),
)

ALLOWED_CONTEXT_PATTERNS = (
    re.compile(r"do\s+not\s+(?:read|open|inspect|scan|search|edit|update|autonomously\s+update)\s+`?README\.md`?", re.IGNORECASE),
    re.compile(r"never\s+(?:read|open|inspect|scan|search|edit|update)\s+`?README\.md`?", re.IGNORECASE),
    re.compile(r"`?README\.md`?\s+is\s+(?:a\s+)?human-facing", re.IGNORECASE),
    re.compile(r"not\s+(?:runtime|routing|policy|validation|context)", re.IGNORECASE),
    re.compile(r"propose\s+.*README", re.IGNORECASE),
)


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_ROOTS:
        if root.is_file():
            files.append(root)
            continue
        if not root.exists():
            continue
        files.extend(sorted(root.rglob("*.md")))
    return [path for path in files if path not in EXCLUDED_FILES and not (set(path.parts) & EXCLUDED_PARTS)]


def is_allowed_context(line: str) -> bool:
    return any(pattern.search(line) for pattern in ALLOWED_CONTEXT_PATTERNS)


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    for index, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if "README" not in line:
            continue
        if is_allowed_context(line):
            continue
        for pattern in PROHIBITED_PATTERNS:
            if pattern.search(line):
                relative = path.relative_to(ROOT).as_posix()
                errors.append(f"{relative}:{index}: prohibited README runtime instruction: {line.strip()}")
                break
    return errors


def main() -> None:
    errors: list[str] = []
    for path in markdown_files():
        errors.extend(check_file(path))
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("README boundary validation passed.")


if __name__ == "__main__":
    main()
