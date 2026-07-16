#!/usr/bin/env python3

import argparse
import hashlib
import json
import re
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

from build_release_archives import RELEASE_TARGETS, VERSION_PATTERN, build_archives

ROOT = Path(__file__).resolve().parents[1]
CLAUDE_TARGETS = {"claude-code", "vs-code-claude"}
CODEX_TARGETS = {"codex", "vs-code-codex"}
HUMAN_FILES = {"README.md", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md"}
FORBIDDEN_ANYWHERE_PARTS = {".obsidian", "node_modules"}
FORBIDDEN_RUNTIME_ROOT_PARTS = {"project", "examples"}
FORBIDDEN_SKILL_TERMS = {
    "shadcn",
    "tailwind-ui",
    "component-library",
    "testing",
    "e2e",
    "unit-test",
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def load_manifest():
    return json.loads((ROOT / "bundle-manifest.json").read_text(encoding="utf-8"))


def safe_member_name(name):
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and ".." not in path.parts


def validate_member_inventory(target, members):
    errors = []
    names = [member.name for member in members]
    expected_first = "webdev-agent-kit" if target in CLAUDE_TARGETS else ".agents"
    if not names or names[0].rstrip("/") != expected_first:
        errors.append(f"{target}: first archive entry must be {expected_first}")

    for member in members:
        name = member.name
        if not safe_member_name(name):
            errors.append(f"{target}: unsafe archive member {name!r}")
            continue
        if member.issym() or member.islnk():
            errors.append(
                f"{target}: links are not allowed in release archives: {name}"
            )
        if not member.isfile() and not member.isdir():
            errors.append(f"{target}: unsupported archive member type: {name}")
        parts = PurePosixPath(name).parts
        if ".agents/.agents" in name:
            errors.append(f"{target}: archive contains double .agents nesting")
        if FORBIDDEN_ANYWHERE_PARTS.intersection(parts):
            errors.append(f"{target}: archive contains excluded path {name}")
        if parts and parts[0] in {".agents", "webdev-agent-kit"}:
            runtime_parts = parts[1:]
            if runtime_parts and runtime_parts[0] in FORBIDDEN_RUNTIME_ROOT_PARTS:
                errors.append(f"{target}: archive contains excluded path {name}")
            if len(runtime_parts) == 1 and runtime_parts[0] in HUMAN_FILES:
                errors.append(f"{target}: archive contains human-facing file {name}")
        if parts and parts[0] in {"AGENTS.md", "CLAUDE.md"}:
            errors.append(f"{target}: archive would overwrite root instructions")
        if any(term in name for term in FORBIDDEN_SKILL_TERMS):
            errors.append(f"{target}: archive contains forbidden skill category {name}")

    if target in CLAUDE_TARGETS:
        if any(name.startswith(".agents/") for name in names):
            errors.append(f"{target}: Claude plugin must not use .agents/skills")
        if "webdev-agent-kit/.claude-plugin/plugin.json" not in names:
            errors.append(f"{target}: native Claude plugin manifest is missing")
        if "webdev-agent-kit/.claude-plugin/marketplace.json" not in names:
            errors.append(f"{target}: Claude marketplace manifest is missing")
        if any("/.codex-plugin/" in name for name in names):
            errors.append(f"{target}: Claude archive contains Codex plugin metadata")
    else:
        if ".agents/AGENTS.md" not in names:
            errors.append(f"{target}: project policy entrypoint is missing")
        if any(name.startswith("webdev-agent-kit/") for name in names):
            errors.append(f"{target}: project target uses plugin-root packaging")

    if target in CODEX_TARGETS:
        if ".agents/.codex-plugin/plugin.json" not in names:
            errors.append(f"{target}: Codex plugin manifest is missing")
    elif any("/agents/openai.yaml" in name for name in names):
        errors.append(f"{target}: archive contains Codex-only skill metadata")

    if target == "cursor":
        if ".cursor/rules/webdev-agent-kit.mdc" not in names:
            errors.append("cursor: root .cursor rule is missing")
        if any(name.startswith(".agents/.cursor/") for name in names):
            errors.append("cursor: rules must not be nested under .agents/.cursor")
    elif any(name.startswith(".cursor/") for name in names):
        errors.append(f"{target}: unexpected Cursor root rules")
    return errors


def extract_and_validate(target, archive, members, destination):
    errors = []
    sentinels = {
        destination / "AGENTS.md": "existing host AGENTS\n",
        destination / "CLAUDE.md": "existing host CLAUDE\n",
    }
    for path, content in sentinels.items():
        path.write_text(content, encoding="utf-8")
    archive.extractall(destination, members=members, filter="data")
    for path, content in sentinels.items():
        if path.read_text(encoding="utf-8") != content:
            errors.append(f"{target}: extraction overwrote {path.name}")

    runtime_root = (
        destination / "webdev-agent-kit"
        if target in CLAUDE_TARGETS
        else destination / ".agents"
    )
    skills_root = runtime_root / "skills"
    expected_skills = sorted(load_manifest().get("skills", []))
    actual_skills = sorted(path.parent.name for path in skills_root.glob("*/SKILL.md"))
    if actual_skills != expected_skills:
        errors.append(f"{target}: archive skill inventory is incomplete")

    version = load_manifest().get("version")
    tool_manifest = runtime_root / "tool-capabilities-manifest.json"
    if not tool_manifest.is_file():
        errors.append(f"{target}: tool capability manifest is missing")
    elif (
        json.loads(tool_manifest.read_text(encoding="utf-8")).get("version") != version
    ):
        errors.append(f"{target}: tool capability version mismatch")

    plugin_path = None
    if target in CLAUDE_TARGETS:
        plugin_path = runtime_root / ".claude-plugin" / "plugin.json"
    elif target in CODEX_TARGETS:
        plugin_path = runtime_root / ".codex-plugin" / "plugin.json"
    if plugin_path is not None:
        if not plugin_path.is_file():
            errors.append(
                f"{target}: native plugin manifest is missing after extraction"
            )
        elif (
            json.loads(plugin_path.read_text(encoding="utf-8")).get("version")
            != version
        ):
            errors.append(f"{target}: native plugin version mismatch")

    if target in CLAUDE_TARGETS:
        marketplace_path = runtime_root / ".claude-plugin" / "marketplace.json"
        try:
            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            plugins = marketplace.get("plugins")
            if marketplace.get("name") != "webdev-agent-kit":
                errors.append(f"{target}: Claude marketplace name mismatch")
            if not isinstance(plugins, list) or len(plugins) != 1:
                errors.append(
                    f"{target}: Claude marketplace must contain exactly one plugin"
                )
            else:
                entry = plugins[0]
                if entry.get("name") != "webdev-agent-kit":
                    errors.append(f"{target}: Claude marketplace plugin name mismatch")
                if entry.get("source") != "./":
                    errors.append(f"{target}: Claude marketplace source must be './'")
                marketplace_root = (runtime_root / entry.get("source", "")).resolve()
                if (
                    not marketplace_root.is_relative_to(runtime_root.resolve())
                    or not (
                        marketplace_root / ".claude-plugin" / "plugin.json"
                    ).is_file()
                ):
                    errors.append(
                        f"{target}: Claude marketplace source does not resolve to the plugin root"
                    )
        except Exception as exc:
            errors.append(f"{target}: cannot validate Claude marketplace: {exc}")

    for markdown in runtime_root.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8-sig")
        for target_link in MARKDOWN_LINK.findall(text):
            clean = target_link.split("#", 1)[0].strip()
            if not clean or clean.startswith(
                ("#", "/", "http://", "https://", "mailto:")
            ):
                continue
            resolved = (markdown.parent / clean).resolve()
            if (
                not resolved.is_relative_to(runtime_root.resolve())
                or not resolved.exists()
            ):
                errors.append(
                    f"{target}: unresolved internal link in {markdown.relative_to(runtime_root)}: {target_link}"
                )
    return errors


def validate_archive(path, target):
    errors = []
    try:
        with tarfile.open(path, "r:gz") as archive:
            members = archive.getmembers()
            errors.extend(validate_member_inventory(target, members))
            if not errors:
                with tempfile.TemporaryDirectory() as temp_dir:
                    errors.extend(
                        extract_and_validate(
                            target,
                            archive,
                            members,
                            Path(temp_dir),
                        )
                    )
    except Exception as exc:
        errors.append(f"{target}: cannot validate {path}: {exc}")
    return errors


def expected_archive_names(version):
    names = set()
    for target in RELEASE_TARGETS:
        names.add(f"webdev-agent-kit-{target}.tar.gz")
        names.add(f"webdev-agent-kit-{target}-{version}.tar.gz")
    return names


def validate_checksums(directory, expected_names, errors):
    checksum_path = directory / "SHA256SUMS"
    if not checksum_path.is_file():
        errors.append("Release directory is missing SHA256SUMS")
        return
    expected = {}
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\s]+)", line)
        if match is None:
            errors.append(f"Malformed checksum line: {line}")
            continue
        digest, name = match.groups()
        if name in expected:
            errors.append(f"Duplicate checksum entry for {name}")
            continue
        expected[name] = digest

    missing = sorted(expected_names - set(expected))
    unexpected = sorted(set(expected) - expected_names)
    if missing:
        errors.append(f"SHA256SUMS is missing archives: {', '.join(missing)}")
    if unexpected:
        errors.append(
            f"SHA256SUMS contains unexpected entries: {', '.join(unexpected)}"
        )

    for name in sorted(expected_names):
        path = directory / name
        if not path.is_file():
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected.get(name) != actual:
            errors.append(f"Checksum mismatch or missing entry for {name}")


