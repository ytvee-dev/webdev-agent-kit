#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG_PATTERN = re.compile(r"^v\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


def load_version():
    manifest = json.loads((ROOT / "bundle-manifest.json").read_text(encoding="utf-8"))
    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("bundle-manifest.json version must be a non-empty string")
    return version


def validate_tag(tag):
    errors = []
    if not TAG_PATTERN.fullmatch(tag):
        errors.append(f"Release tag must be v-prefixed SemVer, got {tag!r}")
        return errors
    expected = f"v{load_version()}"
    if tag != expected:
        errors.append(f"Release tag {tag!r} must match source version {expected!r}")
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Require a v-prefixed release tag matching source metadata."
    )
    parser.add_argument(
        "--tag",
        help="Tag to validate. Defaults to v<bundle-manifest version>.",
    )
    args = parser.parse_args()
    try:
        tag = args.tag or f"v{load_version()}"
        errors = validate_tag(tag)
    except Exception as exc:
        errors = [f"Cannot validate release tag: {exc}"]
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print(f"Release tag {tag} matches source version metadata.")


if __name__ == "__main__":
    main()
