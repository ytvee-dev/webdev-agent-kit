#!/usr/bin/env python3
"""Held-out skill A/B evaluation. Synthetic replay cannot certify live quality."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from learning_cycle import read_json, render_changes, write_json


def score(text, required, forbidden):
    value = " ".join(text.casefold().split())
    present = [term for term in required if term.casefold() in value]
    absent = [term for term in forbidden if term.casefold() not in value]
    total = len(required) + len(forbidden)
    return {
        "passed": len(present) + len(absent),
        "total": total,
        "required_present": present,
        "forbidden_absent": absent,
    }


def run_answer(engine, task, instructions, timeout):
    prompt = (
        "Perform this hypothetical agent task as a concise response. "
        "Follow the skill's procedures; do not execute commands or edit files. "
        "Do not repeat the source skill verbatim.\n\n"
        "SKILL:\n" + instructions + "\n\nTASK:\n" + task
    )
    with tempfile.TemporaryDirectory(prefix="learning-benchmark-") as scratch:
        root = Path(scratch)
        if engine == "codex":
            outfile = root / "answer.txt"
            command = [
                "codex", "exec", "--sandbox", "read-only",
                "--skip-git-repo-check", "--output-last-message", str(outfile), "-",
            ]
            result = subprocess.run(
                command, input=prompt, cwd=root, text=True, capture_output=True,
                timeout=timeout, check=False,
            )
            if result.returncode != 0 or not outfile.is_file():
                raise ValueError("Codex benchmark failed; inspect CLI authentication")
            return outfile.read_text(encoding="utf-8")
        if engine == "opencode":
            env = os.environ.copy()
            env["OPENCODE_CONFIG_CONTENT"] = json.dumps({
                "permission": {
                    "*": "deny", "read": "allow",
                },
            })
            command = ["opencode", "run", "--agent", "plan", "--format", "json", "--dir", str(root), prompt]
            result = subprocess.run(
                command, cwd=root, env=env, text=True, capture_output=True,
                timeout=timeout, check=False,
            )
            if result.returncode != 0:
                raise ValueError("OpenCode benchmark failed; inspect CLI authentication")
            parts = []
            for line in result.stdout.splitlines():
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                part = event.get("part") or {}
                if event.get("type") == "text" and isinstance(part.get("text"), str):
                    parts.append(part["text"])
            if not parts:
                raise ValueError("OpenCode produced no text output")
            return "".join(parts)
    raise ValueError("Unsupported benchmark engine")


def compare_cases(cases, answers):
    results = []
    for case in cases:
        required = case.get("required", [])
        forbidden = case.get("forbidden", [])
        if not required or not all(isinstance(s, str) and s for s in required + forbidden):
            raise ValueError("Cases require nonempty exact-string assertions")
        case_id = case["id"]
        baseline = score(answers[case_id]["baseline"], required, forbidden)
        candidate = score(answers[case_id]["candidate"], required, forbidden)
        results.append({"id": case_id, "baseline": baseline, "candidate": candidate,
                        "regression": candidate["passed"] < baseline["passed"]})
    return results


def evaluate(args):
    from learning_processing import lock
    proposal = Path(args.proposal).expanduser().resolve(strict=True)
    with lock(proposal.parent.parent, args.repo):
        return evaluate_locked(args)


def evaluate_locked(args):
    proposal_path = Path(args.proposal).expanduser().resolve(strict=True)
    proposal = read_json(proposal_path)
    repo = Path(args.repo).expanduser().resolve(strict=True)
    if proposal["repo"] != str(repo) or proposal["state"] != "needs_review":
        raise ValueError("Proposal is not structurally validated for this repository")
    cases_path = Path(args.cases).expanduser().resolve(strict=True)
    cases = read_json(cases_path)["cases"]
    if not isinstance(cases, list) or not cases:
        raise ValueError("Provide held-out cases before benchmarking")
    edits = render_changes(proposal, repo)
    changes = {name: (old, new) for name, old, new in edits}
    applicable = [case for case in cases if case.get("skill") in changes]
    if {case.get("skill") for case in applicable} != set(changes):
        raise ValueError("Every changed skill requires held-out cases")
    answers = {}
    replay = args.replay_responses is not None
    if replay:
        answers = read_json(args.replay_responses)
    elif not args.engine:
        raise ValueError("Select a model engine or offline replay")
    else:
        for case in applicable:
            old, new = changes[case["skill"]]
            task = case["task"]
            answers[case["id"]] = {
                "baseline": run_answer(args.engine, task, old, args.timeout),
                "candidate": run_answer(args.engine, task, new, args.timeout),
            }
    results = compare_cases(applicable, answers)
    regressions = [item["id"] for item in results if item["regression"]]
    complete = all(r["candidate"]["passed"] == r["candidate"]["total"] for r in results)
    passed = not regressions and complete
    proposal["checks"]["benchmark"] = {
        "timestamp": datetime.now(UTC).isoformat(),
        "engine": args.engine or "offline-replay",
        "fixture_sha256": hashlib.sha256(cases_path.read_bytes()).hexdigest(),
        "results": results,
        "passed": passed,
        "synthetic": replay,
    }
    proposal["checks"]["textual_tested"] = True
    proposal["checks"]["textual_passed"] = passed
    # Hypothetical responses are never evidence of executed actions.
    proposal["checks"]["behavioral_tested"] = False
    proposal["checks"]["behavioral_passed"] = False
    write_json(proposal_path, proposal)
    return {
        "result": "passed" if passed else "failed",
        "synthetic": replay,
        "behavioral_passed": proposal["checks"]["behavioral_passed"],
        "regressions": regressions,
        "cases": len(results),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--proposal", required=True)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--engine", choices=("codex", "opencode"))
    parser.add_argument("--replay-responses")
    parser.add_argument("--timeout", type=int, default=240)
    args = parser.parse_args()
    print(json.dumps(evaluate(args), ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(f"agent-learning-benchmark: {exc}", file=sys.stderr)
        sys.exit(1)
