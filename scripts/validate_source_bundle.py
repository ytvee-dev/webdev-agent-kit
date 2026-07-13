#!/usr/bin/env python3

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST_ROOT = ROOT.parent
REQUIRED_SKILL_SECTIONS = (
    "Purpose",
    "When To Use",
    "When Not To Use",
    "Required Context",
    "Tool Contract",
    "Workflow",
    "Output Contract",
    "Validation Gates",
    "Trigger Evals",
    "Reference Map",
)
POSITIVE_PATH_DOCS = (
    ROOT / "project" / "architecture-map.md",
    ROOT / "project" / "react" / "path-index.md",
    ROOT / "project" / "approved-patterns.md",
)
REMOVED_TERMS = (
    "SUMMARY.md",
    "[[SUMMARY",
    "no-tests-for-components-or-functions.md",
    "skills/frontend-typescript-rules",
    "boundary-input-validation",
    "frontend-security-inspector",
    "webapp-task-protocol",
    "react-component-workflow",
    "react-state-workflow",
    "frontend-review-and-fix",
)
HUMAN_ONLY_MARKDOWN_FILES = {
    ".github/PULL_REQUEST_TEMPLATE.md",
    "README.md",
}
LOCAL_ONLY_WIKILINK_PREFIXES = ("project/",)
OPTIONAL_ORPHAN_PATH_PREFIXES = ("examples/",)


def markdown_files():
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if "dist" not in path.parts
        and path.relative_to(ROOT).as_posix() not in HUMAN_ONLY_MARKDOWN_FILES
    )


def split_frontmatter(path):
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5 :]


def scalar(frontmatter, key):
    match = re.search(
        rf"^{re.escape(key)}:\s*['\"]?([^'\"\n]+)", frontmatter, re.MULTILINE
    )
    return match.group(1).strip() if match else None


def resolve_wikilink(target):
    target = target.split("#", 1)[0].strip()
    candidates = (ROOT / f"{target}.md", ROOT / target / "SKILL.md", ROOT / target)
    return next((path for path in candidates if path.is_file()), None)


