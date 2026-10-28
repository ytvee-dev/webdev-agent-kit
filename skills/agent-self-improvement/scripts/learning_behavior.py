"""Bounded live A/B skill evaluation against observable fixture state.

This is a workflow evaluation, not an application benchmark or a model ranking.
Cases and grading live outside the evaluated agent's writable workspace.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

from learning_cycle import read_json, write_json


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(
                p.read_text(encoding="utf-8-sig").encode("utf-8") if p.name == "SKILL.md" else p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file() and "__pycache__" not in p.parts}


def grade(root, case):
    """Evaluate actual persisted state, never the agent's final prose."""
    findings = []
    try:
        # Windows PowerShell emits UTF-8 with a signature. It does not alter the
        # JSON state or the behavior under evaluation; accept both encodings.
        state = json.loads((root / "memory.json").read_text(encoding="utf-8-sig"))
        expected = case["expected"]
        for identifier, outcome in expected["records"].items():
            if state["records"].get(identifier, {}).get("outcome") != outcome:
                findings.append("unexpected record outcome: " + identifier)
        if (root / "rule.txt").read_text(encoding="utf-8") != expected["rule"]:
            findings.append("unexpected rule contents")
        if state.get("apply_count") != expected["apply_count"]:
            findings.append("duplicate or missing application")
        if state.get("behavioral_passed") != expected["behavioral_passed"]:
            findings.append("incorrect behavioral certification")
        if state.get("history", [])[:len(case["initial"]["history"])] != case["initial"]["history"]:
            findings.append("history was rewritten")
        for identifier in expected.get("reason_required", []):
            if not str(state["records"].get(identifier, {}).get("reason", "")).strip():
                findings.append("missing reason: " + identifier)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        findings.append("invalid persisted state: " + str(exc))
    return findings


