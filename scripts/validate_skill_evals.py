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
POLICY_CONFLICT_EVALS = EVAL_DIR / "policy-conflict-evals.json"
README_POLICY_EVALS = EVAL_DIR / "readme-policy-evals.json"
TEST_POLICY_EVALS = EVAL_DIR / "test-policy-evals.json"
TOOL_CAPABILITY_EVALS = EVAL_DIR / "tool-capability-evals.json"
CROSS_MODEL_EVALS = EVAL_DIR / "cross-model-evals.json"
WORKFLOW_LEVELS = {
    "Fast Lookup",
    "Lightweight Workflow",
    "Standard Workflow",
    "Deep Workflow",
}
POLICY_PRECEDENCE = (
    "system-client-security-sandbox",
    "current-user-request",
    "confirmed-scope-approvals",
    "host-project-instructions",
    "verified-project-facts",
    "selected-skill-workflow",
    "active-frontend-profile",
    "generic-kit-defaults",
)
README_EXPECTATIONS = {
    "read-explain": (True, False),
    "verify-commands": (True, False),
    "drift-audit": (True, False),
    "project-onboarding": (True, False),
    "unrelated-code-change": (False, False),
    "explicit-readme-edit": (True, True),
}
TEST_EXPECTATIONS = {
    "css-only-change": (False, False, False, False, "omit-test-line"),
    "run-existing-test": (True, False, False, False, "report-command-result"),
    "update-existing-contract-test": (
        True,
        True,
        False,
        False,
        "report-changes-and-result",
    ),
    "explicit-regression-test": (
        True,
        False,
        True,
        False,
        "report-changes-and-result",
    ),
    "unapproved-infrastructure": (False, False, False, False, "request-approval"),
    "unrelated-full-suite": (False, False, False, False, "omit-test-line"),
    "propose-regression-test": (
        False,
        False,
        False,
        False,
        "report-material-gap",
    ),
    "fix-existing-tests": (
        True,
        True,
        False,
        False,
        "report-changes-and-result",
    ),
}
CAPABILITY_EXPECTATIONS = {
    "native-provider": ("available", False),
    "missing-optional": ("fallback-used", False),
    "missing-required": ("blocked", False),
    "false-proof": ("unknown", False),
    "install-request": ("missing", False),
    "client-parity": ("available", False),
    "lightweight-no-audit": ("not-needed", False),
}
OUTPUT_WORD_LIMITS = {
    "Fast Lookup": 120,
    "Lightweight Workflow": 180,
    "Standard Workflow": 240,
    "Deep Workflow": 320,
}
REQUIRED_OUTPUT_BOILERPLATE_CONTROLS = {
    "repeat or paraphrase the user request",
    "name selected skills or internal workflow",
    "include raw or long command logs",
}
CROSS_MODEL_FAMILIES = {"gpt", "claude"}
CROSS_MODEL_CLIENTS = {"codex", "claude-code"}
CROSS_MODEL_DIMENSIONS = {
    "routing",
    "context-economy",
    "readme-boundary",
    "test-boundary",
    "policy-precedence",
    "capability-resolution",
    "verification-evidence",
    "output-economy",
    "onboarding",
    "scope-control",
}
CLIENT_TERMS = ("codex", "claude", ".agents", ".claude-plugin")


def load_actual_skills(errors):
    manifest_path = ROOT / "bundle-manifest.json"
    try:
        manifest = load_json(manifest_path)
    except Exception as exc:
        errors.append(f"bundle-manifest.json: cannot parse skill inventory: {exc}")
        return set()

    skills = manifest.get("skills")
    if not isinstance(skills, list):
        errors.append(
            "bundle-manifest.json: skills must be a list before eval validation"
        )
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
        (
            "workflow_level",
            "expected_primary_skill",
            "should_trigger",
            "should_not_trigger",
            "reason",
        ),
        errors,
    )

    workflow_level = case.get("workflow_level")
    if workflow_level not in WORKFLOW_LEVELS:
        errors.append(
            f"{label}: workflow_level must be one of {', '.join(sorted(WORKFLOW_LEVELS))}"
        )

    expected_primary = case.get("expected_primary_skill")
    if expected_primary and expected_primary not in actual_skills:
        errors.append(f"{label}: expected_primary_skill is unknown: {expected_primary}")

    should_trigger = case.get("should_trigger", [])
    should_not_trigger = case.get("should_not_trigger", [])
    validate_skill_list(label, "should_trigger", should_trigger, actual_skills, errors)
    validate_skill_list(
        label, "should_not_trigger", should_not_trigger, actual_skills, errors
    )

    if (
        expected_primary
        and isinstance(should_trigger, list)
        and expected_primary not in should_trigger
    ):
        errors.append(
            f"{label}: expected_primary_skill must be included in should_trigger"
        )

    if isinstance(should_trigger, list) and isinstance(should_not_trigger, list):
        overlap = sorted(set(should_trigger) & set(should_not_trigger))
        if overlap:
            errors.append(
                f"{label}: should_trigger and should_not_trigger overlap: {', '.join(overlap)}"
            )


