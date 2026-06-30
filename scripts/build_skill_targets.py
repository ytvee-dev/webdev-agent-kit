#!/usr/bin/env python3

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
TARGETS = ("codex", "claude")
COPY_ROOT_FILES = ("AGENTS.md", "README.md", "CHANGELOG.md", "plugin.json")
COPY_DIRS = ("common", "templates", "examples")


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
    return f"---\nname: {name}\ndescription: {description}\n---\n\n{body.lstrip()}"


def copy_tree(src, dst):
    if not src.exists():
        return
    shutil.copytree(
        src,
        dst,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )


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

    skills_src = ROOT / "skills"
    skills_dst = target_root / "skills"
    skills_dst.mkdir(parents=True, exist_ok=True)
    for skill_dir in sorted(path for path in skills_src.iterdir() if path.is_dir()):
        dst = skills_dst / skill_dir.name
        dst.mkdir(parents=True)
        skill_text = portable_skill_text((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
        (dst / "SKILL.md").write_text(skill_text, encoding="utf-8")
        for resource_dir in ("references", "scripts", "assets"):
            copy_tree(skill_dir / resource_dir, dst / resource_dir)
        if target == "codex" and (skill_dir / "agents").exists():
            copy_tree(skill_dir / "agents", dst / "agents")


def main():
    for target in TARGETS:
        build_target(target)
    print(f"Built targets in {DIST}")


if __name__ == "__main__":
    main()
