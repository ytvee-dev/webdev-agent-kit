#!/usr/bin/env python3
"""Validate live scenario fixtures and synthetic runner mechanics, not models."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from run_behavior_evals import ROOT, scenarios


def validate():
    errors = []
    cases = scenarios()
    ids = [case.get("id") for case in cases]
    if len(ids) != len(set(ids)) or not all(ids):
        errors.append("Live scenario IDs must be present and unique")
    for case in cases:
        if not case.get("prompt") or len(case.get("rubric", [])) < 2:
            errors.append(f"Incomplete live scenario: {case.get('id')}")
    version = json.loads((ROOT / "bundle-manifest.json").read_text())["version"]
    if (
        json.loads((ROOT / "evals/live/scenarios.json").read_text())["version"]
        != version
    ):
        errors.append("Live scenario version must match the bundle")
    if errors:
        return errors
    runner = ROOT / "scripts/run_behavior_evals.py"
    with tempfile.TemporaryDirectory(prefix="webdev-runner-check-") as temp:
        root = Path(temp)
        adapter = root / "synthetic.py"
        adapter.write_text(
            "import sys, time\nfrom pathlib import Path\n"
            "mode, workspace, prompt, trace = sys.argv[1:]\n"
            "if mode == 'timeout': time.sleep(5)\n"
            "if mode == 'complete':\n"
            " Path(trace).write_text('synthetic adapter; not an AI run\\n')\n"
            " Path(workspace, 'observed.txt').write_text('synthetic')\n"
        )
        for mode, expected in [
            ("complete", "completed-unverified"),
            ("missing", "missing-trace"),
            ("timeout", "timeout"),
            ("launch", "launch-error"),
            ("prepare", "not-run"),
        ]:
            output = root / mode
            command = [
                sys.executable,
                str(runner),
                "--case",
                "review-defect",
                "--target",
                "codex",
                "--output",
                str(output),
                "--timeout",
                "0.2" if mode == "timeout" else "10",
            ]
            if mode == "launch":
                command += ["--", str(root / "missing-adapter")]
            elif mode != "prepare":
                command += ["--", sys.executable, str(adapter), mode]
            proc = subprocess.run(command, capture_output=True, text=True)
            result = json.loads((output / "result.json").read_text())
            if (
                result["status"] != expected
                or result["behavior_assessment"] != "unverified"
            ):
                errors.append(f"{mode}: incorrect runner/behavior status")
            success = expected in {"not-run", "completed-unverified"}
            if (proc.returncode == 0) != success:
                errors.append(f"{mode}: incorrect process exit status")
            if mode == "complete" and "observed.txt" not in result["changed_files"]:
                errors.append("Runner did not retain changed-file evidence")
            saved = (output / "result.json").read_bytes()
            repeat = subprocess.run(command, capture_output=True)
            if repeat.returncode == 0 or (output / "result.json").read_bytes() != saved:
                errors.append("Existing run was overwritten")
    return errors


def main():
    errors = validate()
    if errors:
        print("\n".join(errors))
        return 1
    print("Live scenarios and synthetic runner checks pass; no AI behavior evaluated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
