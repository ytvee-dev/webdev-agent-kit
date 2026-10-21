"""Offline tests for proposal generation, isolated checks, and approval gates."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).with_name("learning_cycle.py")
STORE = Path(__file__).with_name("learning.py")


class LearningCycleSmoke(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.state = self.base / "state"
        self.project = self.base / "project"
        self.repo = self.base / "skill-pack"
        self.project.mkdir()
        skill = self.repo / "skills" / "example" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text(
            "---\nname: example\ndescription: Test skill\n---\n\n"
            "Always verify before reporting.\n",
            encoding="utf-8",
        )
        self.skill = skill

    def call(self, cli, *args, payload=None, expect=0):
        result = subprocess.run(
            [sys.executable, str(cli), "--state", str(self.state), *args],
            input=payload, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expect, result.stderr)
        return json.loads(result.stdout) if expect == 0 else result

    def record(self):
        self.call(STORE, "on", "--project", str(self.project))
        response = self.call(
            STORE, "capture", "--project", str(self.project),
            payload=json.dumps({
                "client": "codex",
                "session_id": "session-a",
                "message_id": "message-1",
                "kind": "user_correction",
                "content": "Please verify before reporting.",
            }),
        )
        return response["id"]

    def test_full_offline_cycle(self):
        event_id = self.record()
        proposal = self.base / "input.json"
        proposal.write_text(json.dumps({
            "schema_version": 1,
            "changes": [{
                "path": "skills/example/SKILL.md",
                "find": "Always verify before reporting.",
                "replace": "Always verify the affected functionality before reporting.",
                "reason": "Observed correction",
                "evidence_ids": [event_id],
            }],
        }), encoding="utf-8")
        result = self.call(
            CLI, "propose", "--project", str(self.project),
            "--repo", str(self.repo), "--proposal-file", str(proposal),
        )
        path = result["proposal"]
        self.assertEqual(result["result"], "pending_validation")
        self.call(CLI, "apply", "--repo", str(self.repo), "--proposal", path, expect=1)
        validation = self.call(
            CLI, "check", "--repo", str(self.repo), "--proposal", path,
        )
        self.assertEqual(validation["state"], "needs_review")
        self.assertFalse(validation["behavioral_tested"])
        self.assertIn("Always verify before", self.skill.read_text())
        result = self.call(
            CLI, "apply", "--repo", str(self.repo), "--proposal", path, "--approve",
        )
        self.assertEqual(result["result"], "applied")
        self.assertIn("affected functionality", self.skill.read_text())
        # Project purge also removes derived training suggestions and diffs.
        self.call(STORE, "purge", "--project", str(self.project))
        self.assertFalse(Path(path).exists())
        self.assertFalse(Path(path).with_suffix(".diff").exists())

    def test_scheduled_offline_cycle_skips_unchanged_evidence(self):
        event_id = self.record()
        source = self.base / "scheduled.json"
        source.write_text(json.dumps({
            "schema_version": 1,
            "changes": [{
                "path": "skills/example/SKILL.md",
                "find": "Always verify before reporting.",
                "replace": "Always verify the affected functionality before reporting.",
                "evidence_ids": [event_id],
            }],
        }), encoding="utf-8")
        first = self.call(
            CLI, "auto", "--repo", str(self.repo),
            "--project", str(self.project), "--proposal-file", str(source),
        )
        self.assertEqual(first["state"], "needs_review")
        second = self.call(
            CLI, "auto", "--repo", str(self.repo),
            "--project", str(self.project), "--proposal-file", str(source),
        )
        self.assertEqual(second["result"], "no_change")
        self.assertIn("No new evidence", second["reason"])

    def test_unknown_evidence_is_rejected(self):
        self.record()
        proposal = self.base / "invalid.json"
        proposal.write_text(json.dumps({
            "schema_version": 1,
            "changes": [{
                "path": "skills/example/SKILL.md",
                "find": "Always verify before reporting.",
                "replace": "Skip all checks.",
                "evidence_ids": ["invented"],
            }],
        }), encoding="utf-8")
        result = self.call(
            CLI, "propose", "--project", str(self.project),
            "--repo", str(self.repo), "--proposal-file", str(proposal),
            expect=1,
        )
        self.assertIn("evidence", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
