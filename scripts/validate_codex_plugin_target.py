#!/usr/bin/env python3

import argparse
import sys

from target_validation_common import ROOT, load_json

TARGET = ROOT / "dist" / "codex"


def validate():
    errors = []
    plugin_path = TARGET / ".codex-plugin" / "plugin.json"
    if not plugin_path.is_file():
        return ["dist/codex is missing .codex-plugin/plugin.json"]

    try:
        source = load_json(ROOT / "bundle-manifest.json")
        plugin = load_json(plugin_path)
    except Exception as exc:
        return [f"Cannot parse Codex plugin metadata: {exc}"]

    for field in ("name", "version"):
        if plugin.get(field) != source.get(field):
            errors.append(f"Codex plugin {field} must match bundle-manifest.json")
    if plugin.get("skills") != "./skills/":
        errors.append("Codex plugin skills must be './skills/'")
    if not (TARGET / "skills").is_dir():
        errors.append("Codex plugin skills root does not exist")
    if (TARGET / ".claude-plugin").exists():
        errors.append("Codex target must not include Claude plugin metadata")
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate the Codex plugin contract inside the Codex target."
    )
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Codex plugin target is valid.")


if __name__ == "__main__":
    main()