def validate_output_case(label, case, actual_skills, errors):
    require_case_keys(
        label,
        case,
        (
            "skill",
            "workflow_level",
            "required_facts",
            "forbidden_boilerplate",
            "max_words",
            "must_report_verification",
            "reason",
        ),
        errors,
    )

    skill = case.get("skill")
    if skill and skill not in actual_skills:
        errors.append(f"{label}: skill is unknown: {skill}")

    if "required_output_sections" in case:
        errors.append(f"{label}: required_output_sections is obsolete")

    required_facts = case.get("required_facts", [])
    if not isinstance(required_facts, list) or len(required_facts) < 3:
        errors.append(f"{label}: required_facts should define at least 3 facts")

    boilerplate = case.get("forbidden_boilerplate", [])
    if not isinstance(boilerplate, list):
        errors.append(f"{label}: forbidden_boilerplate must be a list")
    else:
        missing = sorted(REQUIRED_OUTPUT_BOILERPLATE_CONTROLS - set(boilerplate))
        if missing:
            errors.append(f"{label}: missing boilerplate controls: {missing}")

    workflow_level = case.get("workflow_level")
    max_words = case.get("max_words")
    allowed_words = OUTPUT_WORD_LIMITS.get(workflow_level)
    if allowed_words is not None and (
        not isinstance(max_words, int) or max_words > allowed_words
    ):
        errors.append(
            f"{label}: max_words must be at most {allowed_words} for {workflow_level}"
        )

    if case.get("must_report_verification") is not True:
        errors.append(f"{label}: output eval must keep verification visible")
    elif isinstance(required_facts, list) and not any(
        any(term in fact.lower() for term in ("verif", "valid", "evidence"))
        for fact in required_facts
    ):
        errors.append(f"{label}: required_facts must include verification evidence")


def validate_policy_conflict_case(label, case, errors):
    require_case_keys(
        label,
        case,
        (
            "conflict_sources",
            "expected_precedence",
            "expected_behavior",
            "forbidden_behaviors",
            "reason",
        ),
        errors,
    )

    sources = case.get("conflict_sources", [])
    if not isinstance(sources, list) or len(sources) < 2:
        errors.append(f"{label}: conflict_sources must contain at least 2 levels")
        return
    unknown = [source for source in sources if source not in POLICY_PRECEDENCE]
    if unknown:
        errors.append(
            f"{label}: conflict_sources contains unknown levels: {', '.join(unknown)}"
        )
        return

    expected = case.get("expected_precedence")
    actual = min(sources, key=POLICY_PRECEDENCE.index)
    if expected != actual:
        errors.append(
            f"{label}: expected_precedence must be highest listed level {actual!r}"
        )

    forbidden = case.get("forbidden_behaviors", [])
    if not isinstance(forbidden, list) or len(forbidden) < 2:
        errors.append(f"{label}: forbidden_behaviors should define at least 2 controls")


def validate_readme_policy_case(label, case, errors):
    require_case_keys(
        label,
        case,
        (
            "readme_action",
            "expected_read",
            "expected_edit",
            "required_evidence",
            "expected_behavior",
            "forbidden_behaviors",
            "reason",
        ),
        errors,
    )

    action = case.get("readme_action")
    if action not in README_EXPECTATIONS:
        errors.append(f"{label}: unknown readme_action {action!r}")
        return
    expected_read, expected_edit = README_EXPECTATIONS[action]
    if case.get("expected_read") is not expected_read:
        errors.append(f"{label}: expected_read must be {expected_read} for {action}")
    if case.get("expected_edit") is not expected_edit:
        errors.append(f"{label}: expected_edit must be {expected_edit} for {action}")

    evidence = case.get("required_evidence", [])
    if not isinstance(evidence, list) or not evidence:
        errors.append(f"{label}: required_evidence must be a non-empty list")
    elif expected_read and "readme" not in evidence:
        errors.append(f"{label}: README-reading cases must include readme evidence")

    if action in {"verify-commands", "drift-audit", "project-onboarding"}:
        higher_evidence = {
            "runtime-result",
            "source-code",
            "config",
            "ci",
            "package-scripts",
            "lockfile",
        }
        if not higher_evidence.intersection(evidence):
            errors.append(f"{label}: README claim needs higher technical evidence")

    forbidden = case.get("forbidden_behaviors", [])
    if not isinstance(forbidden, list) or len(forbidden) < 2:
        errors.append(f"{label}: forbidden_behaviors should define at least 2 controls")


