"""Offline, synthetic smoke tests for the packaged learning CLI."""
import base64
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).with_name("learning.py")


class LearningSmoke(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.state = str(Path(self.temp.name) / "private")
        self.project = str(Path(self.temp.name) / "project")
        Path(self.project).mkdir()

    def call(self, command, *extra, payload=None, expect=0):
        p = subprocess.run([sys.executable, str(CLI), "--state", self.state,
                            command, "--project", self.project, *extra],
                           input=payload, text=True, capture_output=True)
        self.assertEqual(p.returncode, expect, p.stderr)
        return json.loads(p.stdout) if p.stdout.strip() else p

    def test_windows_project_identifiers_are_case_insensitive(self):
        if os.name != "nt":
            self.skipTest("Windows-only normalization check")
        sys.path.insert(0, str(CLI.parent))
        from learning import project_id

        self.assertEqual(project_id(self.project), project_id(self.project.upper()))

    def test_off_by_default_and_dedup(self):
        event = json.dumps({"client": "codex", "session_id": "s1", "message_id": "m1",
                            "kind": "user", "content": "Hello"})
        self.assertFalse(self.call("capture", payload=event)["recorded"])
        self.call("on")
        self.assertTrue(self.call("capture", payload=event)["recorded"])
        self.assertTrue(self.call("capture", payload=event)["duplicate"])
        self.assertEqual(self.call("status")["events"], 1)
        sessions = self.call("sessions")["sessions"]
        self.assertEqual(sessions[0]["session_id"], "s1")
        self.call("pause", "--client", "codex", "--session", "s1")
        self.assertEqual(self.call("capture", payload=event)["reason"], "session_paused")
        self.assertEqual(len(self.call("status")["paused_sessions"]), 1)
        other = json.loads(event)
        other["session_id"] = "s2"
        self.assertTrue(self.call("capture", payload=json.dumps(other))["recorded"])
        self.call("off")
        self.call("resume", "--client", "codex", "--session", "s1")
        self.assertFalse(self.call("capture", payload=event)["recorded"])

    def test_correction_triage_and_purge(self):
        self.call("on")
        for session in ("one", "two"):
            self.call("capture", payload=json.dumps(
                {"client": "codex", "session_id": session, "message_id": "m",
                 "kind": "user_correction", "content": "Verify the breakpoint first"}))
        result = self.call("run")
        self.assertEqual(result["findings"], 1)
        report = json.loads(Path(result["report"]).read_text())
        self.assertEqual(report["findings"][0]["distinct_sessions"], 2)
        self.call("capture", payload=json.dumps({"client": "codex", "session_id": "old", "message_id": "old",
                  "kind": "tool", "content": "obsolete", "timestamp": "2000-01-01T00:00:00+00:00"}))
        self.assertEqual(self.call("retain", "--days", "30")["eligible"], 1)
        self.assertEqual(self.call("status")["events"], 3)
        self.assertEqual(self.call("retain", "--days", "30", "--apply")["deleted"], 1)
        self.assertEqual(self.call("status")["events"], 2)
        self.assertTrue(self.call("purge")["purged"])
        self.assertEqual(self.call("status")["events"], 0)
        self.assertFalse(Path(result["report"]).exists())

    def test_inline_attachment_is_retained_without_remote_fetch(self):
        self.call("on")
        self.call("capture", payload=json.dumps({
            "client": "opencode", "session_id": "image-chat",
            "message_id": "m1", "kind": "user", "content": "Look at this screenshot",
        }))
        payload = json.dumps({
            "client": "opencode", "session_id": "image-chat", "name": "screenshot.png",
            "data_url": "data:image/png;base64,"
            + base64.b64encode(b"fake-png-bytes").decode("ascii"),
        })
        result = self.call("attach-data", payload=payload)
        self.assertEqual(result["bytes"], len(b"fake-png-bytes"))
        digest = result["sha256"]
        stored = Path(self.state) / "blobs" / digest[:2] / digest
        self.assertEqual(stored.read_bytes(), b"fake-png-bytes")
        self.call("off")
        rejected = self.call("attach-data", payload=payload, expect=1)
        self.assertIn("Collection is off", rejected.stderr)

    def test_attachment_requires_recorded_session(self):
        self.call("on")
        file = Path(self.temp.name) / "test.png"
        file.write_bytes(b"example")
        p = self.call("attach", "--client", "codex", "--session", "absent",
                      "--file", str(file), expect=1)
        self.assertIn("recorded session", p.stderr)


if __name__ == "__main__":
    unittest.main()
