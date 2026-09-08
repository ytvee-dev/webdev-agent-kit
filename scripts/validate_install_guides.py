#!/usr/bin/env python3

import json
import sys
from pathlib import Path

from build_release_archives import RELEASE_TARGETS

ROOT = Path(__file__).resolve().parents[1]
INSTALL_DIR = ROOT / "docs" / "install"
CURSOR_VIDEO = (
    "[![Watch the Cursor installation video guide]"
    "(https://res.cloudinary.com/duyqvi0ig/video/upload/"
    "so_0,w_1280,c_limit,q_auto/v1784235087/cursor_qj5lqq.jpg)]"
    "(https://res.cloudinary.com/duyqvi0ig/video/upload/"
    "v1784235087/cursor_qj5lqq.mp4)"
)
VSCODE_CODEX_VIDEO = (
    "[![Watch the VS Code Codex installation video guide]"
    "(https://res.cloudinary.com/duyqvi0ig/video/upload/"
    "so_0,w_1280,c_limit,q_auto/v1784235091/vs-code-codex_ilqrde.jpg)]"
    "(https://res.cloudinary.com/duyqvi0ig/video/upload/"
    "v1784235091/vs-code-codex_ilqrde.mp4)"
)
GUIDE_CONTRACTS = {
    "codex": (
        "codex.md",
        "Install WebDev Agent Kit for Codex",
        None,
    ),
    "claude-code": (
        "claude-code.md",
        "Install WebDev Agent Kit for Claude Code",
        None,
    ),
    "cursor": (
        "cursor.md",
        "Install WebDev Agent Kit for Cursor",
        CURSOR_VIDEO,
    ),
    "vs-code-codex": (
        "vscode-codex.md",
        "Install WebDev Agent Kit for VS Code Codex",
        VSCODE_CODEX_VIDEO,
    ),
    "vs-code-claude": (
        "vscode-claude.md",
        "Install WebDev Agent Kit for VS Code Claude",
        None,
    ),
}
GUIDE_REQUIRED_TERMS = {
    "codex": (
        "webdev-agent-kit-codex.tar.gz",
        "/.agents/",
        "/AGENTS.md",
        ".agents/project/",
    ),
    "claude-code": (
        "webdev-agent-kit-claude-code.tar.gz",
        ".claude-plugin/marketplace.json",
        "claude plugin marketplace add",
        "webdev-agent-kit@webdev-agent-kit",
        "--scope user",
    ),
    "cursor": (
        "webdev-agent-kit-cursor.tar.gz",
        "/.agents/",
        "/.cursor/rules/webdev-agent-kit.mdc",
        ".agents/project/",
    ),
    "vs-code-codex": (
        "webdev-agent-kit-vs-code-codex.tar.gz",
        "/.agents/",
        "/AGENTS.md",
        ".agents/project/",
    ),
    "vs-code-claude": (
        "webdev-agent-kit-vs-code-claude.tar.gz",
        ".claude-plugin/marketplace.json",
        "/plugins",
        "Install for you",
        "webdev-agent-kit@webdev-agent-kit",
    ),
}
VIDEO_TERMS = ("video", "видео")


def contains_video_term(text):
    lowered = text.lower()
    return any(term in lowered for term in VIDEO_TERMS)


def validate_install_matrix(text, manifest):
    errors = []
    rows = {}
    for line in text.splitlines():
        cells = [cell.strip().strip("`") for cell in line.split("|")[1:-1]]
        if len(cells) == 4 and cells[0] in RELEASE_TARGETS:
            if cells[0] in rows:
                errors.append(f"Duplicate install matrix target: {cells[0]}")
            rows[cells[0]] = cells[1]
    for target in RELEASE_TARGETS:
        canonical = manifest["target_aliases"].get(target, target)
        if rows.get(target) != canonical:
            errors.append(f"Install matrix alias mismatch: {target} -> {canonical}")
    return errors


def validate():
    errors = []
    manifest = json.loads((ROOT / "bundle-manifest.json").read_text())
    first_run = (INSTALL_DIR / "first-run.md").read_text()
    errors.extend(validate_install_matrix(first_run, manifest))
    for old, new in (
        ("| `vs-code-codex` | `codex`", "| `vs-code-codex` | `cursor`"),
        ("| `vs-code-claude` | `claude-code`", "| `vs-code-claude` | `codex`"),
    ):
        if not validate_install_matrix(first_run.replace(old, new), manifest):
            errors.append("Install matrix failed to detect a changed alias")
    if not (INSTALL_DIR / "upgrade.md").is_file():
        errors.append("Missing upgrade and rollback guide")
    if set(GUIDE_CONTRACTS) != set(RELEASE_TARGETS):
        errors.append("Installation guide targets must match release targets")

    index_path = INSTALL_DIR / "README.md"
    index = index_path.read_text(encoding="utf-8-sig")
    if "status: 'active'" not in index:
        errors.append("docs/install/README.md must be active")
    if "not runtime policy" not in index:
        errors.append("Installation index must remain explicitly human-facing")

    for target, (file_name, heading, video_contract) in GUIDE_CONTRACTS.items():
        path = INSTALL_DIR / file_name
        if not path.is_file():
            errors.append(f"Missing installation guide: {path.relative_to(ROOT)}")
            continue
        if f"({file_name})" not in index:
            errors.append(f"Installation index does not link {file_name}")

        text = path.read_text(encoding="utf-8-sig")
        for link in ("(first-run.md)", "(upgrade.md)"):
            if link not in text:
                errors.append(f"{file_name}: missing shared installation guide {link}")
        for required in ("status: 'active'", f"# {heading}"):
            if required not in text:
                errors.append(f"{file_name}: missing guide contract {required!r}")
        for required in GUIDE_REQUIRED_TERMS[target]:
            if required not in text:
                errors.append(f"{file_name}: missing installation step {required!r}")

        if video_contract is None:
            if contains_video_term(text):
                errors.append(
                    f"{file_name}: installation video is allowed only for "
                    "Cursor and VS Code Codex"
                )
        elif video_contract not in text:
            errors.append(f"{file_name}: missing video contract {video_contract!r}")

        if "status: 'draft'" in text:
            errors.append(f"{file_name}: release guide must not remain draft")

    for forbidden in (
        "Codex — video guide",
        "Claude Code — video guide",
        "VS Code Claude — video guide",
    ):
        if forbidden in index:
            errors.append(
                f"docs/install/README.md: forbidden video entry {forbidden!r}"
            )

    root_readme = (ROOT / "README.md").read_text(encoding="utf-8-sig")
    for forbidden in (
        "[Codex — video",
        "[Claude Code — video",
        "[VS Code Claude — video",
    ):
        if forbidden in root_readme:
            errors.append(f"README.md: forbidden video entry {forbidden!r}")

    return errors


def main():
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Installation guides and client video contracts are valid.")


if __name__ == "__main__":
    main()