def run_trial(args, case, variant, repeat):
    directory = args.output / f'{case["id"]}-{variant}-{repeat}'
    if directory.exists():
        raise ValueError("Refusing to overwrite existing trial: " + str(directory))
    workspace = directory / "workspace"
    workspace.mkdir(parents=True)
    source = getattr(args, variant)
    shutil.copytree(source, workspace / "skill", ignore=shutil.ignore_patterns("__pycache__"))
    write_json(workspace / "memory.json", case["initial"])
    (workspace / "rule.txt").write_text(case["initial_rule"], encoding="utf-8")
    write_json(workspace / "evidence.json", case["evidence"])
    prompt = ("Use the agent-self-improvement skill at skill/SKILL.md and its relevant references. "
              "This is an isolated workflow fixture: memory.json represents the processing ledger, "
              "rule.txt the installed rule, evidence.json the available evidence. The JSON fixture "
              "replaces database I/O only; apply the skill's decision rules to it. "
              "Perform the task using tools, persist decisions in memory.json and any authorized "
              "rule change in rule.txt. Preserve history and unrelated records. Do not modify skill/, "
              "The top-level behavioral_passed field describes a newly executed live evaluation, "
              "not historical checks referenced by a proposal. "
              "invoke other agents, access other paths or network, or install anything. "
              "Any claim of completion must follow a read of the resulting files.\nTASK:\n" + case["task"])
    (directory / "prompt.txt").write_text(prompt, encoding="utf-8")
    command = ["codex", "exec", "--ignore-user-config", "--ephemeral", "--skip-git-repo-check",
               "--sandbox", "workspace-write", "--model", args.model,
               "-c", "model_reasoning_effort=" + json.dumps(args.effort), "--json", "-"]
    # Ignoring user config also drops the Windows sandbox backend. Keep the
    # workspace boundary and explicitly select the installed native backend.
    if os.name == "nt":
        command[2:2] = ["-c", 'windows.sandbox="elevated"']
    write_json(directory / "command.json", command)
    start = time.monotonic()
    status, stdout, stderr = "completed", "", ""
    try:
        proc = subprocess.Popen(command, cwd=workspace, text=True, encoding="utf-8",
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        try:
            stdout, stderr = proc.communicate(prompt, timeout=min(args.timeout, 180))
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True,
                               timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                proc.kill()
            stdout, stderr = proc.communicate(timeout=10)
            status = "timeout"
        if proc.returncode:
            status = "environment_error" if status != "timeout" else status
        if "blocked by policy" in stderr or "Rejected(" in stderr:
            status = "environment_blocked"
    except subprocess.TimeoutExpired as exc:
        status = "timeout"
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
    except OSError as exc:
        status, stderr = "environment_error", str(exc)
    stdout = stdout.decode("utf-8", errors="replace") if isinstance(stdout, bytes) else stdout
    stderr = stderr.decode("utf-8", errors="replace") if isinstance(stderr, bytes) else stderr
    (directory / "trace.jsonl").write_text(stdout, encoding="utf-8")
    (directory / "stderr.txt").write_text(stderr, encoding="utf-8")
    events = []
    for line in stdout.splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            pass
    if status == "completed" and not any(e.get("type") == "turn.completed" for e in events):
        status = "environment_error"
    failures = grade(workspace, case)
    executed = [e for e in events if e.get("type") == "item.completed"
                and e.get("item", {}).get("type") in {"command_execution", "mcp_tool_call", "tool_call", "file_change"}]
    if not executed:
        failures.append("no completed tool action; prose alone cannot pass")
        if status == 'completed':
            status = 'environment_unverified'
    if snapshot(workspace / "skill") != snapshot(source):
        failures.append("evaluated skill was modified")
    result = {"case": case["id"], "variant": variant, "repeat": repeat, "status": status,
              "passed": status == "completed" and not failures, "failures": failures,
              "seconds": round(time.monotonic() - start, 3),
              "usage": [e.get("usage") for e in events if e.get("type") == "turn.completed"],
              "completed_tool_actions": len(executed),
              "cost": None}
    write_json(directory / "result.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--cases", type=Path, default=Path(__file__).parent.parent / "assets/behavior-cases.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--effort", required=True)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument('--verification-plan', type=Path,
                        help='Frozen proposal plan; cases must match its scenario IDs exactly')
    args = parser.parse_args()
    args.baseline, args.candidate, args.output = (p.resolve() for p in (args.baseline, args.candidate, args.output))
    cases = read_json(args.cases)["cases"]
    plan = read_json(args.verification_plan) if args.verification_plan else None
    repetitions, planned_trials = trial_plan(cases, plan)
    report = {"kind": "environment-outcome", "synthetic": False,
              "scope": "skill workflow on persisted fixtures; database mechanics covered separately",
              "model": args.model, "effort": args.effort, "planned_trials": planned_trials,
              "baseline": snapshot(args.baseline), "candidate": snapshot(args.candidate),
              "cases_sha256": hashlib.sha256(args.cases.read_bytes()).hexdigest(), "results": []}
    if plan:
        report['verification_plan'] = plan
    for case in cases:
        for repeat in range(1, repetitions + 1):
            # Counterbalance order across repeats.
            for variant in (("baseline", "candidate") if repeat == 1 else ("candidate", "baseline")):
                result = run_trial(args, case, variant, repeat)
                report["results"].append(result)
                report["passed"] = (len(report["results"]) == planned_trials and
                    all(r["passed"] for r in report["results"] if r["variant"] == "candidate") and
                    not any(r["status"] != "completed" for r in report["results"]))
                write_json(args.output / "report.json", report)
                print(json.dumps(result), flush=True)
                if result["status"] in {"environment_blocked", "environment_error", "environment_unverified"}:
                    return  # Do not spend 24 calls on the same environment failure.


def trial_plan(cases, plan=None):
    identifiers = {case['id'] for case in cases}
    if len(identifiers) != len(cases):
        raise ValueError('Duplicate scenario IDs')
    if plan is None:
        if len(cases) != 6:
            raise ValueError('Default suite requires six cases')
        return 2, 24
    from learning_workflow import verification_plan
    expected = verification_plan([], [{'find': 'same', 'replace': 'same'}]) if plan.get('risk') == 'standard' else verification_plan([])
    if plan != expected or identifiers != set(plan['scenarios']):
        raise ValueError('Cases or plan differ from frozen verification coverage')
    return plan['repetitions'], len(cases) * 2 * plan['repetitions']


if __name__ == "__main__":
    main()
