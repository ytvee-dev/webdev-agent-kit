#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SKILL_TERMS = (
    "shadcn",
    "tailwind-ui",
    "component-library",
    "testing",
    "e2e",
    "unit-test",
)
FORBIDDEN_RUNTIME_PATHS = (
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "bundle-manifest.json",
    "examples",
    "project",
)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
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


def file_inventory(root):
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(
            candidate for candidate in root.rglob("*") if candidate.is_file()
        )
    }


def validate_runtime_exclusions(root, label):
    errors = []
    for relative_path in FORBIDDEN_RUNTIME_PATHS:
        if (root / relative_path).exists():
            errors.append(f"{label} must not include {relative_path}")
    for path in root.rglob("*"):
        if ".obsidian" in path.parts or "node_modules" in path.parts:
            errors.append(f"{label} contains excluded path {path.relative_to(root)}")
    return errors


def validate_portable_skills(root, label, *, require_openai_metadata):
    errors = []
    manifest = load_json(ROOT / "bundle-manifest.json")
    skill_paths = sorted(root.glob("skills/*/SKILL.md"))
    actual = [path.parent.name for path in skill_paths]
    if actual != sorted(manifest.get("skills", [])):
        errors.append(f"{label} skill inventory does not match bundle-manifest.json")

    for skill_path in skill_paths:
        skill_name = skill_path.parent.name
        if any(term in skill_name for term in FORBIDDEN_SKILL_TERMS):
            errors.append(f"{label} packages forbidden skill category {skill_name}")
        try:
            keys, values = read_frontmatter(skill_path)
        except Exception as exc:
            errors.append(str(exc))
            continue
        if keys != ["name", "description"]:
            errors.append(
                f"{skill_path.relative_to(ROOT)} must contain only portable name and description frontmatter"
            )
        if not values.get("name") or not values.get("description"):
            errors.append(f"{skill_path.relative_to(ROOT)} needs name and description")

        metadata = skill_path.parent / "agents" / "openai.yaml"
        if require_openai_metadata and not metadata.is_file():
            errors.append(
                f"{skill_path.parent.relative_to(ROOT)} is missing openai.yaml"
            )
        if not require_openai_metadata and metadata.exists():
            errors.append(
                f"{skill_path.parent.relative_to(ROOT)} exposes Codex-only openai.yaml"
            )
    return errors
