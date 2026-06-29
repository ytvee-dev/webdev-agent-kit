#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

from generate_openai_yaml import main as generate_openai_yaml_main
from skill_common import normalize_skill_name, parse_interface_overrides, title_case_skill_name

ALLOWED_RESOURCES = {"scripts", "references", "assets"}

SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Explain what the skill does and when to use it.]
id: 'agents.skills.{skill_name}.skill'
title: '{skill_title}'
doc_type: 'skill'
layer: 'skill'
status: 'draft'
publishable: true
local_only: false
skill: '{skill_name}'
tags:
    - 'agents/skill-package'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related: []
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# {skill_title}

## Purpose

[TODO: Explain the capability this skill adds.]

## Workflow

1. [TODO: Capture the trigger boundary.]
2. [TODO: Describe the reusable workflow.]
3. [TODO: Describe validation or stop conditions.]
"""

EXAMPLE_SCRIPT = """#!/usr/bin/env python3

def main():
    print("Replace this example with a real helper script or delete it.")


if __name__ == "__main__":
    main()
"""

EXAMPLE_REFERENCE = """# Example Reference

Replace this example with real reference material or delete it.
"""

EXAMPLE_ASSET = """Replace this example with a real asset or delete it.
"""


def parse_resources(raw_resources):
    if not raw_resources:
        return []
    resources = [item.strip() for item in raw_resources.split(",") if item.strip()]
    invalid = sorted({item for item in resources if item not in ALLOWED_RESOURCES})
    if invalid:
        allowed = ", ".join(sorted(ALLOWED_RESOURCES))
        raise ValueError(f"Unknown resource type(s): {', '.join(invalid)}. Allowed: {allowed}")
    deduped = []
    seen = set()
    for resource in resources:
        if resource not in seen:
            deduped.append(resource)
            seen.add(resource)
    return deduped


def create_resource_dirs(skill_dir, resources, include_examples):
    for resource in resources:
        resource_dir = skill_dir / resource
        resource_dir.mkdir(exist_ok=True)
        if not include_examples:
            continue
        if resource == "scripts":
            example_script = resource_dir / "example.py"
            example_script.write_text(EXAMPLE_SCRIPT, encoding="utf-8")
        elif resource == "references":
            example_reference = resource_dir / "example.md"
            example_reference.write_text(EXAMPLE_REFERENCE, encoding="utf-8")
        elif resource == "assets":
            example_asset = resource_dir / "example.txt"
            example_asset.write_text(EXAMPLE_ASSET, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Initialize a new .agents skill package.")
    parser.add_argument("skill_name", help="Skill name (normalized to hyphen-case)")
    parser.add_argument("--path", required=True, help="Output directory for the skill")
    parser.add_argument(
        "--resources",
        default="",
        help="Comma-separated list: scripts,references,assets",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Create example files inside selected resource directories",
    )
    parser.add_argument(
        "--interface",
        action="append",
        default=[],
        help="Interface override in key=value format (repeatable)",
    )
    args = parser.parse_args()

    try:
        parse_interface_overrides(args.interface)
        resources = parse_resources(args.resources)
    except Exception as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)

    raw_skill_name = args.skill_name
    skill_name = normalize_skill_name(raw_skill_name)
    if not skill_name:
        print("[ERROR] Skill name must include at least one letter or digit.")
        sys.exit(1)
    if skill_name != raw_skill_name:
        print(f"Note: Normalized skill name from '{raw_skill_name}' to '{skill_name}'.")

    if args.examples and not resources:
        print("[ERROR] --examples requires --resources to be set.")
        sys.exit(1)

    skill_dir = Path(args.path).resolve() / skill_name
    if skill_dir.exists():
        print(f"[ERROR] Skill directory already exists: {skill_dir}")
        sys.exit(1)

    skill_dir.mkdir(parents=True, exist_ok=False)
    skill_title = title_case_skill_name(skill_name)
    (skill_dir / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title),
        encoding="utf-8",
    )
    create_resource_dirs(skill_dir, resources, args.examples)

    argv = [
        "generate_openai_yaml.py",
        str(skill_dir),
        "--name",
        skill_name,
    ]
    for item in args.interface:
        argv.extend(["--interface", item])

    old_argv = sys.argv[:]
    try:
        sys.argv = argv
        generate_openai_yaml_main()
    finally:
        sys.argv = old_argv

    print(f"[OK] Skill '{skill_name}' initialized successfully at {skill_dir}")
    print("Next steps:")
    print("1. Edit SKILL.md and replace the TODO fields with real guidance.")
    print("2. Add only the resources this skill actually needs.")
    print("3. Run validate_agent_skill.py when the draft is ready.")


if __name__ == "__main__":
    main()
