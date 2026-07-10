#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS_BODY_LIMIT = 750
CORE_BODY_LIMIT = 350
PROFILE_BODY_LIMIT = 300
ADAPTER_BODY_LIMIT = 180
SKILL_DESCRIPTION_LIMIT = 45
SKILL_DESCRIPTION_TOTAL_LIMIT = 550
CLAUDE_RUNTIME_PRELUDE = (
    "Apply `common/core/runtime-core-policy.md`, evidence-gated "
    "`profiles/react-typescript/PROFILE.md`, and `adapters/claude-code.md`."
)
REQUIRED_AGENTS_HEADINGS = (
    "Purpose",
    "Precedence And Approvals",
    "Context Loading And Workflow Scale",
    "Skill Discovery",
    "Compact Skill Index",
    "Change Boundaries",
    "Verification And Output",
)
REMOVED_AGENTS_HEADINGS = (
    "Target Stack",
    "Runtime Source Model",
    "README Read And Edit Boundary",
    "Natural Language Commands",
    "Prompt Intake And Task Classification",
    "Prompt Intent And Task Scale Gate",
    "Figma Boundary",
    "Tool Policy",
    "Frontend Implementation Rules",
    "Documentation Rules",
)
GRAPH_FRONTMATTER_KEYS = {
    "id",
    "title",
    "doc_type",
    "layer",
    "status",
    "publishable",
    "local_only",
    "tags",
    "parent",
    "related",
    "depends_on",
}


def split_frontmatter(text):
    normalized = text.replace("\r\n", "\n").lstrip("\ufeff")
    if not normalized.startswith("---\n"):
        return None, normalized
    end = normalized.find("\n---\n", 4)
    if end == -1:
        return None, normalized
    return normalized[4:end], normalized[end + 5 :]


def frontmatter_values(raw):
    values = {}
    if raw is None:
        return values
    for line in raw.splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def word_count(text):
    return len(text.split())


def check_limit(label, text, limit, errors):
    count = word_count(text)
    if count > limit:
        errors.append(f"{label}: {count} words exceeds the {limit}-word budget")


def load_manifest(errors):
    try:
        return json.loads((ROOT / "bundle-manifest.json").read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"Cannot read bundle-manifest.json: {exc}")
        return {}


def source_skill_descriptions(manifest, errors):
    descriptions = {}
    for skill_name in manifest.get("skills", []):
        path = ROOT / "skills" / skill_name / "SKILL.md"
        try:
            raw, _ = split_frontmatter(path.read_text(encoding="utf-8-sig"))
            description = frontmatter_values(raw).get("description", "")
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: cannot read description: {exc}")
            continue
        if not description:
            errors.append(f"{path.relative_to(ROOT)}: description is required")
        descriptions[skill_name] = description
    return descriptions


def validate_description_budget(label, descriptions, errors):
    total = 0
    for skill_name, description in descriptions.items():
        count = word_count(description)
        total += count
        if count > SKILL_DESCRIPTION_LIMIT:
            errors.append(
                f"{label}/{skill_name}: {count} description words exceeds {SKILL_DESCRIPTION_LIMIT}"
            )
    if total > SKILL_DESCRIPTION_TOTAL_LIMIT:
        errors.append(
            f"{label}: {total} discovery-description words exceeds {SKILL_DESCRIPTION_TOTAL_LIMIT}"
        )


