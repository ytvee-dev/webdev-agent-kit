#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path

from skill_common import (
    ALLOWED_FRONTMATTER_KEYS,
    GRAPH_FRONTMATTER_KEYS,
    MAX_DESCRIPTION_LENGTH,
    MAX_SHORT_DESCRIPTION_LENGTH,
    MIN_SHORT_DESCRIPTION_LENGTH,
    extract_resource_paths,
    load_openai_yaml,
    load_skill_frontmatter,
    validate_skill_name,
)


def fail(message):
    print(message)
    return 1


def validate_frontmatter(frontmatter):
    unexpected = sorted(set(frontmatter.keys()) - ALLOWED_FRONTMATTER_KEYS)
    if unexpected:
        allowed = ", ".join(sorted(ALLOWED_FRONTMATTER_KEYS))
        return (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(unexpected)}. "
            f"Allowed properties are: {allowed}"
        )

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name.strip():
        return "Missing or invalid 'name' in frontmatter"

    name_error = validate_skill_name(name.strip())
    if name_error:
        return name_error

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        return "Missing or invalid 'description' in frontmatter"

    if "<" in description or ">" in description:
        return "Description cannot contain angle brackets (< or >)"

    if len(description.strip()) > MAX_DESCRIPTION_LENGTH:
        return (
            f"Description is too long ({len(description.strip())} characters). "
            f"Maximum is {MAX_DESCRIPTION_LENGTH}"
        )

    metadata = frontmatter.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        return "metadata must be a mapping when present"

    if isinstance(metadata, dict):
        short_description = metadata.get("short-description")
        if short_description is not None and not isinstance(short_description, str):
            return "metadata.short-description must be a string when present"

    for graph_key in GRAPH_FRONTMATTER_KEYS & set(frontmatter.keys()):
        value = frontmatter[graph_key]
        if graph_key in {"tags", "parent", "related", "depends_on"} and not isinstance(value, list):
            return f"{graph_key} must be a list in .agents graph metadata"

    return None


def validate_openai_yaml(skill_name, data):
    if not data:
        return "agents/openai.yaml not found"

    interface = data.get("interface")
    if not isinstance(interface, dict):
        return "openai.yaml must contain an interface mapping"

    display_name = interface.get("display_name")
    if not isinstance(display_name, str) or not display_name.strip():
        return "interface.display_name must be a non-empty string"

    short_description = interface.get("short_description")
    if not isinstance(short_description, str):
        return "interface.short_description must be a string"
    if not (
        MIN_SHORT_DESCRIPTION_LENGTH
        <= len(short_description)
        <= MAX_SHORT_DESCRIPTION_LENGTH
    ):
        return (
            "interface.short_description must be 25-64 characters "
            f"(got {len(short_description)})"
        )

    default_prompt = interface.get("default_prompt")
    if default_prompt is not None:
        if not isinstance(default_prompt, str) or not default_prompt.strip():
            return "interface.default_prompt must be a non-empty string when present"
        if f"${skill_name}" not in default_prompt:
            return "interface.default_prompt must mention the skill as $skill-name"

    brand_color = interface.get("brand_color")
    if brand_color is not None and not re.fullmatch(r"#[0-9A-Fa-f]{6}", brand_color):
        return "interface.brand_color must be a 6-digit hex color when present"

    policy = data.get("policy", {})
    if policy and not isinstance(policy, dict):
        return "policy must be a mapping when present"

    allow_implicit = policy.get("allow_implicit_invocation")
    if allow_implicit is not None and not isinstance(allow_implicit, bool):
        return "policy.allow_implicit_invocation must be boolean when present"

    dependencies = data.get("dependencies", {})
    if dependencies and not isinstance(dependencies, dict):
        return "dependencies must be a mapping when present"

    tools = dependencies.get("tools", [])
    if tools and not isinstance(tools, list):
        return "dependencies.tools must be a list when present"

    for index, tool in enumerate(tools):
        if not isinstance(tool, dict):
            return f"dependencies.tools[{index}] must be a mapping"
        tool_type = tool.get("type")
        tool_value = tool.get("value")
        if not isinstance(tool_type, str) or not tool_type:
            return f"dependencies.tools[{index}].type must be a non-empty string"
        if not isinstance(tool_value, str) or not tool_value:
            return f"dependencies.tools[{index}].value must be a non-empty string"
        if tool_type != "mcp":
            return f"dependencies.tools[{index}].type must be 'mcp' when present"
        for optional_key in ("description", "transport", "url"):
            optional_value = tool.get(optional_key)
            if optional_value is not None and not isinstance(optional_value, str):
                return f"dependencies.tools[{index}].{optional_key} must be a string when present"

    return None


def validate_referenced_paths(skill_dir, content):
    missing = []
    for relative_path in extract_resource_paths(content):
        path = Path(skill_dir) / relative_path
        if not path.exists():
            missing.append(relative_path)
    if missing:
        return f"Referenced path(s) not found: {', '.join(missing)}"
    return None


def main():
    parser = argparse.ArgumentParser(description="Validate an .agents skill package.")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.exists() or not skill_dir.is_dir():
        sys.exit(fail(f"Skill directory not found: {skill_dir}"))

    try:
        frontmatter, content = load_skill_frontmatter(skill_dir)
    except Exception as exc:
        sys.exit(fail(str(exc)))

    error = validate_frontmatter(frontmatter)
    if error:
        sys.exit(fail(error))

    try:
        openai_yaml, _ = load_openai_yaml(skill_dir)
    except Exception as exc:
        sys.exit(fail(f"Invalid agents/openai.yaml: {exc}"))

    error = validate_openai_yaml(frontmatter["name"].strip(), openai_yaml)
    if error:
        sys.exit(fail(error))

    error = validate_referenced_paths(skill_dir, content)
    if error:
        sys.exit(fail(error))

    print("Skill is valid!")


if __name__ == "__main__":
    main()
