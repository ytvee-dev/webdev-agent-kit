#!/usr/bin/env python3

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "dist" / "codex"
FORBIDDEN_SKILL_TERMS = ("shadcn", "tailwind-ui", "component-library", "testing", "e2e", "unit-test")
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
    "common/anti-patterns/no-tests-for-components-or-functions.md",
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
        return ["dist/codex does not exist; run scripts/build_skill_targets.py"]
    if (TARGET / "project").exists():
        errors.append("dist/codex must not include project/**")
    for relative_path in REQUIRED_COMMON_FILES:
        if not (TARGET / relative_path).exists():
            errors.append(f"dist/codex is missing required common file: {relative_path}")
    skills = sorted((TARGET / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("dist/codex contains no skills")
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
            errors.append(f"{skill} must contain only portable frontmatter in dist/codex")
        if not values.get("name") or not values.get("description"):
            errors.append(f"{skill} needs non-empty name and description")
        if not (skill.parent / "agents" / "openai.yaml").exists():
            errors.append(f"{skill.parent} is missing agents/openai.yaml")
    return errors


def main():
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Codex skill pack target is valid.")


if __name__ == "__main__":
    main()
