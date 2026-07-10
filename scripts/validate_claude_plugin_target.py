#!/usr/bin/env python3

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "dist" / "claude-code"
ALIASES = (ROOT / "dist" / "claude", ROOT / "dist" / "vs-code-claude")
FORBIDDEN_SKILL_TERMS = (
    "shadcn",
    "tailwind-ui",
    "component-library",
    "testing",
    "e2e",
    "unit-test",
)
REQUIRED_ROOT_FILES = (
    ".claude-plugin/plugin.json",
    "LICENSE",
    "adapters/claude-code.md",
    "common/core/runtime-core-policy.md",
    "profiles/react-typescript/PROFILE.md",
    "tool-capabilities-manifest.json",
)
FORBIDDEN_ROOT_PATHS = (
    ".codex-plugin",
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "bundle-manifest.json",
    "examples",
    "project",
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


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return [], {}, text
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
    return keys, values, text[end + 5 :]


def file_inventory(root):
    inventory = {}
    for path in sorted(
        candidate for candidate in root.rglob("*") if candidate.is_file()
    ):
        inventory[path.relative_to(root).as_posix()] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
    return inventory


def validate_manifest(errors):
    try:
        source = json.loads((ROOT / "bundle-manifest.json").read_text(encoding="utf-8"))
        plugin = json.loads(
            (TARGET / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
    except Exception as exc:
        errors.append(f"Cannot read Claude plugin metadata: {exc}")
        return
    for field in ("name", "version", "description"):
        if not plugin.get(field):
            errors.append(f"Claude plugin manifest needs non-empty {field}")
    for field in ("name", "version", "license"):
        if plugin.get(field) != source.get(field):
            errors.append(
                f"Claude plugin manifest {field} must match bundle-manifest.json"
            )


def validate_aliases(errors):
    expected = file_inventory(TARGET)
    for alias in ALIASES:
        if not alias.exists():
            errors.append(f"{alias.relative_to(ROOT)} does not exist")
        elif file_inventory(alias) != expected:
            errors.append(
                f"{alias.relative_to(ROOT)} must exactly reuse dist/claude-code"
            )


def validate():
    errors = []
    if not TARGET.exists():
        return ["dist/claude-code does not exist; run scripts/build_skill_targets.py"]

    for relative_path in REQUIRED_ROOT_FILES:
        if not (TARGET / relative_path).is_file():
            errors.append(f"dist/claude-code is missing required file: {relative_path}")
    for relative_path in FORBIDDEN_ROOT_PATHS:
        if (TARGET / relative_path).exists():
            errors.append(f"dist/claude-code must not include {relative_path}")
    if list(TARGET.glob("skills/*/agents/openai.yaml")):
        errors.append("Claude plugin must not include Codex-only agents/openai.yaml")

    validate_manifest(errors)

    skills = sorted((TARGET / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("dist/claude-code contains no skills")
    try:
        inventory = json.loads(
            (ROOT / "bundle-manifest.json").read_text(encoding="utf-8")
        )["skills"]
        if [skill.parent.name for skill in skills] != sorted(inventory):
            errors.append(
                "Claude plugin skill inventory does not match bundle-manifest.json"
            )
    except Exception as exc:
        errors.append(f"Cannot validate Claude plugin skill inventory: {exc}")

    for skill in skills:
        name = skill.parent.name
        if any(term in name for term in FORBIDDEN_SKILL_TERMS):
            errors.append(f"Forbidden skill category packaged: {name}")
        try:
            keys, values, _ = read_frontmatter(skill)
        except Exception as exc:
            errors.append(str(exc))
            continue
        if keys != ["name", "description"]:
            errors.append(
                f"{skill.relative_to(ROOT)} must contain only portable name and description frontmatter"
            )
        if not values.get("name") or not values.get("description"):
            errors.append(f"{skill.relative_to(ROOT)} needs name and description")
        skill_text = skill.read_text(encoding="utf-8-sig")
        for runtime_layer in (
            "common/core/runtime-core-policy.md",
            "profiles/react-typescript/PROFILE.md",
            "adapters/claude-code.md",
        ):
            if runtime_layer not in skill_text:
                errors.append(
                    f"{skill.relative_to(ROOT)} does not load {runtime_layer}"
                )

    for markdown_path in TARGET.rglob("*.md"):
        try:
            keys, _, text = read_frontmatter(markdown_path)
        except Exception as exc:
            errors.append(str(exc))
            continue
        if markdown_path.name != "SKILL.md" and GRAPH_FRONTMATTER_KEYS.intersection(
            keys
        ):
            errors.append(
                f"{markdown_path.relative_to(ROOT)} exposes source graph frontmatter"
            )
        if re.search(r"base\s+Codex\s+behavior", text, flags=re.IGNORECASE):
            errors.append(
                f"{markdown_path.relative_to(ROOT)} contains Codex-only fallback language"
            )
        if re.search(r"\]\(\s*(?:\.\./)+", text):
            errors.append(
                f"{markdown_path.relative_to(ROOT)} contains a link that escapes the plugin root"
            )

    validate_aliases(errors)
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate the generated native Claude Code plugin target."
    )
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Claude Code plugin target and aliases are structurally valid.")


if __name__ == "__main__":
    main()
