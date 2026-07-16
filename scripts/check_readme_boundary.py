#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "common" / "readme-policy.md"
SCAN_ROOTS = (
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "common",
    ROOT / "profiles",
    ROOT / "adapters",
    ROOT / "skills",
    ROOT / "templates",
    ROOT / "examples",
)
EXCLUDED_PARTS = {"dist", "project", "node_modules", ".obsidian"}
README_REQUIRED_PHRASES = (
    "Agents may read relevant README sections when the task concerns",
    "README is not sufficient as technical evidence.",
    "Reading does not authorize editing.",
    "An existing README must not be edited unless the user's current request explicitly asks to change that README.",
)
EVIDENCE_ORDER = (
    "Real run or test result.",
    "Source code, configuration, or CI.",
    "Package scripts or lockfile.",
    "README.",
    "Assumption.",
)
ABSOLUTE_READ_BANS = (
    re.compile(
        r"\bnever\s+(?:read|open|inspect|scan|search)\s+(?:the\s+)?`?README(?:\.md)?`?",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bmust\s+not\s+(?:read|open|inspect|scan|search)\s+(?:the\s+)?`?README(?:\.md)?`?",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bdo\s+not\s+(?:read|open|inspect|scan|search)\s+.*README.*(?:under\s+any\s+circumstance|during\s+normal\s+runtime|unless\s+the\s+user)",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bexclude\s+`?README(?:\.md)?`?\s+from\s+(?:agent\s+)?context",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bask\s+the\s+user\s+to\s+paste\s+.*README",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bникогда\s+не\s+(?:читай|открывай|проверяй|сканируй|ищи)\s+.*README",
        re.IGNORECASE,
    ),
)
POSITIVE_AUTHORITY_PATTERNS = (
    re.compile(
        r"\bREADME\s+is\s+(?:the\s+)?(?:runtime|routing|policy|validation)\s+(?:source|truth|input)",
        re.IGNORECASE,
    ),
    re.compile(
        r"\buse\s+README\s+as\s+(?:the\s+)?(?:only|sole|authoritative)\s+(?:source|truth|evidence)",
        re.IGNORECASE,
    ),
    re.compile(r"\brely\s+(?:only|solely)\s+on\s+README", re.IGNORECASE),
    re.compile(
        r"\bderive\s+(?:runtime|project|technical)\s+facts\s+from\s+README",
        re.IGNORECASE,
    ),
    re.compile(
        r"\buse\s+README\s+for\s+(?:routing|skill selection|validation|package inventory)",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bREADME\s+является\s+(?:единственным\s+)?(?:runtime-)?(?:источником|истиной|входом)",
        re.IGNORECASE,
    ),
)
AUTOMATIC_EDIT_PATTERNS = (
    re.compile(
        r"\b(?:automatically|autonomously)\s+(?:edit|update|rewrite|sync)\s+.*README",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:edit|update|rewrite|sync)\s+.*README.*(?:after|during|as\s+a\s+side\s+effect|whenever)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bkeep\s+.*README.*in\s+sync\b", re.IGNORECASE),
    re.compile(
        r"\b(?:автоматически|автономно)\s+(?:редактировать|обновлять|переписывать|синхронизировать)\s+.*README",
        re.IGNORECASE,
    ),
)
NEGATIVE_GUARDS = (
    "do not",
    "does not",
    "must not",
    "never",
    "not sufficient",
    "not used",
    "without an explicit",
    "unless the user",
    "unless the current user",
    "only when the user",
    "only when the current user",
    "не является",
    "недостаточно",
    "не разрешает",
    "нельзя",
    "только если",
)


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_ROOTS:
        if root.is_file():
            files.append(root)
        elif root.exists():
            files.extend(sorted(root.rglob("*.md")))
    return [path for path in files if not (set(path.parts) & EXCLUDED_PARTS)]


def has_negative_guard(line: str) -> bool:
    lowered = line.lower()
    return any(guard in lowered for guard in NEGATIVE_GUARDS)


def check_policy_contract() -> list[str]:
    if not POLICY_PATH.is_file():
        return ["common/readme-policy.md is required"]

    errors: list[str] = []
    text = POLICY_PATH.read_text(encoding="utf-8-sig")
    for phrase in (
        "may be read when relevant",
        "must not be edited unless the user's current request explicitly asks to change that README",
    ):
        if phrase not in text:
            errors.append(f"common/readme-policy.md is missing required rule: {phrase}")

    previous_position = -1
    for index, evidence in enumerate(EVIDENCE_ORDER, start=1):
        numbered = f"{index}. {evidence}"
        position = text.find(numbered)
        if position == -1:
            errors.append(f"README evidence hierarchy is missing: {numbered}")
        elif position <= previous_position:
            errors.append("README evidence hierarchy is out of order")
        previous_position = position

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8-sig")
    for phrase in ("common/readme-policy.md", "Reading never authorizes editing"):
        if phrase not in agents:
            errors.append(f"AGENTS.md is missing README boundary: {phrase}")

    readme_path = ROOT / "README.md"
    if not readme_path.is_file():
        errors.append("README.md is required as human-facing documentation")
    else:
        readme = readme_path.read_text(encoding="utf-8-sig")
        normalized_readme = " ".join(readme.split())
        for phrase in README_REQUIRED_PHRASES:
            if phrase not in normalized_readme:
                errors.append(f"README.md is missing boundary: {phrase}")
    return errors


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    relative = path.relative_to(ROOT).as_posix()
    for index, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if "README" not in line.upper():
            continue
        for pattern in ABSOLUTE_READ_BANS:
            if pattern.search(line):
                errors.append(
                    f"{relative}:{index}: absolute README read ban: {line.strip()}"
                )
        if not has_negative_guard(line):
            for pattern in (*POSITIVE_AUTHORITY_PATTERNS, *AUTOMATIC_EDIT_PATTERNS):
                if pattern.search(line):
                    errors.append(
                        f"{relative}:{index}: unsafe README authority/edit rule: {line.strip()}"
                    )
                    break
    return errors


def main() -> None:
    errors = check_policy_contract()
    for path in markdown_files():
        errors.extend(check_file(path))
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("README read/edit boundary and evidence hierarchy are valid.")


if __name__ == "__main__":
    main()
