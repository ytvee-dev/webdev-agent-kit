#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_VERSION_FILES = (
    (".codex-plugin/plugin.json", "version"),
    (".claude-plugin/plugin.json", "version"),
    ("tool-capabilities-manifest.json", "version"),
)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(generated=False):
    errors = []
    try:
        manifest = load_json(ROOT / "bundle-manifest.json")
    except Exception as exc:
        return [f"Cannot parse bundle-manifest.json: {exc}"]
    version = manifest.get("version")

    for relative_path, field in SOURCE_VERSION_FILES:
        try:
            value = load_json(ROOT / relative_path).get(field)
        except Exception as exc:
            errors.append(f"Cannot parse {relative_path}: {exc}")
            continue
        if value != version:
            errors.append(f"{relative_path} {field} must match version {version}")

    for path in sorted((ROOT / "evals").glob("*.json")):
        try:
            value = load_json(path).get("version")
        except Exception as exc:
            errors.append(f"Cannot parse {path.relative_to(ROOT)}: {exc}")
            continue
        if value != version:
            errors.append(f"{path.relative_to(ROOT)} version must be {version}")

    if generated:
        expected_targets = (
            *manifest.get("targets", {}),
            *manifest.get("target_aliases", {}),
        )
        for target in expected_targets:
            root = ROOT / "dist" / target
            tool_manifest = root / "tool-capabilities-manifest.json"
            if not tool_manifest.is_file():
                errors.append(f"dist/{target} is missing tool capability metadata")
                continue
            if load_json(tool_manifest).get("version") != version:
                errors.append(f"dist/{target} tool metadata version must be {version}")

        generated_plugins = (
            ROOT / "dist" / "codex" / ".codex-plugin" / "plugin.json",
            ROOT / "dist" / "claude-code" / ".claude-plugin" / "plugin.json",
        )
        for path in generated_plugins:
            if not path.is_file():
                errors.append(f"{path.relative_to(ROOT)} is required")
            elif load_json(path).get("version") != version:
                errors.append(f"{path.relative_to(ROOT)} version must be {version}")

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate source and generated release version alignment."
    )
    parser.add_argument(
        "--generated",
        action="store_true",
        help="Also validate generated target metadata versions.",
    )
    args = parser.parse_args()
    errors = validate(generated=args.generated)
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    scope = "source and generated" if args.generated else "source"
    print(f"Version metadata is consistent for {scope} artifacts.")


if __name__ == "__main__":
    main()
