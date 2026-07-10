#!/usr/bin/env python3

import argparse
import sys

from target_validation_common import (
    ROOT,
    validate_portable_skills,
    validate_runtime_exclusions,
)

TARGET = ROOT / "dist" / "cursor"
REQUIRED_FILES = (
    "AGENTS.md",
    "LICENSE",
    "tool-capabilities-manifest.json",
    ".cursor/rules/webdev-agent-kit.mdc",
    "common/core/runtime-core-policy.md",
    "profiles/react-typescript/PROFILE.md",
    "adapters/cursor.md",
)


def validate():
    if not TARGET.is_dir():
        return ["dist/cursor does not exist; run scripts/build_skill_targets.py"]

    errors = validate_runtime_exclusions(TARGET, "dist/cursor")
    for relative_path in REQUIRED_FILES:
        if not (TARGET / relative_path).is_file():
            errors.append(f"dist/cursor is missing required file {relative_path}")
    for forbidden in (".codex-plugin", ".claude-plugin"):
        if (TARGET / forbidden).exists():
            errors.append(f"dist/cursor must not include {forbidden}")
    errors.extend(
        validate_portable_skills(
            TARGET,
            "dist/cursor",
            require_openai_metadata=False,
        )
    )
    rule_path = TARGET / ".cursor" / "rules" / "webdev-agent-kit.mdc"
    if rule_path.is_file() and ".agents/AGENTS.md" not in rule_path.read_text(
        encoding="utf-8"
    ):
        errors.append("Cursor rule must route to .agents/AGENTS.md")
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate the generated Cursor project target."
    )
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Cursor project target is valid.")


if __name__ == "__main__":
    main()
