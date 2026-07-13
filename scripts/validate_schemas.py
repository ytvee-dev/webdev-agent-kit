#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPT_DIR = ROOT / "skills" / "agent-rules-skill-author" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPT_DIR))

from skill_common import (  # noqa: E402
    load_openai_yaml,
    load_skill_frontmatter,
    parse_frontmatter,
    split_frontmatter,
)

SCHEMA_DIR = ROOT / "schemas"
HUMAN_ONLY_MARKDOWN_FILES = {
    ".github/PULL_REQUEST_TEMPLATE.md",
    "README.md",
}


class SchemaError(Exception):
    pass


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def schema_path(name):
    return SCHEMA_DIR / f"{name}.schema.json"


def schema_type_name(value):
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if value is None:
        return "null"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    return type(value).__name__


def validate_type(value, expected):
    if isinstance(expected, list):
        return any(validate_type(value, candidate) for candidate in expected)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def validate_instance(value, schema, path="$"):
    errors = []

    if "type" in schema and not validate_type(value, schema["type"]):
        expected = schema["type"]
        errors.append(f"{path}: expected {expected}, got {schema_type_name(value)}")
        return errors

    if "enum" in schema and value not in schema["enum"]:
        allowed = ", ".join(repr(item) for item in schema["enum"])
        errors.append(f"{path}: expected one of {allowed}, got {value!r}")

    if isinstance(value, str):
        min_length = schema.get("minLength")
        max_length = schema.get("maxLength")
        if min_length is not None and len(value) < min_length:
            errors.append(f"{path}: string is shorter than {min_length} characters")
        if max_length is not None and len(value) > max_length:
            errors.append(f"{path}: string is longer than {max_length} characters")
        pattern = schema.get("pattern")
        if pattern and not re.search(pattern, value):
            errors.append(f"{path}: value {value!r} does not match pattern {pattern!r}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if minimum is not None and value < minimum:
            errors.append(f"{path}: value is less than minimum {minimum}")
        if maximum is not None and value > maximum:
            errors.append(f"{path}: value is greater than maximum {maximum}")

    if isinstance(value, list):
        min_items = schema.get("minItems")
        max_items = schema.get("maxItems")
        if min_items is not None and len(value) < min_items:
            errors.append(f"{path}: array has fewer than {min_items} item(s)")
        if max_items is not None and len(value) > max_items:
            errors.append(f"{path}: array has more than {max_items} item(s)")
        if schema.get("uniqueItems"):
            seen = set()
            for item in value:
                key = json.dumps(item, sort_keys=True, ensure_ascii=False)
                if key in seen:
                    errors.append(f"{path}: array items must be unique")
                    break
                seen.add(key)
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                errors.extend(validate_instance(item, item_schema, f"{path}[{index}]"))

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}: missing required property {key!r}")

        properties = schema.get("properties", {})
        for key, item in value.items():
            if key in properties:
                errors.extend(validate_instance(item, properties[key], f"{path}.{key}"))
                continue

            additional = schema.get("additionalProperties", True)
            if additional is False:
                errors.append(f"{path}: unexpected property {key!r}")
            elif isinstance(additional, dict):
                errors.extend(validate_instance(item, additional, f"{path}.{key}"))

    return errors


def validate_with_schema(label, value, schema, errors):
    for error in validate_instance(value, schema):
        errors.append(f"{label}: {error}")


def markdown_files_for_graph_schema():
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if "dist" not in path.parts
        and path.relative_to(ROOT).as_posix() not in HUMAN_ONLY_MARKDOWN_FILES
        and not (path.parent.parent == ROOT / "skills" and path.name == "SKILL.md")
    )


def load_graph_frontmatter(path):
    content = path.read_text(encoding="utf-8-sig")
    frontmatter = split_frontmatter(content)
    if frontmatter is None:
        raise SchemaError("missing YAML frontmatter")
    return parse_frontmatter(frontmatter)


