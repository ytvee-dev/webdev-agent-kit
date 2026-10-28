"""Offline tests for proposal generation, isolated checks, and approval gates."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from learning_cycle import select_relevant_skills

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
            "decisions": [{"record_id": event_id, "outcome": "pending", "reason": "Observed correction"}],
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
        duplicate = self.call(CLI, "propose", "--project", str(self.project),
                              "--repo", str(self.repo), "--proposal-file", str(proposal))
        self.assertEqual(duplicate["result"], "no_change")
        receipts = self.call(CLI, "status", "--project", str(self.project))["records"]
        self.assertEqual({r["outcome"] for r in receipts}, {"pending"})
        self.assertTrue(all(r["used"] is False and r["used_at"] is None for r in receipts))
        self.call(CLI, "apply", "--repo", str(self.repo), "--proposal", path, expect=1)
        validation = self.call(
            CLI, "check", "--repo", str(self.repo), "--proposal", path,
        )
        self.assertEqual(validation["state"], "needs_review")
        self.assertFalse(validation["behavioral_tested"])
        self.assertIn("Always verify before", self.skill.read_text())
        result = self.call(
            CLI, "apply", "--repo", str(self.repo), "--proposal", path, "--approve",
            "--accept-unevaluated",
        )
        self.assertEqual(result["result"], "applied")
        self.assertIn("affected functionality", self.skill.read_text())
        receipts = self.call(CLI, "status", "--project", str(self.project))["records"]
        self.assertEqual({r["outcome"] for r in receipts}, {"applied"})
        self.assertTrue(all(r["used"] is True and r["used_at"] for r in receipts))
        # The usage flag is persisted in SQLite, not invented by the status renderer.
        import sqlite3
        from contextlib import closing
        with closing(sqlite3.connect(self.state / "experience.sqlite3")) as conn:
            usage = [json.loads(row[0]) for row in conn.execute(
                "SELECT details FROM learning_decisions WHERE outcome='applied'")]
        self.assertTrue(usage and all(row["used"] is True and row["used_at"] for row in usage))
        repeat = self.call(CLI, "propose", "--project", str(self.project),
                           "--repo", str(self.repo), "--proposal-file", str(proposal))
        self.assertEqual(repeat["result"], "no_change")
        recovered = self.call(CLI, "apply", "--repo", str(self.repo),
                              "--proposal", path, "--approve")
        self.assertEqual(recovered["result"], "already_applied")
        # Project purge also removes derived training suggestions and diffs.
        self.call(STORE, "purge", "--project", str(self.project))
        self.assertFalse(Path(path).exists())
        self.assertFalse(Path(path).with_suffix(".diff").exists())
        self.assertEqual(self.call(CLI, "status", "--project", str(self.project))["records"], [])

    def test_automatic_cycle_rejected_without_side_effects(self):
        from unittest.mock import patch
        from learning_cycle import auto
        with patch('learning_cycle.propose') as propose:
            with self.assertRaisesRegex(ValueError, 'Automatic learning is disabled'):
                auto(None)
            propose.assert_not_called()


    def test_forged_proposal_cannot_write_outside_skill_directory(self):
        self.record()
        outside = self.base / "important.txt"
        outside.write_text("Protected", encoding="utf-8")
        import hashlib

        source = self.base / "forged.json"
        source.write_text(json.dumps({
            "repo": str(self.repo.resolve()),
            "state": "pending_validation",
            "changes": [{
                "path": "../important.txt",
                "find": "Protected",
                "replace": "ATTACKED",
                "base_sha256": hashlib.sha256(b"Protected").hexdigest(),
            }],
        }), encoding="utf-8")
        result = self.call(CLI, "check", "--repo", str(self.repo),
                           "--proposal", str(source), expect=1)
        self.assertIn("allowed", result.stderr.lower())
        self.assertEqual(outside.read_text(encoding="utf-8"), "Protected")

    def test_selects_observed_skill_before_heuristic(self):
        inventory = {
            "skills/frontend-bugfix-debugger/SKILL.md": {"content": "A"},
            "skills/frontend-design-director/SKILL.md": {"content": "B"},
        }
        found = select_relevant_skills(
            inventory,
            [{"skills": ["frontend-bugfix-debugger"],
              "content": "The layout requires better design decisions"}],
        )
        self.assertEqual(next(iter(found)), "skills/frontend-bugfix-debugger/SKILL.md")

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

    def test_bounded_batch_preserves_remaining_work_and_rejects_old_change(self):
        first = self.record()
        second = self.call(STORE, "capture", "--project", str(self.project), payload=json.dumps({
            "client": "codex", "session_id": "session-b", "message_id": "message-2",
            "kind": "user_correction", "content": "Inspect resulting files."}))["id"]
        source = self.base / "batch.json"
        candidate = {"schema_version": 1, "changes": [{"path": "skills/example/SKILL.md",
            "find": "Always verify before reporting.", "replace": "Always verify outcomes before reporting.",
            "evidence_ids": [first]}], "decisions": [{"record_id": first, "outcome": "pending", "reason": "Observed correction"}]}
        source.write_text(json.dumps(candidate), encoding="utf-8")
        proposed = self.call(CLI, "propose", "--project", str(self.project), "--repo", str(self.repo),
                             "--batch-size", "1", "--proposal-file", str(source))
        self.call(CLI, "check", "--repo", str(self.repo), "--proposal", proposed["proposal"])
        self.call(CLI, "apply", "--repo", str(self.repo), "--proposal", proposed["proposal"],
                  "--approve", "--accept-unevaluated")
        receipts = self.call(CLI, "status", "--project", str(self.project))["records"]
        self.assertEqual({r["record_id"] for r in receipts}, {first})
        # Fresh work must not be used as a trigger to re-propose an old lesson.
        candidate["changes"][0].update(find="Always verify outcomes before reporting.", replace="Verify again.")
        candidate["decisions"] = [{"record_id": second, "outcome": "pending", "reason": "New correction"}]
        source.write_text(json.dumps(candidate), encoding="utf-8")
        rejected = self.call(CLI, "propose", "--project", str(self.project), "--repo", str(self.repo),
                             "--proposal-file", str(source), expect=1)
        self.assertIn("evidence", rejected.stderr.lower())
        candidate["changes"][0]["evidence_ids"] = [second]
        source.write_text(json.dumps(candidate), encoding="utf-8")
        next_proposal = self.call(CLI, "propose", "--project", str(self.project), "--repo", str(self.repo),
                                 "--proposal-file", str(source))
        self.assertEqual(next_proposal["result"], "pending_validation")
        import sqlite3
        from contextlib import closing
        with closing(sqlite3.connect(self.state / "experience.sqlite3")) as conn, conn:
            conn.execute("UPDATE events SET content='Evidence was corrected' WHERE id=?", (second,))
        stale = self.call(CLI, "check", "--repo", str(self.repo),
                          "--proposal", next_proposal["proposal"], expect=1)
        self.assertIn("Supporting event changed", stale.stderr)
        self.assertIn("Always verify outcomes", self.skill.read_text())


if __name__ == "__main__":
    unittest.main()
