#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "bundle-manifest.json"
CANONICAL_TARGETS = {"claude-code", "codex", "cursor"}
TARGET_ALIASES = {
    "claude": "claude-code",
    "vs-code-claude": "claude-code",
    "vs-code-codex": "codex",
}
REQUIRED_FIELDS = {
    "kind",
    "output",
    "install_mode",
    "entrypoint",
    "skills_root",
    "validator",
}


def is_safe_relative_path(value):
    if not isinstance(value, str) or not value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def validate_contract(name, contract):
    errors = []
    if not isinstance(contract, dict):
        return [f"targets.{name} must be an object"]

    fields = set(contract)
    if fields != REQUIRED_FIELDS:
        missing = sorted(REQUIRED_FIELDS - fields)
        unexpected = sorted(fields - REQUIRED_FIELDS)
        if missing:
            errors.append(f"targets.{name} is missing: {', '.join(missing)}")
        if unexpected:
            errors.append(
                f"targets.{name} has unexpected fields: {', '.join(unexpected)}"
            )

    kind = contract.get("kind")
    install_mode = contract.get("install_mode")
    if kind == "plugin" and install_mode != "plugin-install":
        errors.append(f"targets.{name} plugin must use plugin-install")
    if kind == "project-bundle" and install_mode != "project-root-extract":
        errors.append(f"targets.{name} project bundle must use project-root-extract")

    output = contract.get("output")
    if output != f"dist/{name}":
        errors.append(f"targets.{name}.output must be dist/{name}")

    for field in ("output", "entrypoint", "skills_root", "validator"):
        value = contract.get(field)
        if not is_safe_relative_path(value):
            errors.append(f"targets.{name}.{field} must be a safe relative path")

    validator = contract.get("validator")
    if is_safe_relative_path(validator) and not (ROOT / validator).is_file():
        errors.append(f"targets.{name}.validator does not exist: {validator}")

    return errors


def validate():
    errors = []
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"bundle-manifest.json cannot be parsed: {exc}"]

    targets = manifest.get("targets")
    aliases = manifest.get("target_aliases")
    if not isinstance(targets, dict):
        return ["bundle-manifest.json targets must be an object"]
    if not isinstance(aliases, dict):
        return ["bundle-manifest.json target_aliases must be an object"]

    if set(targets) != CANONICAL_TARGETS:
        errors.append(
            "bundle-manifest.json canonical targets must be: "
            + ", ".join(sorted(CANONICAL_TARGETS))
        )
    if aliases != TARGET_ALIASES:
        errors.append(
            "bundle-manifest.json target aliases do not match the runtime contract"
        )
    if list(targets) != sorted(targets):
        errors.append("bundle-manifest.json targets must be sorted alphabetically")
    if list(aliases) != sorted(aliases):
        errors.append(
            "bundle-manifest.json target aliases must be sorted alphabetically"
        )

    outputs = []
    for name, contract in targets.items():
        errors.extend(validate_contract(name, contract))
        if isinstance(contract, dict):
            outputs.append(contract.get("output"))
    if len(outputs) != len(set(outputs)):
        errors.append("canonical target outputs must be unique")

    for alias, target in aliases.items():
        if alias in targets:
            errors.append(
                f"target alias must not define an independent contract: {alias}"
            )
        if target not in targets:
            errors.append(f"target alias {alias} points to unknown target: {target}")

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate canonical runtime target and alias contracts."
    )
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Runtime target contracts are valid.")


if __name__ == "__main__":
    main()
