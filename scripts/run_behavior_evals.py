#!/usr/bin/env python3
"""Prepare isolated fixtures; optionally run a trusted client adapter, never grade it."""

import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals/live/scenarios.json"


def scenarios():
    return json.loads(CASES.read_text())["cases"]


def snapshot(root):
    return {
        p.relative_to(root).as_posix(): (
            "symlink:" + os.readlink(p)
            if p.is_symlink()
            else hashlib.sha256(p.read_bytes()).hexdigest()
        )
        for p in sorted(root.rglob("*"))
        if p.is_file() or p.is_symlink()
    }


def prepare(case, target, output):
    output = output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError("Use an output directory outside the source repository")
    generated = ROOT / "dist" / target
    if not generated.is_dir():
        raise ValueError("Build portable targets before preparing a run")
    output.mkdir(parents=True, exist_ok=False)
    workspace = output / "workspace"
    shutil.copytree(ROOT / "evals/live/fixture", workspace)
    kit = workspace / ("webdev-agent-kit" if target == "claude-code" else ".agents")
    shutil.copytree(generated, kit)
    # Explicit prompt routing works across clients without overwriting host pointers.
    entry = kit.relative_to(workspace) / "AGENTS.md"
    if not (workspace / entry).is_file():
        raise ValueError("Generated target is missing runtime instructions")
    context = kit / "project"
    if case["id"] in {"domain", "resume"}:
        context.mkdir(exist_ok=True)
    if case["id"] == "domain":
        (context / "domain-glossary.md").write_text(
            "# Confirmed domain vocabulary\n"
            "Workspace: a shared area owned by a team; code identifier Workspace.\n"
            "Member: a person's membership in a Workspace, not the Workspace itself.\n"
            "Evidence: confirmed fixture product specification.\n"
        )
    if case["id"] == "resume":
        page = workspace / "index.html"
        page.write_text(
            page.read_text().replace("background: teal", "background: navy")
        )
        (context / "active-goals.md").write_text(
            "# G-001 Preferences\nAC-001: save button background is navy.\n"
            "AC-002: saved theme survives reload.\nNo new tests or dependencies.\n"
        )
        (context / "active-plan.md").write_text(
            "# G-001 Execution\nS-001 [AC-001]: completed; inspected CSS: navy.\n"
            "S-002 [AC-002]: pending; save and reload to verify persistence.\n"
            "blocked_by: S-001\nNext exact step: inspect theme storage keys.\n"
            "Coverage: AC-001 -> S-001 -> CSS inspection -> verified; "
            "AC-002 -> S-002 -> save/reload -> planned.\n"
        )
    prompt = output / "prompt.txt"
    prompt.write_text(
        f"Read {entry.as_posix()} and the matching skill. "
        "Work only in this disposable fixture. No external writes or installs.\n"
        "The page can be served with python -m http.server 8765 --bind 127.0.0.1 "
        "from the workspace if browser evidence is needed.\n\n" + case["prompt"] + "\n"
    )
    (output / "rubric.json").write_text(json.dumps(case["rubric"], indent=2) + "\n")
    return workspace, prompt


def run_adapter(command, workspace, prompt, output, timeout):
    trace = output / "trace.jsonl"
    with (output / "adapter.log").open("wb") as log:
        try:
            process = subprocess.Popen(
                [*command, str(workspace), str(prompt), str(trace)],
                cwd=workspace,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=os.name == "posix",
            )
        except OSError as exc:
            log.write(str(exc).encode())
            return "launch-error", None
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
            process.wait()
            return "timeout", None
    if code:
        return "adapter-failed", code
    if not trace.is_file() or trace.stat().st_size == 0:
        return "missing-trace", code
    return "completed-unverified", code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--case", choices=[c["id"] for c in scenarios()])
    parser.add_argument("--target", choices=["codex", "claude-code", "cursor"])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--client", default="unrecorded")
    parser.add_argument("--model", default="unrecorded")
    parser.add_argument("--timeout", type=float, default=600)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.list:
        print("\n".join(c["id"] for c in scenarios()))
        return 0
    if not args.case or not args.target or not args.output or args.timeout <= 0:
        parser.error("--case, --target, --output and positive timeout are required")
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    try:
        case = next(c for c in scenarios() if c["id"] == args.case)
        workspace, prompt = prepare(case, args.target, args.output)
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    output = args.output.resolve()
    before = snapshot(workspace)
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True
    ).stdout.strip()
    result = {
        "case": args.case,
        "target": args.target,
        "kit_version": json.loads((ROOT / "bundle-manifest.json").read_text())[
            "version"
        ],
        "kit_commit": commit,
        "client": args.client,
        "model": args.model,
        "status": "not-run",
        "behavior_assessment": "unverified",
        "before": before,
    }
    # Write before execution so interrupted runs cannot look completed.
    result_path = output / "result.json"
    result_path.write_text(json.dumps(result, indent=2) + "\n")
    if command:
        result["status"] = "running"
        result_path.write_text(json.dumps(result, indent=2) + "\n")
        result["status"], result["exit_code"] = run_adapter(
            command, workspace, prompt, output, args.timeout
        )
    after = snapshot(workspace)
    result["changed_files"] = [
        name
        for name in sorted(before.keys() | after.keys())
        if before.get(name) != after.get(name)
    ]
    result["after"] = after
    result_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"result": str(result_path), "status": result["status"]}))
    return 0 if result["status"] in {"not-run", "completed-unverified"} else 1


if __name__ == "__main__":
    sys.exit(main())