def validate_source(manifest, errors):
    agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8-sig")
    _, agents_body = split_frontmatter(agents_text)
    check_limit("AGENTS.md body", agents_body, AGENTS_BODY_LIMIT, errors)

    for heading in REQUIRED_AGENTS_HEADINGS:
        if f"## {heading}" not in agents_body:
            errors.append(f"AGENTS.md is missing compact heading: {heading}")
    for heading in REMOVED_AGENTS_HEADINGS:
        if f"## {heading}" in agents_body:
            errors.append(f"AGENTS.md retains detailed always-on section: {heading}")

    index_match = re.search(
        r"^## Compact Skill Index\s*$([\s\S]*?)(?=^## |\Z)",
        agents_body,
        flags=re.MULTILINE,
    )
    if not index_match:
        errors.append("AGENTS.md needs a Compact Skill Index section")
    else:
        compact_index = index_match.group(1)
        for skill_name in manifest.get("skills", []):
            if f"`{skill_name}`" not in compact_index:
                errors.append(f"AGENTS.md compact index is missing skill {skill_name}")

    layer_limits = {
        manifest.get("portable_core"): CORE_BODY_LIMIT,
        manifest.get("profiles", {}).get(manifest.get("default_profile")): (
            PROFILE_BODY_LIMIT
        ),
    }
    for relative_path, limit in layer_limits.items():
        if not relative_path:
            continue
        text = (ROOT / relative_path).read_text(encoding="utf-8-sig")
        _, body = split_frontmatter(text)
        check_limit(relative_path, body, limit, errors)
    for relative_path in manifest.get("adapters", {}).values():
        text = (ROOT / relative_path).read_text(encoding="utf-8-sig")
        _, body = split_frontmatter(text)
        check_limit(relative_path, body, ADAPTER_BODY_LIMIT, errors)

    validate_description_budget(
        "source skills", source_skill_descriptions(manifest, errors), errors
    )


def generated_skill_descriptions(root, errors):
    descriptions = {}
    for path in sorted(root.glob("skills/*/SKILL.md")):
        raw, _ = split_frontmatter(path.read_text(encoding="utf-8-sig"))
        values = frontmatter_values(raw)
        keys = set(values)
        if keys != {"name", "description"}:
            errors.append(
                f"{path.relative_to(ROOT)}: generated skill frontmatter must contain only name and description"
            )
        descriptions[path.parent.name] = values.get("description", "")
    return descriptions


def validate_generated_markdown(root, errors):
    for path in root.rglob("*.md"):
        raw, _ = split_frontmatter(path.read_text(encoding="utf-8-sig"))
        if path.name == "SKILL.md":
            continue
        graph_keys = GRAPH_FRONTMATTER_KEYS.intersection(frontmatter_values(raw))
        if graph_keys:
            errors.append(
                f"{path.relative_to(ROOT)}: generated runtime exposes graph metadata {sorted(graph_keys)}"
            )


def validate_generated(manifest, errors):
    canonical_targets = manifest.get("targets", {})
    aliases = manifest.get("target_aliases", {})
    for target_name in (*canonical_targets, *aliases):
        root = ROOT / "dist" / target_name
        if not root.is_dir():
            errors.append(f"dist/{target_name}: generated target is missing")
            continue
        validate_generated_markdown(root, errors)
        descriptions = generated_skill_descriptions(root, errors)
        validate_description_budget(f"dist/{target_name}/skills", descriptions, errors)

        agents_path = root / "AGENTS.md"
        if agents_path.exists():
            raw, body = split_frontmatter(agents_path.read_text(encoding="utf-8-sig"))
            if raw is not None:
                errors.append(f"dist/{target_name}/AGENTS.md retains frontmatter")
            check_limit(
                f"dist/{target_name}/AGENTS.md",
                body,
                AGENTS_BODY_LIMIT,
                errors,
            )

        canonical = aliases.get(target_name, target_name)
        for skill_path in root.glob("skills/*/SKILL.md"):
            text = skill_path.read_text(encoding="utf-8-sig")
            occurrences = text.count(CLAUDE_RUNTIME_PRELUDE)
            expected = 1 if canonical == "claude-code" else 0
            if occurrences != expected:
                errors.append(
                    f"{skill_path.relative_to(ROOT)}: runtime prelude count must be {expected}, got {occurrences}"
                )
    if word_count(CLAUDE_RUNTIME_PRELUDE) > 15:
        errors.append("Claude runtime prelude exceeds the 15-word budget")


def validate(generated=False):
    errors = []
    manifest = load_manifest(errors)
    if manifest:
        validate_source(manifest, errors)
        if generated:
            validate_generated(manifest, errors)
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate always-on policy and skill-discovery context budgets."
    )
    parser.add_argument(
        "--generated",
        action="store_true",
        help="Also validate generated target frontmatter and context budgets.",
    )
    args = parser.parse_args()
    errors = validate(generated=args.generated)
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    scope = "source and generated" if args.generated else "source"
    print(f"Context budgets are valid for {scope} artifacts.")


if __name__ == "__main__":
    main()
