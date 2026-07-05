#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

from validate_schemas import load_json, schema_path, validate_instance


ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = ROOT / "evals"
TRIGGER_EVALS = EVAL_DIR / "trigger-evals.json"
OUTPUT_EVALS = EVAL_DIR / "output-evals.json"
WORKFLOW_LEVELS = {"Fast Lookup", "Lightweight Workflow", "Standard Workflow", "Deep Workflow"}


def load_actual_skills(errors):
    manifest_path = ROOT / "bundle-manifest.json"
    try:
        manifest = load_json(manifest_path)
    except Exception as exc:
        errors.append(f"bundle-manifest.json: cannot parse skill inventory: {exc}")
        return set()

    skills = manifest.get("skills")
    if not isinstance(skills, list):
        errors.append("bundle-manifest.json: skills must be a list before eval validation")
        return set()

    return set(skills)


def load_eval_file(path, errors):
    if not path.exists():
        errors.append(f"{path.relative_to(ROOT).as_posix()}: file is required")
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT).as_posix()}: cannot parse JSON: {exc}")
        return None


def validate_with_schema(label, value, schema, errors):
    for error in validate_instance(value, schema):
        errors.append(f"{label}: {error}")


def require_case_keys(label, case, keys, errors):
    for key in keys:
        if key not in case:
            errors.append(f"{label}: missing required eval field {key!r}")


def validate_skill_list(label, key, values, actual_skills, errors):
    if values is None:
        return
    if not isinstance(values, list):
        errors.append(f"{label}: {key} must be a list")
        return
    for value in values:
        if value not in actual_skills:
            errors.append(f"{label}: {key} contains unknown skill {value!r}")


def validate_trigger_case(label, case, actual_skills, errors):
    require_case_keys(
        label,
        case,
        ("workflow_level", "expected_primary_skill", "should_trigger", "should_not_trigger", "reason"),
        errors,
    )

    workflow_level = case.get("workflow_level")
    if workflow_level not in WORKFLOW_LEVELS:
        errors.append(f"{label}: workflow_level must be one of {', '.join(sorted(WORKFLOW_LEVELS))}")

    expected_primary = case.get("expected_primary_skill")
    if expected_primary and expected_primary not in actual_skills:
        errors.append(f"{label}: expected_primary_skill is unknown: {expected_primary}")

    should_trigger = case.get("should_trigger", [])
    should_not_trigger = case.get("should_not_trigger", [])
    validate_skill_list(label, "should_trigger", should_trigger, actual_skills, errors)
    validate_skill_list(label, "should_not_trigger", should_not_trigger, actual_skills, errors)

    if expected_primary and isinstance(should_trigger, list) and expected_primary not in should_trigger:
        errors.append(f"{label}: expected_primary_skill must be included in should_trigger")

    if isinstance(should_trigger, list) and isinstance(should_not_trigger, list):
        overlap = sorted(set(should_trigger) & set(should_not_trigger))
        if overlap:
            errors.append(f"{label}: should_trigger and should_not_trigger overlap: {', '.join(overlap)}")


def validate_output_case(label, case, actual_skills, errors):
    require_case_keys(label, case, ("skill", "required_output_sections", "forbidden_behaviors", "reason"), errors)

    skill = case.get("skill")
    if skill and skill not in actual_skills:
        errors.append(f"{label}: skill is unknown: {skill}")

    required_sections = case.get("required_output_sections", [])
    if isinstance(required_sections, list) and len(required_sections) < 3:
        errors.append(f"{label}: required_output_sections should define at least 3 sections")

    forbidden = case.get("forbidden_behaviors", [])
    if isinstance(forbidden, list) and len(forbidden) < 2:
        errors.append(f"{label}: forbidden_behaviors should define at least 2 controls")


def validate_suite(path, expected_type, suite_schema, case_schema, actual_skills, seen_ids, errors):
    suite = load_eval_file(path, errors)
    if suite is None:
        return

    relative = path.relative_to(ROOT).as_posix()
    validate_with_schema(relative, suite, suite_schema, errors)

    eval_type = suite.get("eval_type")
    if eval_type != expected_type:
        errors.append(f"{relative}: eval_type must be {expected_type!r}")

    cases = suite.get("cases", [])
    if not isinstance(cases, list):
        errors.append(f"{relative}: cases must be a list")
        return

    for index, case in enumerate(cases):
        label = f"{relative}: cases[{index}]"
        validate_with_schema(label, case, case_schema, errors)

        case_id = case.get("id")
        if case_id in seen_ids:
            errors.append(f"{label}: duplicate eval id {case_id}")
        elif case_id:
            seen_ids.add(case_id)

        prompt = case.get("prompt")
        if isinstance(prompt, str) and not prompt.strip():
            errors.append(f"{label}: prompt must not be blank")

        if expected_type == "skill-trigger":
            validate_trigger_case(label, case, actual_skills, errors)
        elif expected_type == "skill-output":
            validate_output_case(label, case, actual_skills, errors)


def validate():
    errors = []
    actual_skills = load_actual_skills(errors)

    try:
        suite_schema = load_json(schema_path("eval-suite"))
        case_schema = load_json(schema_path("eval-case"))
    except Exception as exc:
        return [f"schemas: cannot load eval schema files: {exc}"]

    seen_ids = set()
    validate_suite(TRIGGER_EVALS, "skill-trigger", suite_schema, case_schema, actual_skills, seen_ids, errors)
    validate_suite(OUTPUT_EVALS, "skill-output", suite_schema, case_schema, actual_skills, seen_ids, errors)
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate skill trigger and output eval fixtures.")
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Skill eval fixtures are valid.")


if __name__ == "__main__":
    main()
