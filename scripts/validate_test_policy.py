#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "common" / "test-policy.md"
FORBIDDEN_GLOBAL_RULES = (
    "Do not create or modify tests by default.",
    "Do not create or edit tests by default.",
    "Create no new project tests.",
    "Do not create or edit component tests",
)
NOISY_OUTPUT_PHRASES = (
    "Skipped: test authoring was not requested",
    "test authoring was skipped when not requested",
    "explicitly report that component",
)


def runtime_files():
    files = [ROOT / "AGENTS.md"]
    for directory in ("common", "profiles", "adapters", "skills", "evals"):
        files.extend((ROOT / directory).rglob("*.md"))
        files.extend((ROOT / directory).rglob("*.json"))
    return sorted(set(files))


def validate():
    errors = []
    if not POLICY_PATH.is_file():
        return ["common/test-policy.md is required"]

    policy = POLICY_PATH.read_text(encoding="utf-8-sig")
    for phrase in (
        "Allowed Without Extra Approval",
        "Explicit Request Or Approval Required",
        "CSS-only, copy-only, and other low-risk presentation changes do not create",
        "Do not add routine output such as `Skipped: test authoring was not requested`",
    ):
        if phrase not in policy:
            errors.append(f"common/test-policy.md is missing required rule: {phrase}")

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8-sig")
    if "common/test-policy.md" not in agents:
        errors.append("AGENTS.md must route test decisions to common/test-policy.md")

    for path in runtime_files():
        text = path.read_text(encoding="utf-8-sig")
        relative = path.relative_to(ROOT).as_posix()
        if path != POLICY_PATH:
            for phrase in FORBIDDEN_GLOBAL_RULES:
                if phrase in text:
                    errors.append(
                        f"{relative} contains obsolete blanket rule: {phrase}"
                    )
            for phrase in NOISY_OUTPUT_PHRASES:
                if phrase in text:
                    errors.append(
                        f"{relative} contains noisy skipped-test output: {phrase}"
                    )

    try:
        output_evals = json.loads(
            (ROOT / "evals" / "output-evals.json").read_text(encoding="utf-8")
        )
    except Exception as exc:
        errors.append(f"Cannot read evals/output-evals.json: {exc}")
    else:
        for case in output_evals.get("cases", []):
            if (
                case.get("id")
                == "frontend-layout-implementer.no-component-test-authoring-output"
                and "Skipped" in case.get("required_output_sections", [])
            ):
                errors.append(
                    "CSS/UI output eval must not require a Skipped test section"
                )

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate existing-test, new-test, infrastructure, and reporting boundaries."
    )
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Test change, infrastructure, verification, and reporting policy is valid.")


if __name__ == "__main__":
    main()
