#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "common" / "token-economy-rules.md"
OUTPUT_EVALS_PATH = ROOT / "evals" / "output-evals.json"
OUTPUT_MARKER = (
    "Final response: return only facts that affect the user's understanding, "
    "confidence, or next action. Omit empty fields and workflow narration."
)
OUTPUT_WORD_LIMITS = {
    "Fast Lookup": 120,
    "Lightweight Workflow": 180,
    "Standard Workflow": 240,
    "Deep Workflow": 320,
}
COMMON_BOILERPLATE = {
    "repeat or paraphrase the user request",
    "name selected skills or internal workflow",
    "include raw or long command logs",
}
OUTPUT_CASE_FIELDS = {
    "id",
    "prompt",
    "skill",
    "workflow_level",
    "required_facts",
    "forbidden_boilerplate",
    "max_words",
    "must_report_verification",
    "reason",
}


def output_contract(text):
    match = re.search(
        r"^## Output Contract\s*$([\s\S]*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE,
    )
    return match.group(1) if match else ""


def validate():
    errors = []
    if not POLICY_PATH.is_file():
        return ["common/token-economy-rules.md is required"]

    policy = POLICY_PATH.read_text(encoding="utf-8-sig")
    for phrase in (
        "Return only facts that affect the user's understanding, confidence, or next action.",
        "`Lightweight Workflow`: at most 180 words.",
        "Verification must remain visible",
        "Word limits never authorize hiding a blocker",
    ):
        if phrase not in policy:
            errors.append(f"token economy policy is missing: {phrase}")

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8-sig")
    core = (ROOT / "common" / "core" / "runtime-core-policy.md").read_text(
        encoding="utf-8-sig"
    )
    for label, text in (("AGENTS.md", agents), ("portable core", core)):
        if "common/token-economy-rules.md" not in text:
            errors.append(f"{label} must route output through token economy policy")
        for phrase in ("Changed", "Verified", "Blocked"):
            if phrase not in text:
                errors.append(f"{label} is missing default output field {phrase}")

    manifest = json.loads((ROOT / "bundle-manifest.json").read_text(encoding="utf-8"))
    for skill_name in manifest.get("skills", []):
        path = ROOT / "skills" / skill_name / "SKILL.md"
        contract = output_contract(path.read_text(encoding="utf-8-sig"))
        if not contract:
            errors.append(f"skills/{skill_name}/SKILL.md has no Output Contract")
        elif contract.count(OUTPUT_MARKER) != 1:
            errors.append(
                f"skills/{skill_name}/SKILL.md must contain the fact-only final response marker once"
            )

    try:
        suite = json.loads(OUTPUT_EVALS_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        return [*errors, f"Cannot read evals/output-evals.json: {exc}"]

    for index, case in enumerate(suite.get("cases", [])):
        label = f"evals/output-evals.json: cases[{index}]"
        fields = set(case)
        if fields != OUTPUT_CASE_FIELDS:
            errors.append(
                f"{label}: output fields must be {sorted(OUTPUT_CASE_FIELDS)}, got {sorted(fields)}"
            )
        level = case.get("workflow_level")
        limit = OUTPUT_WORD_LIMITS.get(level)
        max_words = case.get("max_words")
        if limit is None or not isinstance(max_words, int) or max_words > limit:
            errors.append(f"{label}: invalid word budget for {level}")
        if case.get("must_report_verification") is not True:
            errors.append(f"{label}: verification cannot be hidden")
        missing = sorted(
            COMMON_BOILERPLATE - set(case.get("forbidden_boilerplate", []))
        )
        if missing:
            errors.append(f"{label}: missing boilerplate controls {missing}")
        facts = case.get("required_facts", [])
        if not any(
            any(term in fact.lower() for term in ("verif", "valid", "evidence"))
            for fact in facts
        ):
            errors.append(f"{label}: verification evidence is not a required fact")

    return errors


def main():
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Output economy policy and eval budgets are valid.")


if __name__ == "__main__":
    main()
