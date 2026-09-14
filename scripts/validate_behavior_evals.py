#!/usr/bin/env python3
"""Validate live scenario fixtures and synthetic runner mechanics, not models."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from run_behavior_evals import ROOT, prepare, scenarios


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
        for target in ("codex", "claude-code", "cursor"):
            for case in cases:
                workspace, prompt = prepare(
                    case, target, root / f"{target}-{case['id']}"
                )
                if not prompt.is_file():
                    errors.append(f"{target}/{case['id']}: missing prompt")
                for name, content in case.get("files", {}).items():
                    if (workspace / name).read_text(encoding="utf-8") != content:
                        errors.append(f"{target}/{case['id']}: fixture content lost")
                if case["id"] in {"resume", "domain"}:
                    if not (workspace / ".agents/project").is_dir():
                        errors.append(f"{target}/{case['id']}: host context missing")
                if target == "claude-code":
                    if (workspace / "webdev-agent-kit/project").exists():
                        errors.append(f"{case['id']}: host facts leaked into plugin")
                if target == "cursor":
                    rule = workspace / ".cursor/rules/webdev-agent-kit.mdc"
                    if not rule.is_file() or (workspace / ".agents/.cursor").exists():
                        errors.append(
                            f"{case['id']}: Cursor native discovery root broken"
                        )
                if case["id"].startswith("screenshot-"):
                    reference = workspace.parent / "reference/index.html"
                    if not reference.is_file() or (workspace / "reference").exists():
                        errors.append(f"{case['id']}: reference isolation broken")
                if case["id"] == "resume":
                    if "background: navy" not in (workspace / "index.html").read_text():
                        errors.append(f"{target}: completed resume slice lost")
        for number, name in enumerate(
            (
                "../escape",
                "/absolute",
                "C:/escape",
                "dir\\escape",
                ".",
                "dir/../escape",
                "dir//file",
                ".agents/AGENTS.md",
                "webdev-agent-kit/common/policy.md",
                ".cursor/rules/webdev-agent-kit.mdc",
            )
        ):
            output = root / f"invalid-{number}"
            case = {"id": "invalid", "prompt": "invalid", "files": {name: "bad"}}
            try:
                prepare(case, "codex", output)
            except ValueError:
                if output.exists():
                    errors.append(
                        f"Invalid fixture wrote output before rejection: {name}"
                    )
            else:
                errors.append(f"Unsafe scenario path accepted: {name}")
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
                "--client-version",
                "synthetic-1",
                "--shell",
                "synthetic-shell",
                "--capability",
                "project_files",
            ]
            if mode == "launch":
                command += ["--", str(root / "missing-adapter")]
            elif mode != "prepare":
                command += ["--", sys.executable, str(adapter), mode]
            proc = subprocess.run(command, capture_output=True, text=True)
            result = json.loads((output / "result.json").read_text())
            if (
                result["client_version"] != "synthetic-1"
                or result["shell"] != "synthetic-shell"
                or result["reported_capabilities"] != ["project_files"]
                or not result["os"]
            ):
                errors.append(f"{mode}: run provenance metadata lost")
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