def validate_bundle_manifest(schema, errors):
    manifest_path = ROOT / "bundle-manifest.json"
    try:
        manifest = load_json(manifest_path)
    except Exception as exc:
        errors.append(f"bundle-manifest.json: cannot parse JSON: {exc}")
        return

    validate_with_schema("bundle-manifest.json", manifest, schema, errors)

    skills = manifest.get("skills", [])
    if skills != sorted(skills):
        errors.append("bundle-manifest.json: skills must be sorted alphabetically")

    actual = sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())
    if sorted(skills) != actual:
        errors.append(
            "bundle-manifest.json: skills must match actual skills/* directories"
        )


def validate_tool_capabilities_manifest(schema, errors):
    path = ROOT / "tool-capabilities-manifest.json"
    try:
        manifest = load_json(path)
    except Exception as exc:
        errors.append(f"tool-capabilities-manifest.json: cannot parse JSON: {exc}")
        return

    validate_with_schema("tool-capabilities-manifest.json", manifest, schema, errors)


def validate_skills(schema, errors):
    for skill_dir in sorted(
        path for path in (ROOT / "skills").iterdir() if path.is_dir()
    ):
        try:
            frontmatter, _ = load_skill_frontmatter(skill_dir)
        except Exception as exc:
            errors.append(
                f"skills/{skill_dir.name}/SKILL.md: cannot parse frontmatter: {exc}"
            )
            continue

        label = f"skills/{skill_dir.name}/SKILL.md"
        validate_with_schema(label, frontmatter, schema, errors)

        if frontmatter.get("name") != skill_dir.name:
            errors.append(f"{label}: frontmatter name must match directory name")
        if frontmatter.get("skill") != skill_dir.name:
            errors.append(f"{label}: graph skill must match directory name")


def validate_openai_metadata(schema, errors):
    for skill_dir in sorted(
        path for path in (ROOT / "skills").iterdir() if path.is_dir()
    ):
        label = f"skills/{skill_dir.name}/agents/openai.yaml"
        try:
            data, path = load_openai_yaml(skill_dir)
        except Exception as exc:
            errors.append(f"{label}: cannot parse OpenAI metadata: {exc}")
            continue

        if not path.exists():
            errors.append(f"{label}: file is required")
            continue

        validate_with_schema(label, data, schema, errors)

        default_prompt = data.get("interface", {}).get("default_prompt")
        if default_prompt and f"${skill_dir.name}" not in default_prompt:
            errors.append(
                f"{label}: interface.default_prompt must mention ${skill_dir.name}"
            )


def validate_graph_docs(schema, errors):
    for path in markdown_files_for_graph_schema():
        relative = path.relative_to(ROOT).as_posix()
        try:
            frontmatter = load_graph_frontmatter(path)
        except Exception as exc:
            errors.append(f"{relative}: cannot parse graph frontmatter: {exc}")
            continue
        validate_with_schema(relative, frontmatter, schema, errors)


def validate_schema_files(errors):
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        try:
            load_json(path)
        except Exception as exc:
            errors.append(
                f"{path.relative_to(ROOT).as_posix()}: cannot parse JSON schema: {exc}"
            )


def validate(strict_graph=False):
    errors = []
    validate_schema_files(errors)

    try:
        bundle_schema = load_json(schema_path("bundle-manifest"))
        skill_schema = load_json(schema_path("skill-frontmatter"))
        openai_schema = load_json(schema_path("openai-agent"))
        graph_schema = load_json(schema_path("graph-doc"))
        tool_capabilities_schema = load_json(schema_path("tool-capabilities-manifest"))
    except Exception as exc:
        return [f"schemas: cannot load required schema files: {exc}"]

    validate_bundle_manifest(bundle_schema, errors)
    validate_tool_capabilities_manifest(tool_capabilities_schema, errors)
    validate_skills(skill_schema, errors)
    validate_openai_metadata(openai_schema, errors)
    if strict_graph:
        validate_graph_docs(graph_schema, errors)
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate bundle metadata against repository JSON schemas."
    )
    parser.add_argument(
        "--strict-graph",
        action="store_true",
        help="Also enforce graph-doc schema on non-skill Markdown frontmatter.",
    )
    args = parser.parse_args()
    errors = validate(strict_graph=args.strict_graph)
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Schema validation passed.")


if __name__ == "__main__":
    main()
