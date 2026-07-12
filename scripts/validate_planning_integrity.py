#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_MODES = {"create", "resume", "analyze", "converge"}
PLANNING_ACTIONS = {
    "lightweight-bypass",
    "clarify-one-at-a-time",
    "clarify-limit",
    "coverage-complete",
    "enabler-dependencies",
    "analyze-read-only",
    "analyze-blocking-gap",
    "converge-append-only",
    "converge-clean-noop",
    "current-request-reconcile",
    "review-no-slices",
    "resume-stable-ids",
    "client-parity",
}
REQUIRED_PATHS = (
    "bundle-manifest.json",
    "common/goal-contract.md",
    "common/planning-rules.md",
    "common/planning-analysis-rules.md",
    "common/convergence-rules.md",
    "common/policy-precedence.md",
    "common/checkpoint-rules.md",
    "skills/goal-planner/SKILL.md",
    "skills/execution-plan-manager/SKILL.md",
    "skills/loop-workflow-planner/SKILL.md",
    "skills/frontend-quality-reviewer/SKILL.md",
    "templates/goal-contract.md",
    "templates/execution-plan.md",
    "templates/progress-log.md",
    "templates/decision-log.md",
    "templates/loop-workflow-contract.md",
    "evals/planning-workflow-evals.json",
    "evals/cross-model-evals.json",
    "schemas/eval-suite.schema.json",
    "schemas/eval-case.schema.json",
    "scripts/validate_skill_evals.py",
    "scripts/validate_skill_pack.py",
    ".github/workflows/skill-pack-ci.yml",
    ".github/workflows/release.yml",
)


def load_documents() -> tuple[dict[str, str], list[str]]:
    documents: dict[str, str] = {}
    errors: list[str] = []
    for relative in REQUIRED_PATHS:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"planning integrity requires {relative}")
            continue
        documents[relative] = path.read_text(encoding="utf-8-sig")
    return documents, errors


def require_phrases(
    documents: dict[str, str],
    relative: str,
    phrases: tuple[str, ...],
    contract: str,
    errors: list[str],
) -> None:
    text = documents.get(relative, "")
    missing = [phrase for phrase in phrases if phrase not in text]
    if missing:
        missing_text = ", ".join(repr(item) for item in missing)
        errors.append(f"{contract}: {relative} is missing {missing_text}")


def parse_json_document(
    documents: dict[str, str], relative: str, errors: list[str]
) -> object | None:
    try:
        return json.loads(documents.get(relative, ""))
    except Exception as exc:
        errors.append(f"planning JSON contract: cannot parse {relative}: {exc}")
        return None


