#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

from build_skill_targets import split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NATIVE_FIELDS = {"name", "description", "model", "color", "tools"}
READ_TOOLS = {"Read", "Glob", "Grep"}
WRITE_TOOLS = READ_TOOLS | {"Edit", "Write", "Bash"}
WRITE_ROLES = {"wdk-worker", "wdk-worker-light", "wdk-complex"}
EXPECTED_ROLES = {
    "wdk-lookup",
    "wdk-worker-light",
    "wdk-worker",
    "wdk-complex",
    "wdk-reviewer-light",
    "wdk-reviewer",
    "wdk-reviewer-deep",
    "wdk-architect",
    "wdk-architect-deep",
}


def validate_agents(directory, *, generated=True):
    errors = []
    paths = sorted(directory.glob("*.md"))
    names = {path.stem for path in paths}
    if names != EXPECTED_ROLES:
        errors.append(
            f"{directory}: Claude agent inventory is incomplete or unexpected"
        )
    for path in paths:
        fields, body = split_frontmatter(path.read_text(encoding="utf-8"))
        if generated and set(fields) != NATIVE_FIELDS:
            errors.append(f"{path.name}: native agent fields must be portable")
        for key in NATIVE_FIELDS - {"tools"}:
            if not fields.get(key, "").strip("'\""):
                errors.append(f"{path.name}: missing {key}")
        if fields.get("name", "").strip("'\"") != path.stem:
            errors.append(f"{path.name}: name must match the filename")
        if fields.get("model", "").strip("'\"") != "inherit":
            errors.append(f"{path.name}: shipped models must inherit user selection")
        try:
            tools = json.loads(fields.get("tools", "null"))
            expected = WRITE_TOOLS if path.stem in WRITE_ROLES else READ_TOOLS
            if (
                not isinstance(tools, list)
                or set(tools) != expected
                or len(tools) != len(expected)
            ):
                errors.append(f"{path.name}: unexpected role tool permissions")
        except (ValueError, TypeError):
            errors.append(
                f"{path.name}: tools must be an explicit JSON-compatible list"
            )
        for marker in (
            "absolute plugin root",
            "host root",
            "Do not delegate",
            "retry budget",
            "evidence",
        ):
            if marker not in body:
                errors.append(f"{path.name}: missing handoff boundary {marker}")
    return errors


def validate(*, generated=False):
    manifest = json.loads((ROOT / "bundle-manifest.json").read_text())
    errors = []
    if manifest.get("claude_agents") != sorted(EXPECTED_ROLES):
        errors.append("bundle-manifest.json must declare the nine sorted Claude roles")
    errors.extend(validate_agents(ROOT / "agents/claude-code", generated=False))
    if generated:
        for target in (*manifest["targets"], *manifest["target_aliases"]):
            canonical = manifest["target_aliases"].get(target, target)
            directory = ROOT / "dist" / target / "agents"
            if canonical == "claude-code":
                errors.extend(validate_agents(directory))
            elif directory.exists():
                errors.append(f"dist/{target}: must not ship native Claude agents")
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate Claude role inventory and permissions."
    )
    parser.add_argument("--generated", action="store_true")
    args = parser.parse_args()
    errors = validate(generated=args.generated)
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("Claude native roles, permissions and handoff contracts are valid.")


if __name__ == "__main__":
    main()
