#!/usr/bin/env python3

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
TARGETS = (
    "codex",
    "claude",
    "claude-code",
    "cursor",
    "vs-code-codex",
    "vs-code-claude",
)
CODEX_LIKE_TARGETS = {"codex", "vs-code-codex"}
CLAUDE_LIKE_TARGETS = {"claude-code", "vs-code-claude"}
COPY_ROOT_FILES = (
    "AGENTS.md",
    "LICENSE",
    "tool-capabilities-manifest.json",
)
COPY_DIRS = ("common", "templates")
HUMAN_FACING_ROOT_FILES = (
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
)
HUMAN_FACING_DIRS = ("examples",)


def split_frontmatter(text):
    text = text.replace("\r\n", "\n").lstrip("\ufeff")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + len("\n---\n") :]
    data = {}
    for line in raw.splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data, body


def portable_skill_text(source_text):
    frontmatter, body = split_frontmatter(source_text)
    name = frontmatter.get("name", "").strip("'\"")
    description = frontmatter.get("description", "").strip("'\"")
    if not name or not description:
        raise ValueError("SKILL.md must contain name and description")
    return (
        f"---\nname: {json.dumps(name, ensure_ascii=False)}\n"
        f"description: {json.dumps(description, ensure_ascii=False)}\n---\n\n{body.lstrip()}"
    )


def copy_tree(src, dst):
    if not src.exists():
        return
    shutil.copytree(
        src,
        dst,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )


def write_claude_pointer(target_root):
    (target_root / "CLAUDE.md").write_text(
        "# CLAUDE.md\n\nUse the project-local agent policy in `.agents/AGENTS.md`.\n",
        encoding="utf-8",
    )


def write_cursor_rules(target_root):
    rules_dir = target_root / ".cursor" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    (rules_dir / "webdev-agent-kit.mdc").write_text(
        "---\nalwaysApply: true\n---\n\n"
        "Use the project-local WebDev Agent Kit policy in `.agents/AGENTS.md`.\n",
        encoding="utf-8",
    )


def validate_no_human_facing_files(target_root, target):
    for file_name in HUMAN_FACING_ROOT_FILES:
        if (target_root / file_name).exists():
            raise RuntimeError(f"dist/{target} must not include {file_name}")
    for dir_name in HUMAN_FACING_DIRS:
        if (target_root / dir_name).exists():
            raise RuntimeError(f"dist/{target} must not include {dir_name}/")


def build_target(target):
    target_root = DIST / target
    if target_root.exists():
        shutil.rmtree(target_root)
    target_root.mkdir(parents=True)

    for file_name in COPY_ROOT_FILES:
        src = ROOT / file_name
        if src.exists():
            shutil.copy2(src, target_root / file_name)

    for dir_name in COPY_DIRS:
        copy_tree(ROOT / dir_name, target_root / dir_name)

    if target in CODEX_LIKE_TARGETS:
        copy_tree(ROOT / ".codex-plugin", target_root / ".codex-plugin")
    if target in CLAUDE_LIKE_TARGETS:
        write_claude_pointer(target_root)
    if target == "cursor":
        write_cursor_rules(target_root)

    skills_src = ROOT / "skills"
    skills_dst = target_root / "skills"
    skills_dst.mkdir(parents=True, exist_ok=True)
    for skill_dir in sorted(path for path in skills_src.iterdir() if path.is_dir()):
        dst = skills_dst / skill_dir.name
        dst.mkdir(parents=True)
        skill_text = portable_skill_text(
            (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        )
        (dst / "SKILL.md").write_text(skill_text, encoding="utf-8")
        for resource_dir in ("references", "scripts", "assets"):
            copy_tree(skill_dir / resource_dir, dst / resource_dir)
        if target in CODEX_LIKE_TARGETS and (skill_dir / "agents").exists():
            copy_tree(skill_dir / "agents", dst / "agents")

    validate_no_human_facing_files(target_root, target)


def main():
    parser = argparse.ArgumentParser(
        description="Build lean runtime skill-pack targets."
    )
    parser.add_argument(
        "--target",
        choices=TARGETS,
        action="append",
        help="Build only the selected target; repeat to build multiple targets.",
    )
    args = parser.parse_args()

    targets = tuple(dict.fromkeys(args.target or TARGETS))
    for target in targets:
        build_target(target)
    print(f"Built {', '.join(targets)} runtime target(s) in {DIST}")


if __name__ == "__main__":
    main()
