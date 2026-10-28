"""Validate the Kimi project artifact without claiming live client behavior."""

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
    return errors


if __name__ == "__main__":
    errors = validate()
    print(
        "\n".join(errors)
        if errors
        else "Kimi target structure passed; live client verification not performed."
    )
    raise SystemExit(bool(errors))