def validate_directory(directory, version):
    errors = []
    if not VERSION_PATTERN.fullmatch(version):
        return [f"Invalid release directory version: {version}"]

    expected_names = expected_archive_names(version)
    actual_names = {path.name for path in directory.glob("*.tar.gz")}
    missing = sorted(expected_names - actual_names)
    unexpected = sorted(actual_names - expected_names)
    if missing:
        errors.append(f"Missing release archives: {', '.join(missing)}")
    if unexpected:
        errors.append(f"Unexpected release archives: {', '.join(unexpected)}")

    for target in RELEASE_TARGETS:
        stable = directory / f"webdev-agent-kit-{target}.tar.gz"
        versioned = directory / f"webdev-agent-kit-{target}-{version}.tar.gz"
        if not stable.is_file() or not versioned.is_file():
            continue
        if stable.read_bytes() != versioned.read_bytes():
            errors.append(f"{target}: stable and versioned archives differ")
        errors.extend(validate_archive(stable, target))
    validate_checksums(directory, expected_names, errors)
    return errors


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Validate native paths, exclusions, links, and extraction safety in "
            "release archives."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--directory", type=Path)
    group.add_argument("--build-fixtures", action="store_true")
    group.add_argument("--archive", type=Path)
    parser.add_argument("--target", choices=RELEASE_TARGETS)
    parser.add_argument(
        "--version",
        help="Version suffix for --directory. Defaults to v<source version>.",
    )
    args = parser.parse_args()

    if args.archive:
        if not args.target:
            parser.error("--archive requires --target")
        errors = validate_archive(args.archive, args.target)
    elif args.directory:
        version = args.version or f"v{load_manifest().get('version')}"
        errors = validate_directory(args.directory, version)
    else:
        version = load_manifest().get("version")
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            release_version = f"v{version}"
            build_archives(directory, release_version)
            errors = validate_directory(directory, release_version)

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Release archive fixtures are valid.")


if __name__ == "__main__":
    main()
