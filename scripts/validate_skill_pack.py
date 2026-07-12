#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script, *args):
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args], cwd=ROOT
    )
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Validate schemas, source metadata, README boundaries, skill evals, then build and validate targets."
    )
    parser.parse_args()

    schema_code = run("validate_schemas.py", "--strict-graph")
    if schema_code:
        sys.exit(schema_code)
    target_contract_code = run("validate_target_contracts.py")
    if target_contract_code:
        sys.exit(target_contract_code)
    version_code = run("validate_version_consistency.py")
    if version_code:
        sys.exit(version_code)
    release_tag_code = run("validate_release_tag.py")
    if release_tag_code:
        sys.exit(release_tag_code)
    install_guide_code = run("validate_install_guides.py")
    if install_guide_code:
        sys.exit(install_guide_code)
    release_notes_code = run("build_release_notes.py", "--check")
    if release_notes_code:
        sys.exit(release_notes_code)
    capability_code = run("validate_tool_capabilities.py")
    if capability_code:
        sys.exit(capability_code)
    context_budget_code = run("validate_runtime_context_budget.py")
    if context_budget_code:
        sys.exit(context_budget_code)
    output_economy_code = run("validate_output_economy.py")
    if output_economy_code:
        sys.exit(output_economy_code)
    precedence_code = run("validate_policy_precedence.py")
    if precedence_code:
        sys.exit(precedence_code)
    planning_integrity_code = run("validate_planning_integrity.py")
    if planning_integrity_code:
        sys.exit(planning_integrity_code)
    test_policy_code = run("validate_test_policy.py")
    if test_policy_code:
        sys.exit(test_policy_code)
    runtime_layer_code = run("validate_runtime_layers.py")
    if runtime_layer_code:
        sys.exit(runtime_layer_code)
    readme_boundary_code = run("check_readme_boundary.py")
    if readme_boundary_code:
        sys.exit(readme_boundary_code)
    source_code = run("validate_source_bundle.py")
    if source_code:
        sys.exit(source_code)
    eval_code = run("validate_skill_evals.py")
    if eval_code:
        sys.exit(eval_code)
    build_code = run("build_skill_targets.py")
    if build_code:
        sys.exit(build_code)
    generated_layer_code = run("validate_runtime_layers.py", "--generated")
    if generated_layer_code:
        sys.exit(generated_layer_code)
    generated_context_code = run("validate_runtime_context_budget.py", "--generated")
    if generated_context_code:
        sys.exit(generated_context_code)
    planning_target_code = run("validate_planning_target_parity.py")
    if planning_target_code:
        sys.exit(planning_target_code)
    planning_smoke_code = run("validate_planning_smoke.py")
    if planning_smoke_code:
        sys.exit(planning_smoke_code)
    generated_version_code = run("validate_version_consistency.py", "--generated")
    if generated_version_code:
        sys.exit(generated_version_code)
    codex_project_code = run("validate_codex_project_target.py")
    codex_plugin_code = run("validate_codex_plugin_target.py")
    claude_code = run("validate_claude_plugin_target.py")
    cursor_code = run("validate_cursor_target.py")
    archive_code = run("validate_release_archive.py", "--build-fixtures")
    sys.exit(
        codex_project_code
        or codex_plugin_code
        or claude_code
        or cursor_code
        or archive_code
    )


if __name__ == "__main__":
    main()
