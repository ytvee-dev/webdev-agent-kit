#!/usr/bin/env python3
"""Exercise the real review packager and verify its bytes across built targets."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = "skills/frontend-quality-reviewer/scripts/review_package.py"
ARTIFACTS = (
    HELPER,
    "skills/frontend-quality-reviewer/references/review-handoffs.md",
    "common/subagent-handoff-rules.md",
    "templates/subagent-task.md",
    "templates/subagent-report.md",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generated", action="store_true")
    args = parser.parse_args()
    errors = []
    for name in ARTIFACTS:
        if not (ROOT / name).is_file():
            errors.append(f"Missing source handoff artifact: {name}")
    if args.generated and not errors:
        manifest = json.loads((ROOT / "bundle-manifest.json").read_text())
        for target in (*manifest["targets"], *manifest["target_aliases"]):
            for name in ARTIFACTS:
                path = ROOT / "dist" / target / name
                if not path.is_file():
                    errors.append(f"dist/{target}: missing {name}")
                elif name == HELPER and path.read_bytes() != (ROOT / name).read_bytes():
                    errors.append(f"dist/{target}: packager differs from tested source")
    if errors:
        print("\n".join(errors))
        return 1
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "scripts",
            "-p",
            "test_review_package.py",
        ],
        cwd=ROOT,
    )
    if result.returncode:
        return result.returncode
    print("Real Git packaging tests passed; no agent review or model run is claimed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
