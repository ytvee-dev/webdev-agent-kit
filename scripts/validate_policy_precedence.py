#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "common" / "policy-precedence.md"
EXPECTED_ORDER = (
    "System, client security, and sandbox restrictions.",
    "Current direct user request.",
    "Explicitly confirmed scope and approvals.",
    "Existing host-project instructions.",
    "Verified `project/**` facts.",
    "Selected skill workflow.",
    "Active frontend profile.",
    "Generic kit defaults.",
)
FORBIDDEN_ABSOLUTE_PATTERNS = (
    r"\b(?:this|the)\s+(?:skill|profile|adapter|rule|policy)\s+always\s+(?:wins|overrides)\b",
    r"\b(?:skill|profile|adapter|rule|policy)\s+(?:takes precedence|has higher priority)\s+over\b",
    r"\bignore\s+(?:system|client|user|host-project|project)\s+instructions\b",
    r"\bregardless of\s+(?:system|client|user|host-project|project)\s+instructions\b",
    r"\boverrides?\s+(?:all|any)\s+(?:system|client|user|host-project|project)\s+instructions\b",
)


def runtime_markdown_files():
    roots = (
        ROOT / "AGENTS.md",
        ROOT / "common",
        ROOT / "profiles",
        ROOT / "adapters",
        ROOT / "skills",
    )
    files = [roots[0]]
    for directory in roots[1:]:
        files.extend(directory.rglob("*.md"))
    return sorted(set(files))


def validate():
    errors = []
    if not POLICY_PATH.is_file():
        return ["common/policy-precedence.md is required"]

    policy = POLICY_PATH.read_text(encoding="utf-8-sig")
    previous_position = -1
    for index, statement in enumerate(EXPECTED_ORDER, start=1):
        numbered = f"{index}. {statement}"
        position = policy.find(numbered)
        if position == -1:
            errors.append(f"Policy precedence is missing: {numbered}")
        elif position <= previous_position:
            errors.append("Policy precedence statements are out of order")
        previous_position = position

    required_routes = {
        "AGENTS.md": ROOT / "AGENTS.md",
        "common/core/runtime-core-policy.md": (
            ROOT / "common" / "core" / "runtime-core-policy.md"
        ),
    }
    for label, path in required_routes.items():
        text = path.read_text(encoding="utf-8-sig")
        if "common/policy-precedence.md" not in text:
            errors.append(
                f"{label} must route conflicts to common/policy-precedence.md"
            )

    for path in runtime_markdown_files():
        text = path.read_text(encoding="utf-8-sig")
        relative = path.relative_to(ROOT).as_posix()
        for pattern in FORBIDDEN_ABSOLUTE_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                errors.append(
                    f"{relative} contains forbidden absolute precedence wording: {pattern}"
                )

        if relative.startswith("skills/"):
            copied = [statement for statement in EXPECTED_ORDER if statement in text]
            if copied:
                errors.append(
                    f"{relative} repeats the global precedence list: {', '.join(copied)}"
                )

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate centralized instruction precedence policy."
    )
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Policy precedence contract is valid and centralized.")


if __name__ == "__main__":
    main()
