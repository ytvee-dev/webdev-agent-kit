"""Validate the Kimi project artifact without claiming live client behavior."""

import json

from target_validation_common import (
    ROOT,
    validate_portable_skills,
    validate_runtime_exclusions,
)


def validate():
    target = ROOT / "dist/kimi"
    errors = validate_runtime_exclusions(target, "dist/kimi")
    for name in ("AGENTS.md", "adapters/kimi.md", "common/core/runtime-core-policy.md"):
        if not (target / name).is_file():
            errors.append("Missing Kimi runtime file: " + name)
    errors.extend(
        validate_portable_skills(target, "dist/kimi", require_openai_metadata=False)
    )
    for path in (target / "skills").glob("*/SKILL.md"):
        if "${KIMI_SKILL_DIR}/../../adapters/kimi.md" not in path.read_text(
            encoding="utf-8"
        ):
            errors.append("Missing Kimi policy prelude: " + str(path))
    for name in (".codex-plugin", ".claude-plugin", ".cursor"):
        if (target / name).exists():
            errors.append("Unexpected foreign client metadata: " + name)
    manifest = json.loads((ROOT / "bundle-manifest.json").read_text(encoding="utf-8"))
    plugin_path = target / "kimi.plugin.json"
    if not plugin_path.is_file():
        errors.append("Missing native Kimi plugin")
    else:
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        if plugin.get("version") != manifest["version"] or not plugin.get(
            "systemPrompt"
        ):
            errors.append("Invalid Kimi plugin version or startup instructions")
    for role in manifest["claude_agents"]:
        path = target / "agents" / (role + ".md")
        if not path.is_file():
            errors.append("Missing Kimi role: " + role)
        else:
            text = path.read_text(encoding="utf-8")
            if "subagents: []" not in text or "adapters/kimi.md" not in text:
                errors.append("Invalid Kimi role boundaries: " + role)
            if "adapters/claude-code.md" in text or "model:" in text:
                errors.append("Foreign Kimi role configuration: " + role)
    return errors


if __name__ == "__main__":
    errors = validate()
    print(
        "\n".join(errors)
        if errors
        else "Kimi target structure passed; live client verification not performed."
    )
    raise SystemExit(bool(errors))
