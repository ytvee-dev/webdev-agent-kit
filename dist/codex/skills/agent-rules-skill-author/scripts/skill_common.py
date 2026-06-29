#!/usr/bin/env python3

import re
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MIN_SHORT_DESCRIPTION_LENGTH = 25
MAX_SHORT_DESCRIPTION_LENGTH = 64

NATIVE_FRONTMATTER_KEYS = {
    "name",
    "description",
    "metadata",
    "license",
    "allowed-tools",
}

GRAPH_FRONTMATTER_KEYS = {
    "id",
    "title",
    "doc_type",
    "layer",
    "status",
    "publishable",
    "local_only",
    "skill",
    "tags",
    "parent",
    "related",
    "depends_on",
}

ALLOWED_FRONTMATTER_KEYS = NATIVE_FRONTMATTER_KEYS | GRAPH_FRONTMATTER_KEYS

ALLOWED_INTERFACE_KEYS = {
    "display_name",
    "short_description",
    "default_prompt",
    "icon_small",
    "icon_large",
    "brand_color",
}

ACRONYMS = {
    "API",
    "CLI",
    "CI",
    "GH",
    "LLM",
    "MCP",
    "PDF",
    "PR",
    "SQL",
    "UI",
    "URL",
}

BRANDS = {
    "datadog": "DataDog",
    "fastapi": "FastAPI",
    "github": "GitHub",
    "openai": "OpenAI",
    "openapi": "OpenAPI",
    "pagerduty": "PagerDuty",
    "sqlite": "SQLite",
}

SMALL_WORDS = {"and", "or", "to", "up", "with"}


