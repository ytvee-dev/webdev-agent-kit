#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(script):
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Validate schemas, source metadata, skill evals, then build and validate Codex and Claude targets.")
    parser.parse_args()

    schema_code = run("validate_schemas.py")
    if schema_code:
        sys.exit(schema_code)
    source_code = run("validate_source_bundle.py")
    if source_code:
        sys.exit(source_code)
    eval_code = run("validate_skill_evals.py")
    if eval_code:
        sys.exit(eval_code)
    build_code = run("build_skill_targets.py")
    if build_code:
        sys.exit(build_code)
    codex_code = run("validate_codex_skill_pack.py")
    claude_code = run("validate_claude_skill_pack.py")
    sys.exit(codex_code or claude_code)


if __name__ == "__main__":
    main()
