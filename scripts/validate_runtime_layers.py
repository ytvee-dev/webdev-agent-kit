#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "bundle-manifest.json"
EXPECTED_CORE = "common/core/runtime-core-policy.md"
EXPECTED_PROFILE = "react-typescript"
EXPECTED_PROFILES = {
    EXPECTED_PROFILE: "profiles/react-typescript/PROFILE.md",
}
EXPECTED_ADAPTERS = {
    "claude-code": "adapters/claude-code.md",
    "codex": "adapters/codex.md",
    "cursor": "adapters/cursor.md",
}
CLIENT_SPECIFIC_PATTERNS = (
    r"\bCodex\b",
    r"\bClaude(?: Code)?\b",
    r"\bCursor\b",
    r"AGENTS\.md",
    r"CLAUDE\.md",
    r"\.codex(?:-plugin)?",
    r"\.claude-plugin",
    r"\.cursor",
    r"agents/openai\.yaml",
)
CORE_HEADINGS = (
    "Authority And Evidence",
    "Context And Execution",
    "Safety And Approval",
    "Verification",
    "Output Economy",
)
ADAPTER_MARKERS = {
    "claude-code": (
        ".claude-plugin/plugin.json",
        "@.agents/AGENTS.md",
        "agents/openai.yaml",
    ),
    "codex": (
        ".agents/AGENTS.md",
        ".agents/skills",
        "agents/openai.yaml",
    ),
    "cursor": (
        ".cursor/rules/webdev-agent-kit.mdc",
        ".agents/AGENTS.md",
        ".agents/skills",
    ),
}


def is_safe_path(value):
    if not isinstance(value, str) or not value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def load_manifest(errors):
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"Cannot read bundle-manifest.json: {exc}")
        return {}


def read_text(relative_path, errors):
    if not is_safe_path(relative_path):
        errors.append(f"Runtime layer path is not safe: {relative_path!r}")
        return ""
    path = ROOT / relative_path
    if not path.is_file():
        errors.append(f"Runtime layer file does not exist: {relative_path}")
        return ""
    return path.read_text(encoding="utf-8-sig")


def validate_neutral_layer(label, text, word_limit, errors):
    for pattern in CLIENT_SPECIFIC_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"{label} contains client-specific term matching {pattern}")
    if len(text.split()) > word_limit:
        errors.append(f"{label} exceeds the {word_limit}-word context budget")


def validate_source_layers(manifest, errors):
    core_path = manifest.get("portable_core")
    profiles = manifest.get("profiles")
    adapters = manifest.get("adapters")
    default_profile = manifest.get("default_profile")

    if core_path != EXPECTED_CORE:
        errors.append(f"portable_core must be {EXPECTED_CORE}")
    if profiles != EXPECTED_PROFILES:
        errors.append("profiles must declare only the react-typescript profile")
    if adapters != EXPECTED_ADAPTERS:
        errors.append("adapters must match the three canonical runtime targets")
    if default_profile != EXPECTED_PROFILE:
        errors.append(f"default_profile must be {EXPECTED_PROFILE}")
    if isinstance(profiles, dict) and list(profiles) != sorted(profiles):
        errors.append("bundle-manifest.json profiles must be sorted")
    if isinstance(adapters, dict) and list(adapters) != sorted(adapters):
        errors.append("bundle-manifest.json adapters must be sorted")

    core = read_text(core_path, errors) if isinstance(core_path, str) else ""
    profile_path = profiles.get(default_profile) if isinstance(profiles, dict) else None
    profile = read_text(profile_path, errors) if isinstance(profile_path, str) else ""

    validate_neutral_layer("portable core", core, 400, errors)
    validate_neutral_layer("react-typescript profile", profile, 350, errors)
    for heading in CORE_HEADINGS:
        if f"## {heading}" not in core:
            errors.append(f"portable core is missing heading: {heading}")
    if "local project conventions override profile defaults" not in profile.lower():
        errors.append("profile must declare the local-convention override boundary")

    if isinstance(adapters, dict):
        for target, relative_path in adapters.items():
            adapter = read_text(relative_path, errors)
            if len(adapter.split()) > 225:
                errors.append(f"{relative_path} exceeds the 225-word adapter budget")
            for marker in ADAPTER_MARKERS.get(target, ()):
                if marker not in adapter:
                    errors.append(f"{relative_path} is missing client marker: {marker}")

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8-sig")
    for relative_path in (EXPECTED_CORE, EXPECTED_PROFILES[EXPECTED_PROFILE]):
        if relative_path not in agents:
            errors.append(f"AGENTS.md does not route through {relative_path}")


def validate_generated_layers(manifest, errors):
    targets = manifest.get("targets", {})
    aliases = manifest.get("target_aliases", {})
    profiles = manifest.get("profiles", {})
    default_profile = manifest.get("default_profile")
    core_path = manifest.get("portable_core")
    profile_path = profiles.get(default_profile)

    for output_name in (*targets, *aliases):
        canonical = aliases.get(output_name, output_name)
        root = ROOT / "dist" / output_name
        if not root.is_dir():
            errors.append(f"dist/{output_name} does not exist")
            continue
        for relative_path in (core_path, profile_path, EXPECTED_ADAPTERS[canonical]):
            if (
                not isinstance(relative_path, str)
                or not (root / relative_path).is_file()
            ):
                errors.append(
                    f"dist/{output_name} is missing runtime layer {relative_path}"
                )
        for target, adapter_path in EXPECTED_ADAPTERS.items():
            if target != canonical and (root / adapter_path).exists():
                errors.append(
                    f"dist/{output_name} must not include the {target} adapter"
                )


def validate(generated=False):
    errors = []
    manifest = load_manifest(errors)
    if manifest:
        validate_source_layers(manifest, errors)
        if generated:
            validate_generated_layers(manifest, errors)
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate portable core, project profile, and client adapters."
    )
    parser.add_argument(
        "--generated",
        action="store_true",
        help="Also validate generated target layer selection.",
    )
    args = parser.parse_args()
    errors = validate(generated=args.generated)
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    scope = "source and generated" if args.generated else "source"
    print(f"Runtime policy layers are valid for {scope} artifacts.")


if __name__ == "__main__":
    main()
