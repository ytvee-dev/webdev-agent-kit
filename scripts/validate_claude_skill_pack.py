#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "dist" / "claude"
FORBIDDEN_SKILL_TERMS = ("shadcn", "tailwind-ui", "component-library", "testing", "e2e", "unit-test")
REQUIRED_ROOT_FILES = (
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
)
REQUIRED_COMMON_FILES = (
    "common/target-stack-policy.md",
    "common/anti-patterns.md",
    "common/anti-patterns/README.md",
    "common/anti-patterns/no-as-const-variables.md",
    "common/anti-patterns/no-anonymous-functions.md",
    "common/anti-patterns/no-use-callback-by-default.md",
    "common/anti-patterns/no-render-functions.md",
    "common/anti-patterns/no-nested-array-pipelines.md",
    "common/anti-patterns/no-component-loops.md",
    "common/anti-patterns/no-unapproved-test-infrastructure.md",
)


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").lstrip("\ufeff")
    if not text.startswith("---\n"):
        raise ValueError(f"{path} is missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path} has unterminated YAML frontmatter")
    keys = []
    values = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        keys.append(key.strip())
        values[key.strip()] = value.strip()
    return keys, values


def validate():
    errors = []
    if not TARGET.exists():
        return ["dist/claude does not exist; run scripts/build_skill_targets.py"]
    if (TARGET / "project").exists():
        errors.append("dist/claude must not include project/**")
    if (TARGET / "bundle-manifest.json").exists():
        errors.append("dist/claude must not expose the internal bundle-manifest.json")
    if list(TARGET.glob("skills/*/agents/openai.yaml")):
        errors.append("dist/claude must not include Codex-only agents/openai.yaml files")
    if (TARGET / ".codex-plugin").exists():
        errors.append("dist/claude must not include the Codex plugin manifest")
    for relative_path in REQUIRED_ROOT_FILES:
        if not (TARGET / relative_path).exists():
            errors.append(f"dist/claude is missing required root file: {relative_path}")
    for relative_path in REQUIRED_COMMON_FILES:
        if not (TARGET / relative_path).exists():
            errors.append(f"dist/claude is missing required common file: {relative_path}")
    skills = sorted((TARGET / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("dist/claude contains no skills")
    try:
        inventory = json.loads((ROOT / "bundle-manifest.json").read_text(encoding="utf-8"))["skills"]
        if [skill.parent.name for skill in skills] != sorted(inventory):
            errors.append("dist/claude skill inventory does not match bundle-manifest.json")
    except Exception as exc:
        errors.append(f"Cannot validate Claude skill inventory: {exc}")
    for skill in skills:
        name = skill.parent.name
        if any(term in name for term in FORBIDDEN_SKILL_TERMS):
            errors.append(f"Forbidden skill category packaged: {name}")
        try:
            keys, values = read_frontmatter(skill)
        except Exception as exc:
            errors.append(str(exc))
            continue
        if keys[:2] != ["name", "description"]:
            errors.append(f"{skill} must start frontmatter with name and description")
        if set(keys) != {"name", "description"}:
            errors.append(f"{skill} must contain only portable frontmatter in dist/claude")
        if not values.get("name") or not values.get("description"):
            errors.append(f"{skill} needs non-empty name and description")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate the generated Claude portable skill-pack target.")
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Claude skill pack target is valid by local structural checklist.")


if __name__ == "__main__":
    main()
