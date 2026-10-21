"""Offline, synthetic smoke tests for the packaged learning CLI."""
import json
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

    def test_off_by_default_and_dedup(self):
        event = json.dumps({"client": "codex", "session_id": "s1", "message_id": "m1",
                            "kind": "user", "content": "Hello"})
        self.assertFalse(self.call("capture", payload=event)["recorded"])
        self.call("on")
        self.assertTrue(self.call("capture", payload=event)["recorded"])
        self.assertTrue(self.call("capture", payload=event)["duplicate"])
        self.assertEqual(self.call("status")["events"], 1)
        self.call("off")
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
        self.assertTrue(self.call("purge")["purged"])
        self.assertEqual(self.call("status")["events"], 0)
        self.assertFalse(Path(result["report"]).exists())

    def test_attachment_requires_recorded_session(self):
        self.call("on")
        file = Path(self.temp.name) / "test.png"
        file.write_bytes(b"example")
        p = self.call("attach", "--client", "codex", "--session", "absent",
                      "--file", str(file), expect=1)
        self.assertIn("recorded session", p.stderr)


if __name__ == "__main__":
    unittest.main()