def validate_documents(documents: dict[str, str]) -> list[str]:
    errors: list[str] = []

    execution_skill = documents.get("skills/execution-plan-manager/SKILL.md", "")
    mode_match = re.search(
        r"3\. Choose one explicit mode:(.*?)4\. In `analyze` mode",
        execution_skill,
        flags=re.DOTALL,
    )
    found_modes = (
        set(re.findall(r"^\s+- `([a-z]+)`:", mode_match.group(1), re.MULTILINE))
        if mode_match
        else set()
    )
    if found_modes != CANONICAL_MODES:
        errors.append(
            "canonical modes: execution-plan-manager must define exactly "
            "create, resume, analyze, and converge"
        )

    require_phrases(
        documents,
        "common/goal-contract.md",
        ("`G-###`", "`AC-###`", "superseded", "three-question limit"),
        "goal identifier contract",
        errors,
    )
    require_phrases(
        documents,
        "templates/goal-contract.md",
        ("Goal ID: G-###", "- AC-###:"),
        "goal template contract",
        errors,
    )
    require_phrases(
        documents,
        "common/planning-rules.md",
        (
            "`S-###`",
            "`AC-###`",
            "Coverage Map",
            "planned | in-progress | verified | blocked | superseded",
        ),
        "coverage contract",
        errors,
    )
    require_phrases(
        documents,
        "templates/execution-plan.md",
        ("- S-### [AC-###]:", "Coverage:", "| AC-### | S-### |"),
        "execution template contract",
        errors,
    )
    require_phrases(
        documents,
        "skills/execution-plan-manager/SKILL.md",
        (
            "Map every active `AC-###` to at least one `S-###`",
            "planned`, `in-progress`, `verified`, `blocked`, or `superseded",
        ),
        "coverage skill alignment",
        errors,
    )

    require_phrases(
        documents,
        "common/planning-analysis-rules.md",
        (
            "repeatable, read-only pass",
            "PA-001",
            "Any `blocking` or `high` finding stops implementation handoff.",
            "edit the plan, goal, decisions, application code, configuration, or tests",
        ),
        "analysis contract",
        errors,
    )
    require_phrases(
        documents,
        "skills/execution-plan-manager/SKILL.md",
        (
            "In `analyze` mode",
            "Do not write analysis",
            "Implementation Handoff: proceed | stop",
        ),
        "analysis skill alignment",
        errors,
    )

    require_phrases(
        documents,
        "common/convergence-rules.md",
        (
            "append exactly one new section",
            "F-001",
            "leave the durable plan byte-for-byte unchanged",
            "Never delete the work or assume",
        ),
        "append-only convergence",
        errors,
    )
    require_phrases(
        documents,
        "skills/execution-plan-manager/SKILL.md",
        (
            "append one convergence pass only",
            "with zero findings, preserve it byte-for-byte",
            "Plan Update: unchanged | appended Convergence Pass N",
        ),
        "byte-identical clean convergence",
        errors,
    )

    require_phrases(
        documents,
        "common/policy-precedence.md",
        ("2. Current direct user request.",),
        "current-user precedence",
        errors,
    )
    require_phrases(
        documents,
        "common/convergence-rules.md",
        (
            "Apply `common/policy-precedence.md`.",
            "current user request changed",
            "reconcile that intent in `create` or `resume` mode before convergence",
        ),
        "current-user precedence",
        errors,
    )

    require_phrases(
        documents,
        "common/goal-contract.md",
        ("one question at a time", "no more than three"),
        "clarification limit",
        errors,
    )
    require_phrases(
        documents,
        "skills/goal-planner/SKILL.md",
        ("ask exactly one question", "at a time and no more than three"),
        "clarification limit",
        errors,
    )

    require_phrases(
        documents,
        "common/checkpoint-rules.md",
        (
            "last completed `S-###` slice and covered `AC-###` criteria",
            "next `S-###` slice",
            "latest convergence pass",
            "local-only `project/**`",
            "must not duplicate",
        ),
        "checkpoint alignment",
        errors,
    )
    require_phrases(
        documents,
        "skills/frontend-quality-reviewer/SKILL.md",
        (
            "Must not add, remove, reorder, renumber, or mark execution-plan slices",
            "judge every in-scope `AC-###`",
            "execution-plan-manager` in `converge` mode",
        ),
        "reviewer alignment",
        errors,
    )
    require_phrases(
        documents,
        "skills/loop-workflow-planner/SKILL.md",
        (
            "affected `AC-###` and `S-###`",
            "Existing slice identifiers must be referenced",
            "Memory updates must stay in local-only `project/**` files.",
        ),
        "loop alignment",
        errors,
    )
    require_phrases(
        documents,
        "templates/progress-log.md",
        (
            "Goal ID:",
            "Slice ID:",
            "Criteria Covered:",
            "Convergence Pass:",
            "Next Slice ID:",
        ),
        "resume template alignment",
        errors,
    )
    require_phrases(
        documents,
        "templates/decision-log.md",
        (
            "Affected Criteria:",
            "Criteria Change:",
            "Supersedes Criteria:",
            "Replacement Criteria:",
            "Affected Slices:",
        ),
        "decision template alignment",
        errors,
    )
    require_phrases(
        documents,
        "templates/loop-workflow-contract.md",
        (
            "Goal ID: G-###",
            "Target Slices: S-###",
            "criterion: AC-###",
            "criteria: AC-###",
            "slices: S-###",
            "next slice: S-###",
        ),
        "loop template alignment",
        errors,
    )

    manifest = parse_json_document(documents, "bundle-manifest.json", errors)
    if isinstance(manifest, dict):
        skills = manifest.get("skills")
        if not isinstance(skills, list) or len(skills) != 19:
            errors.append("skill inventory: bundle-manifest.json must list 19 skills")
        elif "spec-driven-feature-manager" in skills:
            errors.append(
                "skill inventory: spec-driven-feature-manager must not be added"
            )

    planning_suite = parse_json_document(
        documents, "evals/planning-workflow-evals.json", errors
    )
    if isinstance(planning_suite, dict):
        cases = planning_suite.get("cases", [])
        actions = {
            case.get("planning_action") for case in cases if isinstance(case, dict)
        }
        if planning_suite.get("eval_type") != "planning-integrity":
            errors.append("planning eval suite: eval_type must be planning-integrity")
        if len(cases) != 13 or actions != PLANNING_ACTIONS:
            errors.append(
                "planning eval suite: exactly 13 canonical planning actions "
                "are required"
            )

    cross_model = parse_json_document(documents, "evals/cross-model-evals.json", errors)
    if isinstance(cross_model, dict):
        dimensions = {
            case.get("parity_dimension")
            for case in cross_model.get("cases", [])
            if isinstance(case, dict)
        }
        if "planning-integrity" not in dimensions:
            errors.append(
                "planning eval suite: cross-model parity needs planning-integrity"
            )

    require_phrases(
        documents,
        "schemas/eval-suite.schema.json",
        ('"planning-integrity"',),
        "planning eval schema",
        errors,
    )
    require_phrases(
        documents,
        "schemas/eval-case.schema.json",
        ('"planning_action"', '"expected_mode"', '"planning-integrity"'),
        "planning eval schema",
        errors,
    )
    require_phrases(
        documents,
        "scripts/validate_skill_evals.py",
        ("PLANNING_EXPECTATIONS", '"planning-integrity"'),
        "planning eval validation",
        errors,
    )

    for relative in (
        "scripts/validate_skill_pack.py",
        ".github/workflows/skill-pack-ci.yml",
        ".github/workflows/release.yml",
    ):
        require_phrases(
            documents,
            relative,
            ("validate_planning_integrity.py",),
            "CI integration",
            errors,
        )

    return errors