def graph_field_links(frontmatter, field):
    links = []
    active = False
    for line in frontmatter.splitlines():
        if line.startswith(f"{field}:"):
            active = True
        elif active and line and not line[0].isspace():
            break
        if active:
            links.extend(re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", line))
    return links


def is_local_only_wikilink(target):
    return target.startswith(LOCAL_ONLY_WIKILINK_PREFIXES)


def is_optional_orphan(path):
    relative = path.relative_to(ROOT).as_posix()
    return relative.startswith(OPTIONAL_ORPHAN_PATH_PREFIXES)


def validate_license(errors):
    path = ROOT / "LICENSE"
    if not path.exists():
        errors.append("LICENSE file is required and must use Apache License 2.0")
        return

    text = path.read_text(encoding="utf-8", errors="replace")
    if "Apache License" not in text or "Version 2.0" not in text:
        errors.append("LICENSE must contain Apache License 2.0 text")


def validate_markdown(errors):
    ids = {}
    paths = markdown_files()
    incoming = {path.resolve(): 0 for path in paths}
    for path in paths:
        frontmatter, text = split_frontmatter(path)
        relative = path.relative_to(ROOT).as_posix()
        if frontmatter is None:
            errors.append(f"{relative}: missing or unterminated YAML frontmatter")
            continue
        document_id = scalar(frontmatter, "id")
        if not document_id:
            errors.append(f"{relative}: missing graph id")
        elif document_id in ids:
            errors.append(
                f"Duplicate graph id {document_id}: {ids[document_id]} and {relative}"
            )
        else:
            ids[document_id] = relative

        if relative.startswith("skills/") and relative.endswith("/SKILL.md"):
            for key in ("name", "description"):
                match = re.search(rf"^{key}:\s*(.+)$", frontmatter, re.MULTILINE)
                if (
                    match
                    and not match.group(1).startswith(("'", '"'))
                    and ": " in match.group(1)
                ):
                    errors.append(
                        f"{relative}: unquoted {key} is not valid YAML because it contains ': '"
                    )

        document = f"{frontmatter}\n{text}"
        for match in re.finditer(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", document):
            target = match.group(1)
            resolved = resolve_wikilink(target)
            if resolved is None:
                if is_local_only_wikilink(target):
                    continue
                errors.append(f"{relative}: unresolved wikilink [[{target}]]")
            elif resolved.resolve() in incoming:
                incoming[resolved.resolve()] += 1

        for field in ("parent", "related", "depends_on"):
            links = graph_field_links(frontmatter, field)
            duplicates = sorted({link for link in links if links.count(link) > 1})
            for target in duplicates:
                errors.append(f"{relative}: duplicate {field} edge [[{target}]]")

        for term in REMOVED_TERMS:
            if term in text:
                errors.append(f"{relative}: stale removed term {term}")

    orphan_exceptions = {
        (ROOT / "AGENTS.md").resolve(),
        (ROOT / "CHANGELOG.md").resolve(),
        (ROOT / "CONTRIBUTING.md").resolve(),
        (ROOT / "SECURITY.md").resolve(),
        (ROOT / "AUDIT_AND_OPTIMIZATION_PLAN.md").resolve(),
    }
    for path, count in incoming.items():
        if (
            count == 0
            and path not in orphan_exceptions
            and not is_optional_orphan(path)
        ):
            errors.append(
                f"{path.relative_to(ROOT)}: graph document has no incoming edge"
            )


def skill_directories():
    return sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())


def validate_skill_inventory(errors):
    actual = [path.name for path in skill_directories()]
    manifest_path = ROOT / "bundle-manifest.json"
    plugin_path = ROOT / ".codex-plugin" / "plugin.json"

    if (ROOT / "plugin.json").exists():
        errors.append(
            "Legacy root plugin.json must not exist; use bundle-manifest.json and .codex-plugin/plugin.json"
        )

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"Invalid bundle-manifest.json: {exc}")
        manifest = {}
    if sorted(manifest.get("skills", [])) != actual:
        errors.append("bundle-manifest.json skill inventory does not match skills/*")

    try:
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"Invalid .codex-plugin/plugin.json: {exc}")
        plugin = {}
    if plugin.get("skills") != "./skills/":
        errors.append("Native Codex plugin manifest must use skills: './skills/'")

    validator = (
        ROOT
        / "skills"
        / "agent-rules-skill-author"
        / "scripts"
        / "validate_agent_skill.py"
    )
    for skill_dir in skill_directories():
        content = (skill_dir / "SKILL.md").read_text(encoding="utf-8-sig")
        for section_name in REQUIRED_SKILL_SECTIONS:
            if not re.search(
                rf"^## {re.escape(section_name)}\s*$", content, re.MULTILINE
            ):
                errors.append(
                    f"skills/{skill_dir.name}/SKILL.md: missing section {section_name}"
                )
        if not (skill_dir / "agents" / "openai.yaml").exists():
            errors.append(f"skills/{skill_dir.name}: missing agents/openai.yaml")
            continue
        result = subprocess.run(
            [sys.executable, str(validator), str(skill_dir)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            output = (result.stdout + result.stderr).strip()
            errors.append(f"skills/{skill_dir.name}: {output}")


def validate_skill_path_mentions(errors):
    actual = {path.name for path in skill_directories()}
    for path in markdown_files():
        text = path.read_text(encoding="utf-8-sig")
        pattern = r"(?<![A-Za-z0-9._/-])(?:\.agents/)?skills/([a-z0-9-]+)/"
        for name in re.findall(pattern, text):
            if name == "skills":
                continue
            if name not in actual:
                errors.append(
                    f"{path.relative_to(ROOT).as_posix()}: unknown skill path {name}"
                )


def path_exists(pattern):
    if "*" in pattern:
        return any(HOST_ROOT.glob(pattern))
    return (HOST_ROOT / pattern).exists()


def validate_positive_project_paths(errors):
    pattern = re.compile(r"`((?:src|tools)/[A-Za-z0-9_@.*\-/]+(?:\.[A-Za-z0-9.*]+)?)`")
    for path in POSITIVE_PATH_DOCS:
        if not path.exists():
            # `project/**` is a local-only overlay and is intentionally ignored in
            # the reusable source bundle. A clean checkout must still validate.
            continue
        text = path.read_text(encoding="utf-8-sig")
        for referenced in sorted(set(pattern.findall(text))):
            if not path_exists(referenced):
                relative = path.relative_to(ROOT).as_posix()
                errors.append(
                    f"{relative}: positive project path does not exist: {referenced}"
                )


def validate():
    errors = []
    validate_license(errors)
    validate_markdown(errors)
    validate_skill_inventory(errors)
    validate_skill_path_mentions(errors)
    validate_positive_project_paths(errors)
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate the source .agents bundle before building targets."
    )
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Source agent bundle is valid.")


if __name__ == "__main__":
    main()
