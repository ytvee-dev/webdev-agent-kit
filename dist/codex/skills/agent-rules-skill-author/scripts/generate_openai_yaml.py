#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

from skill_common import (
    MAX_SHORT_DESCRIPTION_LENGTH,
    MIN_SHORT_DESCRIPTION_LENGTH,
    build_openai_yaml,
    format_display_name,
    generate_short_description,
    load_openai_yaml,
    load_skill_frontmatter,
    parse_interface_overrides,
)


def main():
    parser = argparse.ArgumentParser(description="Create or refresh agents/openai.yaml for an .agents skill.")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument("--name", help="Skill name override (defaults to SKILL.md frontmatter)")
    parser.add_argument(
        "--interface",
        action="append",
        default=[],
        help="Interface override in key=value format (repeatable)",
    )
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.exists() or not skill_dir.is_dir():
        print(f"[ERROR] Skill directory not found: {skill_dir}")
        sys.exit(1)

    try:
        frontmatter, _ = load_skill_frontmatter(skill_dir)
        existing_yaml, output_path = load_openai_yaml(skill_dir)
        overrides = parse_interface_overrides(args.interface)
    except Exception as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)

    skill_name = args.name or frontmatter.get("name", "")
    metadata = frontmatter.get("metadata", {}) if isinstance(frontmatter.get("metadata"), dict) else {}
    existing_interface = existing_yaml.get("interface", {})
    existing_policy = existing_yaml.get("policy", {})
    existing_dependencies = existing_yaml.get("dependencies", {})

    display_name = overrides.get("display_name") or existing_interface.get("display_name") or format_display_name(skill_name)
    short_description = (
        overrides.get("short_description")
        or existing_interface.get("short_description")
        or metadata.get("short-description")
        or generate_short_description(display_name)
    )

    if not (MIN_SHORT_DESCRIPTION_LENGTH <= len(short_description) <= MAX_SHORT_DESCRIPTION_LENGTH):
        print(
            "[ERROR] short_description must be 25-64 characters "
            f"(got {len(short_description)})."
        )
        sys.exit(1)

    interface = {
        "display_name": display_name,
        "short_description": short_description,
    }

    for key in ("icon_small", "icon_large", "brand_color", "default_prompt"):
        interface[key] = overrides.get(key) or existing_interface.get(key)

    policy = existing_policy or {"allow_implicit_invocation": True}
    yaml_output = build_openai_yaml(interface, policy=policy, dependencies=existing_dependencies)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml_output, encoding="utf-8")
    print(f"[OK] Created {output_path}")


if __name__ == "__main__":
    main()
