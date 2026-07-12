#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SMOKE_CASES = {
    "lightweight-bypass": {
        "common/goal-contract.md": (
            "Do not create a durable goal contract for lightweight work.",
        ),
        "skills/execution-plan-manager/SKILL.md": (
            "Do not use this skill for `Lightweight Workflow` prompts",
        ),
    },
    "bounded-clarification": {
        "common/goal-contract.md": (
            "Ask exactly one question at a time and no more than three questions",
            "three-question limit",
        ),
        "skills/goal-planner/SKILL.md": (
            "ask exactly one question",
            "at a time and no more than three",
        ),
    },
    "criterion-coverage": {
        "common/planning-rules.md": (
            "Every durable plan must map active acceptance criteria",
            "planned | in-progress | verified | blocked | superseded",
        ),
        "templates/execution-plan.md": (
            "- S-### [AC-###]:",
            "Coverage:",
        ),
    },
    "read-only-analysis": {
        "common/planning-analysis-rules.md": (
            "repeatable, read-only pass",
            "Any `blocking` or `high` finding stops implementation handoff.",
        ),
        "skills/execution-plan-manager/SKILL.md": (
            "In `analyze` mode",
            "Implementation Handoff: proceed | stop",
        ),
    },
    "append-only-convergence": {
        "common/convergence-rules.md": (
            "append exactly one new section",
            "leave the durable plan byte-for-byte unchanged",
        ),
        "skills/execution-plan-manager/SKILL.md": (
            "Plan Update: unchanged | appended Convergence Pass N",
        ),
    },
    "current-request-reconciliation": {
        "common/convergence-rules.md": (
            "current user request changed",
            "reconcile that intent in `create` or `resume` mode before convergence",
        ),
        "common/policy-precedence.md": ("2. Current direct user request.",),
    },
    "independent-review-boundary": {
        "skills/frontend-quality-reviewer/SKILL.md": (
            "Must not add, remove, reorder, renumber, or mark execution-plan slices",
            "execution-plan-manager` in `converge` mode",
        ),
        "common/independent-review-rules.md": (
            "report remaining work without adding or renumbering plan slices",
        ),
    },
    "stable-loop-resume": {
        "skills/loop-workflow-planner/SKILL.md": (
            "affected `AC-###` and `S-###`",
            "Existing slice identifiers must be referenced",
        ),
        "common/checkpoint-rules.md": (
            "last completed `S-###` slice and covered `AC-###` criteria",
            "next `S-###` slice",
        ),
    },
}


def load_manifest() -> dict:
    return json.loads((ROOT / "bundle-manifest.json").read_text(encoding="utf-8"))


def validate_entrypoint(target: str, canonical: str, root: Path) -> list[str]:
    errors: list[str] = []
    if canonical == "claude-code":
        required = root / ".claude-plugin" / "plugin.json"
    elif canonical == "cursor":
        required = root / ".cursor" / "rules" / "webdev-agent-kit.mdc"
    else:
        required = root / "AGENTS.md"
    if not required.is_file():
        errors.append(f"dist/{target}: smoke entrypoint is missing")
    return errors


def validate_case(target: str, root: Path, case: str, requirements: dict) -> list[str]:
    errors: list[str] = []
    for relative, phrases in requirements.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"dist/{target} [{case}]: missing {relative}")
            continue
        text = path.read_text(encoding="utf-8-sig")
        for phrase in phrases:
            if phrase not in text:
                errors.append(
                    f"dist/{target} [{case}]: {relative} is missing {phrase!r}"
                )
    return errors


def validate() -> list[str]:
    errors: list[str] = []
    try:
        manifest = load_manifest()
    except Exception as exc:
        return [f"Cannot parse bundle-manifest.json: {exc}"]

    targets = manifest.get("targets", {})
    aliases = manifest.get("target_aliases", {})
    all_targets = (*targets, *aliases)
    if len(all_targets) != 6:
        errors.append("planning smoke requires six generated runtime targets")

    for target in all_targets:
        canonical = aliases.get(target, target)
        root = DIST / target
        if not root.is_dir():
            errors.append(f"dist/{target}: generated target is missing")
            continue
        errors.extend(validate_entrypoint(target, canonical, root))
        for case, requirements in SMOKE_CASES.items():
            errors.extend(validate_case(target, root, case, requirements))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run portable planning contract smoke checks across targets."
    )
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    checks = len(SMOKE_CASES) * 6
    print(f"Cross-client planning smoke checks passed: {checks} target cases.")


if __name__ == "__main__":
    main()