def validate_test_policy_case(label, case, errors):
    require_case_keys(
        label,
        case,
        (
            "test_action",
            "expected_run_existing",
            "expected_edit_existing",
            "expected_create_new",
            "expected_change_infrastructure",
            "expected_reporting",
            "expected_behavior",
            "forbidden_behaviors",
            "reason",
        ),
        errors,
    )

    action = case.get("test_action")
    if action not in TEST_EXPECTATIONS:
        errors.append(f"{label}: unknown test_action {action!r}")
        return

    expected = TEST_EXPECTATIONS[action]
    actual = (
        case.get("expected_run_existing"),
        case.get("expected_edit_existing"),
        case.get("expected_create_new"),
        case.get("expected_change_infrastructure"),
        case.get("expected_reporting"),
    )
    if actual != expected:
        errors.append(f"{label}: test-policy expectation must be {expected!r}")

    if actual[3] and not actual[2]:
        errors.append(
            f"{label}: infrastructure change cannot be implied without authorized test work"
        )

    forbidden = case.get("forbidden_behaviors", [])
    if not isinstance(forbidden, list) or len(forbidden) < 2:
        errors.append(f"{label}: forbidden_behaviors should define at least 2 controls")


def validate_tool_capability_case(label, case, capability_names, errors):
    require_case_keys(
        label,
        case,
        (
            "capability_action",
            "required_capabilities",
            "available_providers",
            "expected_status",
            "expected_install",
            "expected_behavior",
            "forbidden_behaviors",
            "reason",
        ),
        errors,
    )

    action = case.get("capability_action")
    if action not in CAPABILITY_EXPECTATIONS:
        errors.append(f"{label}: unknown capability_action {action!r}")
        return

    expected = CAPABILITY_EXPECTATIONS[action]
    actual = (case.get("expected_status"), case.get("expected_install"))
    if actual != expected:
        errors.append(f"{label}: capability expectation must be {expected!r}")

    required = case.get("required_capabilities", [])
    if not isinstance(required, list) or not required:
        errors.append(f"{label}: required_capabilities must be a non-empty list")
    else:
        unknown = sorted(set(required) - capability_names)
        if unknown:
            errors.append(f"{label}: unknown capabilities {unknown}")

    providers = case.get("available_providers", [])
    if not isinstance(providers, list):
        errors.append(f"{label}: available_providers must be a list")
    elif action in {"native-provider", "client-parity"} and not providers:
        errors.append(f"{label}: available provider evidence is required for {action}")

    forbidden = case.get("forbidden_behaviors", [])
    if not isinstance(forbidden, list) or len(forbidden) < 2:
        errors.append(f"{label}: forbidden_behaviors should define at least 2 controls")


def validate_cross_model_case(label, case, actual_skills, errors):
    require_case_keys(
        label,
        case,
        (
            "parity_dimension",
            "model_families",
            "client_targets",
            "workflow_level",
            "portable_expectation",
            "client_expectations",
            "required_facts",
            "forbidden_behaviors",
            "max_words",
            "reason",
        ),
        errors,
    )

    if set(case.get("model_families", [])) != CROSS_MODEL_FAMILIES:
        errors.append(f"{label}: model_families must cover gpt and claude")
    if set(case.get("client_targets", [])) != CROSS_MODEL_CLIENTS:
        errors.append(f"{label}: client_targets must cover codex and claude-code")

    primary = case.get("expected_primary_skill")
    if primary is not None and primary not in actual_skills:
        errors.append(f"{label}: expected_primary_skill is unknown: {primary}")

    workflow_level = case.get("workflow_level")
    max_words = case.get("max_words")
    allowed_words = OUTPUT_WORD_LIMITS.get(workflow_level)
    if allowed_words is not None and (
        not isinstance(max_words, int) or max_words > allowed_words
    ):
        errors.append(
            f"{label}: max_words must be at most {allowed_words} for {workflow_level}"
        )

    expectation = case.get("portable_expectation", "")
    if isinstance(expectation, str):
        found_terms = [term for term in CLIENT_TERMS if term in expectation.lower()]
        if found_terms:
            errors.append(
                f"{label}: portable_expectation contains client-specific terms: "
                f"{', '.join(found_terms)}"
            )

    client_expectations = case.get("client_expectations", {})
    if not isinstance(client_expectations, dict) or set(client_expectations) != (
        CROSS_MODEL_CLIENTS
    ):
        errors.append(f"{label}: client_expectations must define both clients only")

    facts = case.get("required_facts", [])
    if not isinstance(facts, list) or len(facts) < 2:
        errors.append(f"{label}: required_facts should define at least 2 facts")

    forbidden = case.get("forbidden_behaviors", [])
    if not isinstance(forbidden, list) or len(forbidden) < 2:
        errors.append(f"{label}: forbidden_behaviors should define at least 2 controls")


