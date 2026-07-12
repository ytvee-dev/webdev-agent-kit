#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from validate_context_budgets import validate as validate_context_budgets

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CLAUDE_RUNTIME_PRELUDE = (
    "Apply `common/core/runtime-core-policy.md`, evidence-gated "
    "`profiles/react-typescript/PROFILE.md`, and `adapters/claude-code.md`."
)
PLANNING_COMMON = (
    "common/agent-loop-policy.md",
    "common/checkpoint-rules.md",
    "common/context-compaction-rules.md",
    "common/convergence-rules.md",
    "common/goal-contract.md",
    "common/independent-review-rules.md",
    "common/planning-analysis-rules.md",
    "common/planning-rules.md",
)
PLANNING_TEMPLATES = (
    "templates/decision-log.md",
    "templates/execution-plan.md",
    "templates/goal-contract.md",
    "templates/loop-memory.md",
    "templates/loop-workflow-contract.md",
    "templates/progress-log.md",
)
PLANNING_SKILLS = (
    "execution-plan-manager",
    "frontend-quality-reviewer",
    "goal-planner",
    "loop-workflow-planner",
)


def load_manifest() -> dict:
    return json.loads((ROOT / "bundle-manifest.json").read_text(encoding="utf-8"))


def split_frontmatter(text: str) -> tuple[str | None, str]:
    normalized = text.replace("\r\n", "\n").lstrip("\ufeff")
    if not normalized.startswith("---\n"):
        return None, normalized
    end = normalized.find("\n---\n", 4)
    if end == -1:
        return None, normalized
    return normalized[4:end], normalized[end + 5 :]


def source_runtime_body(relative: str) -> str:
    text = (ROOT / relative).read_text(encoding="utf-8-sig")
    _, body = split_frontmatter(text)
    return body.lstrip()


def generated_skill_body(path: Path, canonical: str, errors: list[str]) -> str:
    raw, body = split_frontmatter(path.read_text(encoding="utf-8-sig"))
    if raw is None:
        errors.append(
            f"{path.relative_to(ROOT)}: portable skill frontmatter is missing"
        )
        return body
    keys = {
        line.split(":", 1)[0].strip()
        for line in raw.splitlines()
        if ":" in line and not line.startswith(" ")
    }
    if keys != {"name", "description"}:
        errors.append(
            f"{path.relative_to(ROOT)}: portable skill frontmatter is not minimal"
        )

    portable_body = body.lstrip()
    if canonical == "claude-code":
        prefix = f"{CLAUDE_RUNTIME_PRELUDE}\n\n"
        if not portable_body.startswith(prefix):
            errors.append(
                f"{path.relative_to(ROOT)}: Claude runtime prelude is missing"
            )
            return portable_body
        portable_body = portable_body[len(prefix) :]
    elif CLAUDE_RUNTIME_PRELUDE in portable_body:
        errors.append(
            f"{path.relative_to(ROOT)}: non-Claude target contains Claude prelude"
        )
    return portable_body


def validate_runtime_file(
    target_root: Path, relative: str, target: str, errors: list[str]
) -> None:
    generated = target_root / relative
    if not generated.is_file():
        errors.append(f"dist/{target}: missing planning runtime file {relative}")
        return
    actual = generated.read_text(encoding="utf-8-sig")
    expected = source_runtime_body(relative)
    if actual != expected:
        errors.append(f"dist/{target}: planning runtime drift in {relative}")


def validate_skill(
    target_root: Path,
    target: str,
    canonical: str,
    skill: str,
    errors: list[str],
) -> None:
    relative = f"skills/{skill}/SKILL.md"
    generated = target_root / relative
    if not generated.is_file():
        errors.append(f"dist/{target}: missing planning skill {skill}")
        return
    actual = generated_skill_body(generated, canonical, errors)
    expected = source_runtime_body(relative)
    if actual != expected:
        errors.append(f"dist/{target}: planning skill body drift in {skill}")


def file_inventory(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def validate_alias(alias: str, canonical: str, errors: list[str]) -> None:
    alias_root = DIST / alias
    canonical_root = DIST / canonical
    if not alias_root.is_dir() or not canonical_root.is_dir():
        errors.append(f"dist/{alias}: alias or canonical target is missing")
        return
    if file_inventory(alias_root) != file_inventory(canonical_root):
        errors.append(f"dist/{alias}: target must be byte-identical to {canonical}")


def validate() -> list[str]:
    errors: list[str] = []
    try:
        manifest = load_manifest()
    except Exception as exc:
        return [f"Cannot parse bundle-manifest.json: {exc}"]

    targets = manifest.get("targets", {})
    aliases = manifest.get("target_aliases", {})
    for target in (*targets, *aliases):
        canonical = aliases.get(target, target)
        root = DIST / target
        if not root.is_dir():
            errors.append(f"dist/{target}: generated target is missing")
            continue
        for relative in (*PLANNING_COMMON, *PLANNING_TEMPLATES):
            validate_runtime_file(root, relative, target, errors)
        for skill in PLANNING_SKILLS:
            validate_skill(root, target, canonical, skill, errors)

    for alias, canonical in aliases.items():
        validate_alias(alias, canonical, errors)

    for error in validate_context_budgets(generated=True):
        errors.append(f"planning target context budget: {error}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate generated planning parity and context budgets."
    )
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Planning contracts are equivalent across targets and within budgets.")


if __name__ == "__main__":
    main()
