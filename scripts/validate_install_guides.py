#!/usr/bin/env python3

import json
import sys
from pathlib import Path

from build_release_archives import RELEASE_TARGETS

ROOT = Path(__file__).resolve().parents[1]
INSTALL_DIR = ROOT / "docs" / "install"
GUIDE_CONTRACTS = {
    "codex": (
        "ru-codex.md",
        (".agents/AGENTS.md", ".agents/skills/", ".agents/.codex-plugin/plugin.json"),
    ),
    "claude-code": (
        "ru-claude-code.md",
        (
            "~/.claude/skills/webdev-agent-kit/.claude-plugin/plugin.json",
            "~/.claude/skills/webdev-agent-kit/skills/",
            "claude --plugin-dir",
        ),
    ),
    "cursor": (
        "ru-cursor.md",
        (".agents/AGENTS.md", ".agents/skills/", ".cursor/rules/webdev-agent-kit.mdc"),
    ),
    "vs-code-codex": (
        "ru-vscode-codex.md",
        (".agents/AGENTS.md", ".agents/skills/", ".agents/.codex-plugin/plugin.json"),
    ),
    "vs-code-claude": (
        "ru-vscode-claude.md",
        (
            "~/.claude/skills/webdev-agent-kit/.claude-plugin/plugin.json",
            "~/.claude/skills/webdev-agent-kit/skills/",
            "/plugins",
        ),
    ),
}


def load_version():
    manifest = json.loads((ROOT / "bundle-manifest.json").read_text(encoding="utf-8"))
    return manifest["version"]


def validate():
    errors = []
    if set(GUIDE_CONTRACTS) != set(RELEASE_TARGETS):
        errors.append("Installation guide targets must match release targets")

    index_path = INSTALL_DIR / "README.md"
    index = index_path.read_text(encoding="utf-8-sig")
    if "status: 'active'" not in index:
        errors.append("docs/install/README.md must be active")
    if "not runtime policy" not in index and "не runtime policy" not in index:
        errors.append("Installation index must remain explicitly human-facing")

    version = load_version()
    for target, (file_name, required_paths) in GUIDE_CONTRACTS.items():
        path = INSTALL_DIR / file_name
        if not path.is_file():
            errors.append(f"Missing installation guide: {path.relative_to(ROOT)}")
            continue
        if f"({file_name})" not in index:
            errors.append(f"Installation index does not link {file_name}")

        text = path.read_text(encoding="utf-8-sig")
        stable = f"webdev-agent-kit-{target}.tar.gz"
        versioned = f"webdev-agent-kit-{target}-v{version}.tar.gz"
        for required in (
            "status: 'active'",
            stable,
            versioned,
            "SHA256SUMS",
            *required_paths,
        ):
            if required not in text:
                errors.append(f"{file_name}: missing install contract {required!r}")

        lowered = text.lower()
        if "распакуйте архив в `.agents/`" in lowered:
            errors.append(f"{file_name}: archive must not be extracted inside .agents")
        if "status: 'draft'" in text:
            errors.append(f"{file_name}: release guide must not remain draft")

    return errors


def main():
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Installation guides match release target and archive contracts.")


if __name__ == "__main__":
    main()
