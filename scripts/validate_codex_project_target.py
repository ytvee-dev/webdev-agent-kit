#!/usr/bin/env python3

import argparse
import sys

from target_validation_common import (
    ROOT,
    file_inventory,
    validate_portable_skills,
    validate_runtime_exclusions,
)

TARGET = ROOT / "dist" / "codex"
ALIAS = ROOT / "dist" / "vs-code-codex"
REQUIRED_FILES = (
    "AGENTS.md",
    "LICENSE",
    "tool-capabilities-manifest.json",
    "common/core/runtime-core-policy.md",
    "profiles/react-typescript/PROFILE.md",
    "adapters/codex.md",
)


def validate():
    if not TARGET.is_dir():
        return ["dist/codex does not exist; run scripts/build_skill_targets.py"]

    errors = validate_runtime_exclusions(TARGET, "dist/codex")
    for relative_path in REQUIRED_FILES:
        if not (TARGET / relative_path).is_file():
            errors.append(f"dist/codex is missing required file {relative_path}")
    for forbidden in (".claude-plugin", ".cursor"):
        if (TARGET / forbidden).exists():
            errors.append(f"dist/codex must not include {forbidden}")
    errors.extend(
        validate_portable_skills(
            TARGET,
            "dist/codex",
            require_openai_metadata=True,
        )
    )
    if not ALIAS.is_dir():
        errors.append("dist/vs-code-codex does not exist")
    elif file_inventory(ALIAS) != file_inventory(TARGET):
        errors.append("dist/vs-code-codex must exactly reuse dist/codex")
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate the generated Codex project target."
    )
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Codex project target and alias are valid.")


if __name__ == "__main__":
    main()
