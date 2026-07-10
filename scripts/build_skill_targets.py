#!/usr/bin/env python3

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
MANIFEST = json.loads((ROOT / "bundle-manifest.json").read_text(encoding="utf-8"))
CANONICAL_TARGETS = tuple(MANIFEST["targets"])
TARGET_ALIASES = MANIFEST["target_aliases"]
TARGETS = CANONICAL_TARGETS + tuple(TARGET_ALIASES)
PORTABLE_CORE = MANIFEST["portable_core"]
DEFAULT_PROFILE = MANIFEST["default_profile"]
PROFILE_PATH = MANIFEST["profiles"][DEFAULT_PROFILE]
ADAPTER_PATHS = MANIFEST["adapters"]
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
CLAUDE_RUNTIME_PRELUDE = (
    "Apply `common/core/runtime-core-policy.md`, evidence-gated "
    "`profiles/react-typescript/PROFILE.md`, and `adapters/claude-code.md`."
)


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


def portable_skill_text(source_text, runtime_prelude=None):
    frontmatter, body = split_frontmatter(source_text)
    name = frontmatter.get("name", "").strip("'\"")
    description = frontmatter.get("description", "").strip("'\"")
    if not name or not description:
        raise ValueError("SKILL.md must contain name and description")
    portable_body = body.lstrip()
    if runtime_prelude:
        portable_body = f"{runtime_prelude}\n\n{portable_body}"
    return (
        f"---\nname: {json.dumps(name, ensure_ascii=False)}\n"
        f"description: {json.dumps(description, ensure_ascii=False)}\n---\n\n"
        f"{portable_body}"
    )


def copy_file(src, dst, *, strip_graph_frontmatter=False):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if strip_graph_frontmatter and src.suffix == ".md":
        frontmatter, body = split_frontmatter(src.read_text(encoding="utf-8-sig"))
        if frontmatter.get("id"):
            dst.write_text(body.lstrip(), encoding="utf-8")
            return
    shutil.copy2(src, dst)


def copy_tree(src, dst, *, strip_graph_frontmatter=False):
    if not src.exists():
        return
    for source_path in sorted(src.rglob("*")):
        if source_path.name == "__pycache__" or source_path.suffix in {
            ".pyc",
            ".pyo",
        }:
            continue
        relative_path = source_path.relative_to(src)
        destination_path = dst / relative_path
        if source_path.is_dir():
            destination_path.mkdir(parents=True, exist_ok=True)
            continue
        copy_file(
            source_path,
            destination_path,
            strip_graph_frontmatter=strip_graph_frontmatter,
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


def prepare_target_root(target):
    target_root = DIST / target
    if target_root.exists():
        shutil.rmtree(target_root)
    target_root.mkdir(parents=True)
    return target_root


def copy_runtime_layers(target_root, target, *, strip_graph_frontmatter):
    for relative_path in (PORTABLE_CORE, PROFILE_PATH, ADAPTER_PATHS[target]):
        copy_file(
            ROOT / relative_path,
            target_root / relative_path,
            strip_graph_frontmatter=strip_graph_frontmatter,
        )


def copy_skills(
    target_root,
    *,
    include_codex_metadata,
    strip_graph_frontmatter,
    runtime_prelude=None,
):
    skills_src = ROOT / "skills"
    skills_dst = target_root / "skills"
    skills_dst.mkdir(parents=True, exist_ok=True)
    for skill_dir in sorted(path for path in skills_src.iterdir() if path.is_dir()):
        dst = skills_dst / skill_dir.name
        dst.mkdir(parents=True)
        skill_text = portable_skill_text(
            (skill_dir / "SKILL.md").read_text(encoding="utf-8"),
            runtime_prelude=runtime_prelude,
        )
        (dst / "SKILL.md").write_text(skill_text, encoding="utf-8")
        for resource_dir in ("references", "scripts", "assets"):
            copy_tree(
                skill_dir / resource_dir,
                dst / resource_dir,
                strip_graph_frontmatter=strip_graph_frontmatter,
            )
        if include_codex_metadata and (skill_dir / "agents").exists():
            copy_tree(skill_dir / "agents", dst / "agents")


def copy_project_target_base(target_root, target, *, include_codex_metadata):
    for file_name in COPY_ROOT_FILES:
        src = ROOT / file_name
        if src.exists():
            copy_file(
                src,
                target_root / file_name,
                strip_graph_frontmatter=file_name == "AGENTS.md",
            )

    for dir_name in COPY_DIRS:
        copy_tree(
            ROOT / dir_name,
            target_root / dir_name,
            strip_graph_frontmatter=True,
        )

    copy_runtime_layers(target_root, target, strip_graph_frontmatter=True)
    copy_skills(
        target_root,
        include_codex_metadata=include_codex_metadata,
        strip_graph_frontmatter=True,
    )

    validate_no_human_facing_files(target_root, target)


def build_codex_plugin_target(target_root):
    copy_tree(ROOT / ".codex-plugin", target_root / ".codex-plugin")


def build_codex_project_target():
    target = "codex"
    target_root = prepare_target_root(target)
    copy_project_target_base(target_root, target, include_codex_metadata=True)
    build_codex_plugin_target(target_root)


def build_cursor_project_target():
    target = "cursor"
    target_root = prepare_target_root(target)
    copy_project_target_base(target_root, target, include_codex_metadata=False)
    write_cursor_rules(target_root)


def build_claude_plugin_target():
    target = "claude-code"
    target_root = prepare_target_root(target)

    for file_name in ("LICENSE", "tool-capabilities-manifest.json"):
        shutil.copy2(ROOT / file_name, target_root / file_name)

    copy_tree(ROOT / ".claude-plugin", target_root / ".claude-plugin")
    for dir_name in COPY_DIRS:
        copy_tree(
            ROOT / dir_name,
            target_root / dir_name,
            strip_graph_frontmatter=True,
        )
    copy_runtime_layers(target_root, target, strip_graph_frontmatter=True)
    copy_skills(
        target_root,
        include_codex_metadata=False,
        strip_graph_frontmatter=True,
        runtime_prelude=CLAUDE_RUNTIME_PRELUDE,
    )

    validate_no_human_facing_files(target_root, target)


def build_canonical_target(target):
    if target == "claude-code":
        build_claude_plugin_target()
        return
    if target == "codex":
        build_codex_project_target()
        return
    if target == "cursor":
        build_cursor_project_target()
        return
    raise ValueError(f"Unknown canonical target: {target}")


def build_alias(alias):
    canonical = TARGET_ALIASES[alias]
    canonical_root = DIST / canonical
    alias_root = DIST / alias
    if alias_root.exists():
        shutil.rmtree(alias_root)
    shutil.copytree(canonical_root, alias_root)


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

    requested_targets = tuple(dict.fromkeys(args.target or TARGETS))
    built_canonical_targets = set()
    for target in requested_targets:
        canonical = TARGET_ALIASES.get(target, target)
        if canonical not in built_canonical_targets:
            build_canonical_target(canonical)
            built_canonical_targets.add(canonical)
        if target in TARGET_ALIASES:
            build_alias(target)
    print(f"Built {', '.join(requested_targets)} runtime target(s) in {DIST}")


if __name__ == "__main__":
    main()
