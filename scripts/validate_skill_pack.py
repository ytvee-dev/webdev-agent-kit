#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(script):
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT)
    return result.returncode


def main():
    build_code = run("build_skill_targets.py")
    if build_code:
        sys.exit(build_code)
    codex_code = run("validate_codex_skill_pack.py")
    claude_code = run("validate_claude_skill_pack.py")
    sys.exit(codex_code or claude_code)


if __name__ == "__main__":
    main()

