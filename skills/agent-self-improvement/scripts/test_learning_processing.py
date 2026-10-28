"""Regression scenarios for queue loss, stale evidence and crash recovery."""
import copy
import json
import sqlite3
import tempfile
import unittest
from argparse import Namespace
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from learning_cycle import (
    apply,
    certify,
    hash_text,
    processing_receipt,
    read_json,
    validate_candidate,
    validate_decisions,
    write_json,
)
from learning_processing import append, connect, eligible, lock


class ProcessingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.state = self.root / "state"
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.receipt = {"project_id": "p", "repo": str(self.repo), "skill_digest": "rules1",
                        "records": [{"id": "a", "digest": "a1"}, {"id": "b", "digest": "b1"}]}

    def test_partial_batch_does_not_close_unselected_work(self):
        append(self.state, self.receipt, "proposal", {"a": {"outcome": "applied", "reason": "verified"}})
        self.assertEqual(eligible(self.state, self.receipt), ["b"])
        append(self.state, self.receipt, "proposal", {"a": {"outcome": "applied", "reason": "verified"}})
        with closing(connect(self.state)) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM learning_decisions").fetchone()[0], 1)

    def test_changed_evidence_and_rules_reopen_only_related_records(self):
        append(self.state, self.receipt, "proposal", {k: {"outcome": "applied", "reason": "verified"} for k in ("a", "b")})
        changed = copy.deepcopy(self.receipt)
        changed["records"][0]["digest"] = "a2"
        self.assertEqual(eligible(self.state, changed), ["a"])
        changed = copy.deepcopy(self.receipt)
        changed["records"][0]["skill_digest"] = "rules2"
        self.assertEqual(eligible(self.state, changed), ["a"])

    def test_deferred_conditions_and_explicit_review(self):
        append(self.state, self.receipt, "proposal", {
            "a": {"outcome": "deferred", "reason": "conflicting evidence", "recheck_when": "explicit_review"},
            "b": {"outcome": "deferred", "reason": "missing evidence", "recheck_when": "dependencies_changed"}})
        self.assertEqual(eligible(self.state, self.receipt), [])
        changed = dict(self.receipt, skill_digest="rules2")
        self.assertEqual(eligible(self.state, changed), ["b"])

    def test_pending_failed_check_resumes_existing_proposal(self):
        proposal = self.root / "proposal.json"
        write_json(proposal, {"state": "validation_failed"})
        append(self.state, self.receipt, proposal, {"a": {"outcome": "pending", "reason": "needs validation"}})
        self.assertEqual(eligible(self.state, self.receipt), ["b"])
        proposal.unlink()
        with self.assertRaisesRegex(ValueError, "restore"):
            eligible(self.state, self.receipt)

    def test_project_and_repository_isolation(self):
        append(self.state, self.receipt, "proposal", {"a": {"outcome": "applied", "reason": "done"}})
        self.assertEqual(eligible(self.state, dict(self.receipt, project_id="other")), ["a", "b"])
        self.assertEqual(eligible(self.state, dict(self.receipt, repo="other")), ["a", "b"])

    def test_repository_lock_excludes_overlapping_operations(self):
        with lock(self.state, self.repo):
            with self.assertRaisesRegex(ValueError, "locked"):
                with lock(self.state, self.repo):
                    self.fail("Concurrent lock was acquired")
        with lock(self.state, self.repo):
            pass

    def test_migration_keeps_legacy_history_without_acceptance(self):
        self.state.mkdir()
        with closing(sqlite3.connect(self.state / "experience.sqlite3")) as conn, conn:
            conn.execute("CREATE TABLE learning_processing (project_id,repo,record_id,record_digest,skill_digest,outcome,proposal,updated_at)")
            conn.execute("INSERT INTO learning_processing VALUES (?,?,?,?,?,?,?,?)",
                         ("p", str(self.repo), "a", "a1", "rules1", "reviewed", "old", "then"))
        for _ in range(2):
            conn = connect(self.state)
            conn.close()
        with closing(sqlite3.connect(self.state / "experience.sqlite3")) as conn, conn:
            self.assertEqual(conn.execute("SELECT outcome FROM learning_processing").fetchall(), [("reviewed",)])
            self.assertEqual(conn.execute("SELECT outcome,recheck_when FROM learning_decisions").fetchall(), [("deferred", "explicit_review")])

    def test_decisions_must_cover_work_and_link_new_changes(self):
        pending = {"record_id": "a", "outcome": "pending", "reason": "measured failure"}
        change = {"evidence_ids": ["a", "context"]}
        self.assertEqual(validate_decisions({"decisions": [pending]}, [change], ["a"]), [pending])
        with self.assertRaisesRegex(ValueError, "Every selected"):
            validate_decisions({"decisions": [pending]}, [change], ["a", "b"])
        with self.assertRaises(ValueError):
            validate_decisions({"decisions": []}, [{"evidence_ids": ["old"]}], ["a"])
        with self.assertRaises(ValueError):
            validate_decisions({"changes": []}, [], ["a"])

    def test_analysis_dependency_change_invalidates_receipt(self):
        items = [{"id": "a", "content": "example", "skills": []}]
        skills = {"skills/example/SKILL.md": {"sha256": "one"}}
        before = processing_receipt(items, skills, self.repo, self.repo)
        with patch("learning_cycle.hash_text", return_value="new-policy"):
            after = processing_receipt(items, skills, self.repo, self.repo)
        self.assertNotEqual(before["records"][0]["skill_digest"], after["records"][0]["skill_digest"])

    def test_crash_after_file_write_recovers_without_reapplying(self):
        target = self.repo / "skills/example/SKILL.md"
        target.parent.mkdir(parents=True)
        old = "---\nname: example\ndescription: example\n---\nVerify.\n"
        target.write_text(old, encoding="utf-8")
        path = self.root / "proposal.json"
        proposal = {"repo": str(self.repo), "state": "needs_review",
                    "checks": {"structural_passed": True},
                    "changes": [{"path": "skills/example/SKILL.md", "find": "Verify.",
                                 "replace": "Verify outcome.", "base_sha256": hash_text(old)}]}
        write_json(path, proposal)
        args = Namespace(state=str(self.state), repo=str(self.repo), proposal=str(path),
                         approve=True, accept_unevaluated=True)
        original = write_json
        def crash(path, value):
            if value["state"] == "applied":
                raise OSError("simulated process interruption")
            original(path, value)
        with patch("learning_cycle.write_json", side_effect=crash):
            with self.assertRaises(OSError):
                apply(args)
        self.assertEqual(read_json(path)["state"], "applying")
        self.assertIn("Verify outcome.", target.read_text())
        with patch("learning_cycle.atomic_text", side_effect=AssertionError("Already written file was rewritten")):
            self.assertEqual(apply(args)["result"], "already_applied")

    def test_textual_success_cannot_unlock_apply(self):
        path = self.root / "proposal.json"
        write_json(path, {"repo": str(self.repo), "state": "needs_review", "changes": [],
                         "checks": {"structural_passed": True, "behavioral_passed": True,
                                    "textual_passed": True}})
        with self.assertRaisesRegex(ValueError, "behavioral benchmark"):
            apply(Namespace(state=str(self.state), repo=str(self.repo), proposal=str(path),
                            approve=True, accept_unevaluated=False))

    def test_weak_conflicting_and_project_scoped_evidence_is_not_promoted(self):
        source = "---\nname: example\ndescription: example\n---\nVerify.\n"
        skills = {"skills/example/SKILL.md": {"content": source, "sha256": hash_text(source)}}
        lesson = {"id": "lesson", "kind": "lesson", "status": "candidate", "payload": {"scope": "transfer_candidate"}}
        evidence = [{"id": f"e{i}", "kind": "evidence", "episode_id": f"episode{i}", "status": "verified",
                     "payload": {"source_type": "test", "source_ref": f"trace{i}", "summary": "Observed failure",
                                 "source_revision": "abcdef", "procedure": "test", "result": "failed", "availability": "local"}}
                    for i in (1, 2)]
        candidate = {"schema_version": 1, "changes": [{"path": "skills/example/SKILL.md", "find": "Verify.",
            "replace": "Verify outcomes.", "evidence_ids": ["lesson", "e1", "e2"]}]}
        def observations():
            return [{"id": r["id"], "kind": r["kind"], "content": json.dumps(r)} for r in [lesson, *evidence]]
        self.assertEqual(len(validate_candidate(candidate, skills, observations())), 1)
        lesson["payload"]["scope"] = "project"
        self.assertEqual(len(validate_candidate(candidate, skills, observations(), "project")), 1)
        with self.assertRaisesRegex(ValueError, "Project lessons"):
            validate_candidate(candidate, skills, observations())
        lesson["payload"]["scope"] = "transfer_candidate"
        evidence[1]["status"] = "disputed"
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            validate_candidate(candidate, skills, observations())
        evidence[1]["status"] = "verified"
        evidence[1]["payload"]["source_type"] = "agent_report"
        with self.assertRaisesRegex(ValueError, "independent episodes"):
            validate_candidate(candidate, skills, observations())

    def test_certification_protocol_rejects_incomplete_or_different_reports(self):
        # Synthetic unit fixtures exercise the validator only; this is not a live pass.
        from learning_behavior import snapshot
        target = self.repo / "skills/example/SKILL.md"
        target.parent.mkdir(parents=True)
        old = "---\nname: example\ndescription: example\n---\nVerify.\n"
        new = old.replace("Verify.", "Verify results.")
        target.write_text(old, encoding="utf-8")
        proposal = self.root / "proposal.json"
        write_json(proposal, {"repo": str(self.repo), "state": "needs_review",
            "checks": {"structural_passed": True}, "changes": [{"path": "skills/example/SKILL.md",
            "find": "Verify.", "replace": "Verify results.", "base_sha256": hash_text(old)}]})
        report = {"kind": "environment-outcome", "synthetic": False,
                  "baseline": snapshot(target.parent), "candidate": {"SKILL.md": hash_text(new)},
                  "results": [{"case": str(i), "variant": variant, "repeat": repeat,
                    "status": "completed", "passed": True, "completed_tool_actions": 1}
                    for i in range(6) for variant in ("baseline", "candidate") for repeat in (1, 2)]}
        path = self.root / "report.json"
        args = Namespace(state=str(self.state), repo=str(self.repo), proposal=str(proposal),
                         report=str(path), skill="skills/example/SKILL.md")
        for invalid in (dict(report, synthetic=True), dict(report, results=report["results"][:-1]),
                        dict(report, candidate={"SKILL.md": "wrong"})):
            write_json(path, invalid)
            with self.assertRaises(ValueError):
                certify(args)
        write_json(path, report)
        self.assertTrue(certify(args)["behavioral_passed"])
        from learning_workflow import verification_plan
        plan = verification_plan(['skills/example/SKILL.md'])
        report['verification_plan'] = plan
        report['results'] = [dict(case=case, variant=variant, repeat=repeat, status='completed', passed=True, completed_tool_actions=1)
                             for case in plan['scenarios'] for variant in ('baseline', 'candidate') for repeat in range(1, plan['repetitions'] + 1)]
        write_json(path, report)
        self.assertTrue(certify(args)['behavioral_passed'])
        report['verification_plan'] = dict(plan, repetitions=0)
        write_json(path, report)
        with self.assertRaisesRegex(ValueError, 'risk coverage'):
            certify(args)


if __name__ == "__main__":
    unittest.main()
