"""Synthetic Codex hook payload and nonblocking output contract tests."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

BRIDGE = Path(__file__).resolve().parents[1] / "assets" / "integrations" / "hook_bridge.py"


class HookBridgeTests(unittest.TestCase):
    def test_codex_stop_always_returns_json(self):
        with tempfile.TemporaryDirectory() as directory:
            event = {
                "hook_event_name": "Stop",
                "cwd": directory,
                "session_id": "test-session",
                "turn_id": "test-turn",
                "last_assistant_message": "A completed turn",
            }
            result = subprocess.run(
                [sys.executable, str(BRIDGE), "--client", "codex"],
                input=json.dumps(event), text=True, capture_output=True, check=True,
            )
            self.assertEqual(json.loads(result.stdout), {})

    def test_codex_stop_handles_bad_payload_without_blocking(self):
        result = subprocess.run(
            [sys.executable, str(BRIDGE), "--client", "codex"],
            input="{invalid-json", text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0)

    def test_unknown_project_writes_nothing(self):
        event = {
            "hook_event_name": "UserPromptSubmit",
            "session_id": "test-session",
            "prompt": "A test",
        }
        result = subprocess.run(
            [sys.executable, str(BRIDGE), "--client", "codex"],
            input=json.dumps(event), text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
