#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {"dist", "project", "node_modules", ".obsidian", ".git"}
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not (set(path.parts) & EXCLUDED_PARTS)
    )


def strip_anchor(target: str) -> str:
    return target.split("#", 1)[0]


def is_external(target: str) -> bool:
    parsed = urlparse(target)
    return parsed.scheme in {"http", "https"}


def local_target_exists(source: Path, target: str) -> bool:
    target = strip_anchor(target).strip()
    if not target or target.startswith("mailto:"):
        return True
    if is_external(target):
        return True
    if target.startswith("#"):
        return True
    candidate = (source.parent / target).resolve()
    if candidate.exists():
        return True
    if candidate.suffix == "":
        return candidate.with_suffix(".md").exists() or (candidate / "README.md").exists()
    return False


def wiki_target_exists(target: str) -> bool:
    target = target.strip()
    if not target:
        return True
    candidates = [
        ROOT / f"{target}.md",
        ROOT / target,
        ROOT / target / "README.md",
    ]
    return any(candidate.exists() for candidate in candidates)


def check_external_url(url: str, timeout: int) -> str | None:
    request = Request(url, method="HEAD", headers={"User-Agent": "webdev-agent-kit-link-check"})
    try:
        with urlopen(request, timeout=timeout) as response:
            if response.status >= 400:
                return f"HTTP {response.status}"
            return None
    except Exception:
        try:
            request = Request(url, method="GET", headers={"User-Agent": "webdev-agent-kit-link-check"})
            with urlopen(request, timeout=timeout) as response:
                if response.status >= 400:
                    return f"HTTP {response.status}"
                return None
        except Exception as exc:
            return str(exc)


def check_file(path: Path, check_external: bool, timeout: int) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8-sig")
    relative = path.relative_to(ROOT).as_posix()

    for match in MARKDOWN_LINK_RE.finditer(text):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        if is_external(target):
            if check_external:
                error = check_external_url(target, timeout)
                if error:
                    errors.append(f"{relative}: external link failed {target!r}: {error}")
            continue
        if not local_target_exists(path, target):
            errors.append(f"{relative}: broken local link {target!r}")

    for match in WIKI_LINK_RE.finditer(text):
        target = match.group(1).strip()
        if not wiki_target_exists(target):
            errors.append(f"{relative}: broken wiki link {target!r}")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Markdown local links and optional external links.")
    parser.add_argument("--external", action="store_true", help="Also check external HTTP(S) links.")
    parser.add_argument("--timeout", type=int, default=10, help="External link timeout in seconds.")
    args = parser.parse_args()

    errors: list[str] = []
    for path in markdown_files():
        errors.extend(check_file(path, args.external, args.timeout))

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Markdown link validation passed.")


if __name__ == "__main__":
    main()
