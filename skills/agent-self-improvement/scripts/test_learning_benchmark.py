"""Synthetic held-out A/B scoring tests; never claim a model run."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from learning_benchmark import compare_cases

CLI = Path(__file__).with_name("learning_benchmark.py")
STORE = Path(__file__).with_name("learning.py")
CYCLE = Path(__file__).with_name("learning_cycle.py")


class BenchmarkTests(unittest.TestCase):
    def test_assertion_scoring_catches_regression(self):
        cases = [{"id": "test", "skill": "skills/sample/SKILL.md",
                  "required": ["verify", "evidence"], "forbidden": ["guess"]}]
        answers = {"test": {"baseline": "Verify evidence, do not guess.",
                            "candidate": "Guess without verification."}}
        scores = compare_cases(cases, answers)
        self.assertTrue(scores[0]["regression"])
        self.assertLess(scores[0]["candidate"]["passed"], scores[0]["baseline"]["passed"])

    def test_offline_replay_never_unlocks_automatic_apply(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            repo = root / "skill-pack"
            target = repo / "skills" / "sample" / "SKILL.md"
            target.parent.mkdir(parents=True)
            target.write_text("---\nname: sample\ndescription: sample\n---\n\nVerify evidence.\n", encoding="utf-8")
            project = root / "project"
            project.mkdir()
            state = root / "state"

            def run(script, *arguments, data=None, expect=0):
                proc = subprocess.run(
                    [sys.executable, str(script), *arguments],
                    input=data, capture_output=True, text=True,
                )
                self.assertEqual(proc.returncode, expect, proc.stderr)
                return json.loads(proc.stdout) if expect == 0 else proc

            run(STORE, "--state", str(state), "on", "--project", str(project))
            event = run(
                STORE, "--state", str(state), "capture", "--project", str(project),
                data=json.dumps({"client": "codex", "session_id": "a", "message_id": "m",
                                 "kind": "user_correction", "content": "Verify with evidence"}),
            )
            offline = root / "proposal.json"
            offline.write_text(json.dumps({
                "schema_version": 1, "changes": [{
                    "path": "skills/sample/SKILL.md",
                    "find": "Verify evidence.",
                    "replace": "Verify evidence and report the check.",
                    "evidence_ids": [event["id"]],
                }],
            }), encoding="utf-8")
            proposed = run(
                CYCLE, "--state", str(state), "propose", "--project", str(project),
                "--repo", str(repo), "--proposal-file", str(offline),
            )
            accepted = run(CYCLE, "--state", str(state), "check",
                           "--repo", str(repo), "--proposal", proposed["proposal"])
            self.assertTrue(accepted["structural_passed"])
            fixtures = root / "cases.json"
            fixtures.write_text(json.dumps({"cases": [{
                "id": "new-case", "skill": "skills/sample/SKILL.md",
                "task": "Explain verification", "required": ["evidence"], "forbidden": ["guess"],
            }]}), encoding="utf-8")
            replay = root / "replay.json"
            replay.write_text(json.dumps({"new-case": {
                "baseline": "Evidence is required.",
                "candidate": "Evidence and checked behavior are required.",
            }}), encoding="utf-8")
            scored = run(CLI, "--repo", str(repo), "--proposal", proposed["proposal"],
                         "--cases", str(fixtures), "--replay-responses", str(replay))
            self.assertTrue(scored["synthetic"])
            self.assertFalse(scored["behavioral_passed"])
            blocked = run(CYCLE, "--state", str(state), "apply", "--repo", str(repo),
                          "--proposal", proposed["proposal"], "--approve", expect=1)
            self.assertIn("benchmark", blocked.stderr.lower())
            self.assertIn("Verify evidence.", target.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
