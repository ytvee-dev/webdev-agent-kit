#!/usr/bin/env python3

import sys
from pathlib import Path

from build_release_archives import RELEASE_TARGETS

ROOT = Path(__file__).resolve().parents[1]
INSTALL_DIR = ROOT / "docs" / "install"
VIDEO_PLACEHOLDER = "Installation video coming soon."
VSCODE_CODEX_VIDEO = (
    '<video controls src="https://res.cloudinary.com/duyqvi0ig/video/upload/'
    'v1783954898/vscode-codex_tpg1aq.mp4"></video>'
)
GUIDE_CONTRACTS = {
    "codex": (
        "codex.md",
        "Install WebDev Agent Kit for Codex",
        f"> {VIDEO_PLACEHOLDER}",
    ),
    "claude-code": (
        "claude-code.md",
        "Install WebDev Agent Kit for Claude Code",
        f"> {VIDEO_PLACEHOLDER}",
    ),
    "cursor": (
        "cursor.md",
        "Install WebDev Agent Kit for Cursor",
        f"> {VIDEO_PLACEHOLDER}",
    ),
    "vs-code-codex": (
        "vscode-codex.md",
        "Install WebDev Agent Kit for VS Code Codex",
        VSCODE_CODEX_VIDEO,
    ),
    "vs-code-claude": (
        "vscode-claude.md",
        "Install WebDev Agent Kit for VS Code Claude",
        f"> {VIDEO_PLACEHOLDER}",
    ),
}


def validate():
    errors = []
    if set(GUIDE_CONTRACTS) != set(RELEASE_TARGETS):
        errors.append("Installation guide targets must match release targets")

    index_path = INSTALL_DIR / "README.md"
    index = index_path.read_text(encoding="utf-8-sig")
    if "status: 'active'" not in index:
        errors.append("docs/install/README.md must be active")
    if "not runtime policy" not in index:
        errors.append("Installation index must remain explicitly human-facing")

    for file_name, heading, video_contract in GUIDE_CONTRACTS.values():
        path = INSTALL_DIR / file_name
        if not path.is_file():
            errors.append(f"Missing installation guide: {path.relative_to(ROOT)}")
            continue
        if f"({file_name})" not in index:
            errors.append(f"Installation index does not link {file_name}")

        text = path.read_text(encoding="utf-8-sig")
        for required in (
            "status: 'active'",
            f"# {heading}",
            video_contract,
        ):
            if required not in text:
                errors.append(f"{file_name}: missing guide contract {required!r}")

        if "status: 'draft'" in text:
            errors.append(f"{file_name}: release guide must not remain draft")

    return errors


def main():
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Installation guide video contracts match release targets.")


if __name__ == "__main__":
    main()