def strip_quotes(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_scalar(value):
    value = value.strip()
    if value == "[]":
        return []
    if value == "true":
        return True
    if value == "false":
        return False
    return strip_quotes(value)


def split_frontmatter(content):
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", content, re.DOTALL)
    if not match:
        return None
    return match.group(1)


def strip_frontmatter(content):
    match = re.match(r"^---\r?\n.*?\r?\n---(?:\r?\n|$)(.*)$", content, re.DOTALL)
    if not match:
        return content
    return match.group(1)


def parse_frontmatter(frontmatter_text):
    data = {}
    current_key = None

    for raw_line in frontmatter_text.splitlines():
        if not raw_line.strip():
            continue

        if not raw_line.startswith(" "):
            if ":" not in raw_line:
                raise ValueError(f"Invalid frontmatter line: {raw_line}")
            key, raw_value = raw_line.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()
            current_key = key

            if not raw_value:
                if key in {"metadata"}:
                    data[key] = {}
                else:
                    data[key] = []
                continue

            data[key] = parse_scalar(raw_value)
            current_key = None
            continue

        stripped = raw_line.strip()
        if current_key == "metadata":
            if ":" not in stripped:
                raise ValueError(f"Invalid metadata line: {raw_line}")
            key, raw_value = stripped.split(":", 1)
            data[current_key][key.strip()] = parse_scalar(raw_value)
            continue

        if isinstance(data.get(current_key), list):
            if not stripped.startswith("- "):
                raise ValueError(f"Invalid list item: {raw_line}")
            data[current_key].append(parse_scalar(stripped[2:]))
            continue

        raise ValueError(f"Unsupported frontmatter structure: {raw_line}")

    return data


def load_skill_frontmatter(skill_dir):
    skill_md = Path(skill_dir) / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")
    content = skill_md.read_text(encoding="utf-8-sig")
    frontmatter = split_frontmatter(content)
    if frontmatter is None:
        raise ValueError("No YAML frontmatter found")
    return parse_frontmatter(frontmatter), content


def normalize_skill_name(skill_name):
    normalized = re.sub(r"[^a-z0-9]+", "-", skill_name.strip().lower()).strip("-")
    return re.sub(r"-{2,}", "-", normalized)


def validate_skill_name(skill_name):
    if not re.fullmatch(r"[a-z0-9-]+", skill_name):
        return "Name must use lowercase letters, digits, and hyphens only"
    if skill_name.startswith("-") or skill_name.endswith("-") or "--" in skill_name:
        return "Name cannot start or end with a hyphen or contain consecutive hyphens"
    if len(skill_name) > MAX_SKILL_NAME_LENGTH:
        return f"Name is too long ({len(skill_name)} characters). Maximum is {MAX_SKILL_NAME_LENGTH}"
    return None


def title_case_skill_name(skill_name):
    return " ".join(format_display_word(word, index) for index, word in enumerate(skill_name.split("-")) if word)


def format_display_word(word, index):
    lower = word.lower()
    upper = word.upper()
    if upper in ACRONYMS:
        return upper
    if lower in BRANDS:
        return BRANDS[lower]
    if index > 0 and lower in SMALL_WORDS:
        return lower
    return word.capitalize()


def format_display_name(skill_name):
    words = [word for word in skill_name.split("-") if word]
    return " ".join(format_display_word(word, index) for index, word in enumerate(words))


def generate_short_description(display_name):
    description = f"Help with {display_name} tasks"
    if len(description) < MIN_SHORT_DESCRIPTION_LENGTH:
        description = f"Help with {display_name} tasks and workflows"
    if len(description) < MIN_SHORT_DESCRIPTION_LENGTH:
        description = f"Help with {display_name} tasks with guidance"
    if len(description) > MAX_SHORT_DESCRIPTION_LENGTH:
        description = f"Help with {display_name}"
    if len(description) > MAX_SHORT_DESCRIPTION_LENGTH:
        description = f"{display_name} helper"
    if len(description) > MAX_SHORT_DESCRIPTION_LENGTH:
        description = f"{display_name} tools"
    if len(description) > MAX_SHORT_DESCRIPTION_LENGTH:
        suffix = " helper"
        max_name_length = MAX_SHORT_DESCRIPTION_LENGTH - len(suffix)
        description = f"{display_name[:max_name_length].rstrip()}{suffix}"
    if len(description) > MAX_SHORT_DESCRIPTION_LENGTH:
        description = description[:MAX_SHORT_DESCRIPTION_LENGTH].rstrip()
    if len(description) < MIN_SHORT_DESCRIPTION_LENGTH:
        description = f"{description} workflows"
        if len(description) > MAX_SHORT_DESCRIPTION_LENGTH:
            description = description[:MAX_SHORT_DESCRIPTION_LENGTH].rstrip()
    return description


def parse_interface_overrides(raw_overrides):
    overrides = {}
    for item in raw_overrides:
        if "=" not in item:
            raise ValueError(f"Invalid interface override '{item}'. Use key=value.")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key not in ALLOWED_INTERFACE_KEYS:
            allowed = ", ".join(sorted(ALLOWED_INTERFACE_KEYS))
            raise ValueError(f"Unknown interface field '{key}'. Allowed: {allowed}")
        overrides[key] = value
    return overrides


def yaml_quote(value):
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def split_key_value(line):
    if ":" not in line:
        raise ValueError(f"Invalid YAML line: {line}")
    key, value = line.split(":", 1)
    return key.strip(), value.strip()


def parse_openai_yaml(content):
    data = {}
    section = None
    subsection = None
    current_tool = None

    for raw_line in content.splitlines():
        if not raw_line.strip():
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()

        if indent == 0:
            if not stripped.endswith(":"):
                raise ValueError(f"Invalid top-level YAML line: {raw_line}")
            section = stripped[:-1]
            subsection = None
            if section in {"interface", "policy", "dependencies"}:
                data.setdefault(section, {})
            continue

        if section in {"interface", "policy"} and ":" in stripped and not stripped.endswith(":"):
            key, raw_value = split_key_value(stripped)
            data[section][key] = parse_scalar(raw_value)
            continue

        if section == "dependencies" and stripped == "tools:":
            subsection = "tools"
            data[section]["tools"] = []
            continue

        if section == "dependencies" and subsection == "tools" and stripped.startswith("- "):
            current_tool = {}
            remainder = stripped[2:].strip()
            if remainder:
                key, raw_value = split_key_value(remainder)
                current_tool[key] = parse_scalar(raw_value)
            data[section]["tools"].append(current_tool)
            continue

        if section == "dependencies" and subsection == "tools" and current_tool is not None and ":" in stripped:
            key, raw_value = split_key_value(stripped)
            current_tool[key] = parse_scalar(raw_value)
            continue

        raise ValueError(f"Unsupported openai.yaml structure: {raw_line}")

    return data


def load_openai_yaml(skill_dir):
    path = Path(skill_dir) / "agents" / "openai.yaml"
    if not path.exists():
        return {}, path
    return parse_openai_yaml(path.read_text(encoding="utf-8-sig")), path


def build_openai_yaml(interface, policy=None, dependencies=None):
    lines = [
        "interface:",
        f"  display_name: {yaml_quote(interface['display_name'])}",
        f"  short_description: {yaml_quote(interface['short_description'])}",
    ]

    for key in ("icon_small", "icon_large", "brand_color", "default_prompt"):
        value = interface.get(key)
        if value:
            lines.append(f"  {key}: {yaml_quote(value)}")

    if policy:
        lines.append("")
        lines.append("policy:")
        for key, value in policy.items():
            rendered = "true" if value is True else "false" if value is False else yaml_quote(value)
            lines.append(f"  {key}: {rendered}")

    tools = (dependencies or {}).get("tools", [])
    if tools:
        lines.append("")
        lines.append("dependencies:")
        lines.append("  tools:")
        for tool in tools:
            first = True
            for key in ("type", "value", "description", "transport", "url"):
                if key not in tool:
                    continue
                prefix = "    - " if first else "      "
                lines.append(f"{prefix}{key}: {yaml_quote(tool[key])}")
                first = False

    return "\n".join(lines) + "\n"


def extract_resource_paths(content):
    body = strip_frontmatter(content)
    pattern = re.compile(r"`(?P<path>(?:references|scripts|assets|agents)/[A-Za-z0-9._/\-]+)`")
    paths = []
    seen = set()
    for match in pattern.finditer(body):
        path = match.group("path")
        if path not in seen:
            paths.append(path)
            seen.add(path)
    return paths
