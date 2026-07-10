#!/usr/bin/env python3

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPT_DIR = ROOT / "skills" / "agent-rules-skill-author" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPT_DIR))

from skill_common import load_openai_yaml  # noqa: E402

CAPABILITY_LIST_KEYS = (
    "requires",
    "requires_when_in_scope",
    "optional",
    "blocked",
)
PROVIDER_LIST_KEYS = (
    "preferred_providers",
    "fallback_providers",
    "blocked_providers",
)
VALID_EVIDENCE = {
    "current_session_tool_registry",
    "direct_user_confirmation",
    "validated_project_profile",
}
FORBIDDEN_PROVIDER_DEPENDENCIES = {
    "context7",
    "filesystem_server",
    "mdn",
    "openaiDeveloperDocs",
    "openai_developer_docs_mcp",
    "playwright",
}
OPENAI_DOCS_CAPABILITY = "openai_platform_docs"
OPENAI_DOCS_PROVIDER = "openai_developer_docs_mcp"
OPENAI_DOCS_FALLBACK = "official_openai_web_docs"
OPENAI_DOCS_SCOPED_SKILLS = {
    "agent-rules-skill-author",
    "frontend-architecture-planner",
    "frontend-bugfix-debugger",
    "frontend-layout-implementer",
    "frontend-quality-reviewer",
    "frontend-refactor-surgeon",
    "greenfield-project-builder",
    "mcp-toolchain-manager",
    "pattern-library-manager",
    "project-context-adapter",
    "project-onboarding-adapter",
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_sorted_unique(label, values, errors):
    if values != sorted(values):
        errors.append(f"{label}: values must be sorted alphabetically")
    if len(values) != len(set(values)):
        errors.append(f"{label}: values must be unique")


def validate():
    errors = []
    try:
        manifest = load_json(ROOT / "tool-capabilities-manifest.json")
        bundle = load_json(ROOT / "bundle-manifest.json")
    except Exception as exc:
        return [f"tool capability metadata cannot be parsed: {exc}"]

    if manifest.get("version") != bundle.get("version"):
        errors.append(
            "tool-capabilities-manifest.json: version must match bundle-manifest.json"
        )

    capabilities = manifest.get("capabilities", {})
    skills = manifest.get("skills", {})
    expected_skills = bundle.get("skills", [])

    if list(capabilities) != sorted(capabilities):
        errors.append(
            "tool-capabilities-manifest.json: capabilities must be sorted alphabetically"
        )
    if list(skills) != sorted(skills):
        errors.append(
            "tool-capabilities-manifest.json: skills must be sorted alphabetically"
        )
    if set(skills) != set(expected_skills):
        missing = sorted(set(expected_skills) - set(skills))
        extra = sorted(set(skills) - set(expected_skills))
        errors.append(
            "tool-capabilities-manifest.json: skill map must match bundle inventory; "
            f"missing={missing}, extra={extra}"
        )

    capability_names = set(capabilities)
    if "codex_platform_docs" in capabilities:
        errors.append(
            "tool-capabilities-manifest.json: use openai_platform_docs for the "
            "official OpenAI documentation surface"
        )

    openai_docs = capabilities.get(OPENAI_DOCS_CAPABILITY)
    if not isinstance(openai_docs, dict):
        errors.append(
            "tool-capabilities-manifest.json: openai_platform_docs is required"
        )
    else:
        if OPENAI_DOCS_PROVIDER not in openai_docs.get("preferred_providers", []):
            errors.append(
                "tool-capabilities-manifest.json: openai_platform_docs must prefer "
                "openai_developer_docs_mcp"
            )
        if OPENAI_DOCS_FALLBACK not in openai_docs.get("fallback_providers", []):
            errors.append(
                "tool-capabilities-manifest.json: openai_platform_docs must fall back "
                "to official_openai_web_docs"
            )

    for name, capability in capabilities.items():
        label = f"tool-capabilities-manifest.json: capabilities.{name}"
        evidence = capability.get("availability_evidence", [])
        validate_sorted_unique(f"{label}.availability_evidence", evidence, errors)
        unknown_evidence = sorted(set(evidence) - VALID_EVIDENCE)
        if unknown_evidence:
            errors.append(f"{label}: unknown availability evidence {unknown_evidence}")
        if "current_session_tool_registry" not in evidence:
            errors.append(
                f"{label}: current session tool registry must be accepted as evidence"
            )
        if "direct_user_confirmation" in evidence and name != "design_reference_files":
            errors.append(
                f"{label}: direct user confirmation is limited to user-supplied design references"
            )

        provider_sets = []
        for key in PROVIDER_LIST_KEYS:
            values = capability.get(key, [])
            validate_sorted_unique(f"{label}.{key}", values, errors)
            provider_sets.append((key, set(values)))
        for index, (left_name, left) in enumerate(provider_sets):
            for right_name, right in provider_sets[index + 1 :]:
                overlap = sorted(left & right)
                if overlap:
                    errors.append(
                        f"{label}: {left_name} and {right_name} overlap: {overlap}"
                    )

    for skill_name, declaration in skills.items():
        label = f"tool-capabilities-manifest.json: skills.{skill_name}"
        declared_sets = []
        for key in CAPABILITY_LIST_KEYS:
            values = declaration.get(key, [])
            validate_sorted_unique(f"{label}.{key}", values, errors)
            unknown = sorted(set(values) - capability_names)
            if unknown:
                errors.append(f"{label}.{key}: unknown capabilities {unknown}")
            declared_sets.append((key, set(values)))
        for index, (left_name, left) in enumerate(declared_sets):
            for right_name, right in declared_sets[index + 1 :]:
                overlap = sorted(left & right)
                if overlap:
                    errors.append(
                        f"{label}: {left_name} and {right_name} overlap: {overlap}"
                    )

    for skill_name in sorted(OPENAI_DOCS_SCOPED_SKILLS):
        scoped = skills.get(skill_name, {}).get("requires_when_in_scope", [])
        if OPENAI_DOCS_CAPABILITY not in scoped:
            errors.append(
                "tool-capabilities-manifest.json: "
                f"skills.{skill_name}.requires_when_in_scope must include "
                "openai_platform_docs"
            )

    for skill_name in expected_skills:
        skill_dir = ROOT / "skills" / skill_name
        try:
            metadata, _ = load_openai_yaml(skill_dir)
        except Exception as exc:
            errors.append(
                f"skills/{skill_name}/agents/openai.yaml: cannot parse metadata: {exc}"
            )
            continue
        tools = metadata.get("dependencies", {}).get("tools", [])
        if tools:
            names = sorted(
                str(item.get("value", item.get("name", "")))
                if isinstance(item, dict)
                else str(item)
                for item in tools
            )
            errors.append(
                f"skills/{skill_name}/agents/openai.yaml: this bundle has no hard provider dependencies; found {names}"
            )
        serialized = json.dumps(metadata, sort_keys=True)
        found = sorted(
            name for name in FORBIDDEN_PROVIDER_DEPENDENCIES if name in serialized
        )
        if found:
            errors.append(
                f"skills/{skill_name}/agents/openai.yaml: optional providers must stay out of client UI metadata: {found}"
            )

    return errors


def main():
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Tool capability metadata is complete and client-neutral.")


if __name__ == "__main__":
    main()
