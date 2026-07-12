#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

from validate_release_tag import load_version, validate_tag

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"


def unreleased_body(require_content=False):
    lines = CHANGELOG.read_text(encoding="utf-8-sig").splitlines()
    try:
        start = lines.index("## Unreleased") + 1
    except ValueError as exc:
        raise ValueError("CHANGELOG.md is missing the Unreleased section") from exc
    end = next(
        (index for index in range(start, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    body = "\n".join(lines[start:end]).strip()
    if "### Added" not in body or "### Changed" not in body:
        raise ValueError("Unreleased notes must contain Added and Changed sections")
    if require_content and not any(line.startswith("- ") for line in body.splitlines()):
        raise ValueError("Unreleased notes must contain at least one release item")
    return body


def build_notes(tag, require_content=False):
    errors = validate_tag(tag)
    if errors:
        raise ValueError("; ".join(errors))
    return (
        f"# WebDev Agent Kit {tag}\n\n"
        f"{unreleased_body(require_content=require_content)}\n\n"
        "## Installation\n\n"
        "Verify the selected archive against `SHA256SUMS`. Extract Codex and "
        "Cursor archives from the project root; they create `.agents/` "
        "automatically. Extract Claude archives as the native "
        "`webdev-agent-kit/` plugin root. See `docs/install/README.md` for the "
        "client-specific entrypoint.\n"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Build release notes from the validated Unreleased changelog."
    )
    parser.add_argument("--tag", help="Release tag. Defaults to the source version.")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate generated notes without writing a file.",
    )
    parser.add_argument(
        "--require-content",
        action="store_true",
        help="Require at least one release item in the Unreleased section.",
    )
    args = parser.parse_args()
    if args.output and args.check:
        parser.error("--output and --check are mutually exclusive")
    if not args.output and not args.check:
        parser.error("one of --output or --check is required")

    try:
        tag = args.tag or f"v{load_version()}"
        notes = build_notes(tag, require_content=args.require_content)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(notes, encoding="utf-8")
    except Exception as exc:
        print(f"Cannot build release notes: {exc}")
        sys.exit(1)
    print(f"Release notes for {tag} are valid.")


if __name__ == "__main__":
    main()