def validate_suite(
    path,
    expected_type,
    suite_schema,
    case_schema,
    actual_skills,
    capability_names,
    seen_ids,
    errors,
):
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
    if expected_type == "policy-conflict" and len(cases) < 5:
        errors.append(f"{relative}: policy-conflict suite needs at least 5 cases")
    if expected_type == "readme-policy" and len(cases) < 5:
        errors.append(f"{relative}: readme-policy suite needs at least 5 cases")
    if expected_type == "test-policy" and len(cases) < 6:
        errors.append(f"{relative}: test-policy suite needs at least 6 cases")
    if expected_type == "tool-capability" and len(cases) < 7:
        errors.append(f"{relative}: tool-capability suite needs at least 7 cases")
    if expected_type == "cross-model" and len(cases) < 10:
        errors.append(f"{relative}: cross-model suite needs at least 10 cases")
    if expected_type == "cross-model":
        dimensions = {
            case.get("parity_dimension") for case in cases if isinstance(case, dict)
        }
        missing_dimensions = sorted(CROSS_MODEL_DIMENSIONS - dimensions)
        if missing_dimensions:
            errors.append(
                f"{relative}: missing parity dimensions: {missing_dimensions}"
            )

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
        elif expected_type == "policy-conflict":
            validate_policy_conflict_case(label, case, errors)
        elif expected_type == "readme-policy":
            validate_readme_policy_case(label, case, errors)
        elif expected_type == "test-policy":
            validate_test_policy_case(label, case, errors)
        elif expected_type == "tool-capability":
            validate_tool_capability_case(label, case, capability_names, errors)
        elif expected_type == "cross-model":
            validate_cross_model_case(label, case, actual_skills, errors)


def validate():
    errors = []
    actual_skills = load_actual_skills(errors)
    try:
        capability_names = set(
            load_json(ROOT / "tool-capabilities-manifest.json").get("capabilities", {})
        )
    except Exception as exc:
        errors.append(f"tool-capabilities-manifest.json: cannot parse: {exc}")
        capability_names = set()

    try:
        suite_schema = load_json(schema_path("eval-suite"))
        case_schema = load_json(schema_path("eval-case"))
    except Exception as exc:
        return [f"schemas: cannot load eval schema files: {exc}"]

    seen_ids = set()
    validate_suite(
        TRIGGER_EVALS,
        "skill-trigger",
        suite_schema,
        case_schema,
        actual_skills,
        capability_names,
        seen_ids,
        errors,
    )
    validate_suite(
        OUTPUT_EVALS,
        "skill-output",
        suite_schema,
        case_schema,
        actual_skills,
        capability_names,
        seen_ids,
        errors,
    )
    validate_suite(
        POLICY_CONFLICT_EVALS,
        "policy-conflict",
        suite_schema,
        case_schema,
        actual_skills,
        capability_names,
        seen_ids,
        errors,
    )
    validate_suite(
        README_POLICY_EVALS,
        "readme-policy",
        suite_schema,
        case_schema,
        actual_skills,
        capability_names,
        seen_ids,
        errors,
    )
    validate_suite(
        TEST_POLICY_EVALS,
        "test-policy",
        suite_schema,
        case_schema,
        actual_skills,
        capability_names,
        seen_ids,
        errors,
    )
    validate_suite(
        TOOL_CAPABILITY_EVALS,
        "tool-capability",
        suite_schema,
        case_schema,
        actual_skills,
        capability_names,
        seen_ids,
        errors,
    )
    validate_suite(
        CROSS_MODEL_EVALS,
        "cross-model",
        suite_schema,
        case_schema,
        actual_skills,
        capability_names,
        seen_ids,
        errors,
    )
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate skill trigger and output eval fixtures."
    )
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Skill eval fixtures are valid.")


if __name__ == "__main__":
    main()