def mutated_document(
    documents: dict[str, str], relative: str, old: str, new: str
) -> dict[str, str] | None:
    text = documents.get(relative, "")
    if old not in text:
        return None
    mutated = dict(documents)
    mutated[relative] = text.replace(old, new, 1)
    return mutated


def validate_negative_fixtures(documents: dict[str, str]) -> list[str]:
    fixtures = (
        (
            "canonical-mode",
            "skills/execution-plan-manager/SKILL.md",
            "- `analyze`:",
            "- `inspect`:",
            "canonical modes",
        ),
        (
            "analysis-write-boundary",
            "common/planning-analysis-rules.md",
            "repeatable, read-only pass",
            "repeatable analysis pass",
            "analysis contract",
        ),
        (
            "append-only-convergence",
            "common/convergence-rules.md",
            "append exactly one new section",
            "rewrite one section",
            "append-only convergence",
        ),
        (
            "clean-convergence",
            "skills/execution-plan-manager/SKILL.md",
            "with zero findings, preserve it byte-for-byte",
            "with zero findings, record success",
            "byte-identical clean convergence",
        ),
        (
            "current-request-precedence",
            "common/convergence-rules.md",
            "current user request changed",
            "saved plan changed",
            "current-user precedence",
        ),
        (
            "clarification-limit",
            "common/goal-contract.md",
            "no more than three",
            "no more than four",
            "clarification limit",
        ),
        (
            "reviewer-mutation",
            "skills/frontend-quality-reviewer/SKILL.md",
            "Must not add, remove, reorder, renumber, or mark execution-plan slices",
            "May add or mark execution-plan slices",
            "reviewer alignment",
        ),
        (
            "coverage-template",
            "templates/execution-plan.md",
            "Coverage:",
            "Status Summary:",
            "execution template contract",
        ),
        (
            "checkpoint-resume",
            "common/checkpoint-rules.md",
            "next `S-###` slice",
            "next task",
            "checkpoint alignment",
        ),
        (
            "CI-gate",
            ".github/workflows/skill-pack-ci.yml",
            "validate_planning_integrity.py",
            "validate_skill_evals.py",
            "CI integration",
        ),
    )
    errors: list[str] = []
    for name, relative, old, new, expected_error in fixtures:
        mutated = mutated_document(documents, relative, old, new)
        if mutated is None:
            errors.append(f"negative fixture {name}: source text is missing")
            continue
        fixture_errors = validate_documents(mutated)
        if not any(expected_error in error for error in fixture_errors):
            errors.append(
                f"negative fixture {name}: validator did not report {expected_error}"
            )

    planning_suite = json.loads(documents["evals/planning-workflow-evals.json"])
    planning_suite["cases"] = planning_suite["cases"][:-1]
    mutated = dict(documents)
    mutated["evals/planning-workflow-evals.json"] = json.dumps(planning_suite)
    if not any("planning eval suite" in error for error in validate_documents(mutated)):
        errors.append("negative fixture planning-evals: missing case was accepted")

    manifest = json.loads(documents["bundle-manifest.json"])
    manifest["skills"].append("spec-driven-feature-manager")
    mutated = dict(documents)
    mutated["bundle-manifest.json"] = json.dumps(manifest)
    if not any("skill inventory" in error for error in validate_documents(mutated)):
        errors.append("negative fixture skill-inventory: twentieth skill was accepted")

    return errors


def validate() -> list[str]:
    documents, errors = load_documents()
    if errors:
        return errors

    errors.extend(validate_documents(documents))
    skill_directories = sorted(
        path.name for path in (ROOT / "skills").iterdir() if path.is_dir()
    )
    if len(skill_directories) != 19:
        errors.append("skill inventory: source skills directory must contain 19 skills")
    if "spec-driven-feature-manager" in skill_directories:
        errors.append("skill inventory: forbidden twentieth planning skill exists")

    if not errors:
        errors.extend(validate_negative_fixtures(documents))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validate deterministic planning integrity contracts and drift guards."
        )
    )
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Planning integrity contracts and negative fixtures are valid.")


if __name__ == "__main__":
    main()
