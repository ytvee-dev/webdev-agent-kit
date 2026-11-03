"""Synthetic Codex hook payload and nonblocking output contract tests."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

BRIDGE = Path(__file__).resolve().parents[1] / "assets" / "integrations" / "hook_bridge.py"


class HookBridgeTests(unittest.TestCase):
    def test_enabled_hook_only_captures_locally(self):
        import io
        import os
        import runpy
        import sqlite3
        from contextlib import closing
        from unittest.mock import patch

        from learning import set_mode
        from learning_memory import open_store
        from learning_project import initialize
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            initialize(project)
            state = project / '.agents/learning'
            with closing(open_store(state)) as conn:
                set_mode(conn, str(project), True)
            event = {'hook_event_name': 'Stop', 'cwd': directory,
                     'session_id': 'capture-only', 'turn_id': 'one',
                     'last_assistant_message': 'A local outcome'}
            original = subprocess.run
            calls = []
            def capture_only(args, **kwargs):
                calls.append(args)
                self.assertEqual(args[2:], ['capture', '--project', directory])
                self.assertEqual(Path(args[1]).name, 'learning.py')
                return original(args, **kwargs)
            with patch.dict(os.environ, {'AGENT_LEARNING_STATE': str(state)}), patch.object(sys, 'argv', [str(BRIDGE), '--client', 'codex']), patch.object(sys, 'stdin', io.TextIOWrapper(io.BytesIO(json.dumps(event).encode('utf-8')), encoding='utf-8')), patch.object(sys, 'stdout', io.StringIO()), patch('subprocess.run', side_effect=capture_only):
                runpy.run_path(str(BRIDGE), run_name='__main__')
            self.assertEqual(len(calls), 1)
            with closing(sqlite3.connect(state / 'experience.sqlite3')) as conn:
                self.assertEqual(conn.execute('SELECT COUNT(*) FROM events').fetchone()[0], 1)
            self.assertFalse(list((state / 'outbox').glob('*.json')))
            self.assertFalse(list((state / 'runs').glob('*')))
            self.assertFalse(list((state / 'archive').glob('*/*.json')))
            kimi_event = {"hook_event_name": "PostToolUse", "cwd": directory,
                          "session_id": "kimi-capture", "tool_call_id": "native-id",
                          "tool_name": "Read", "tool_output": "observed result"}
            original([sys.executable, str(BRIDGE), "--client", "kimi", "--project", directory,
                      "--state", str(state)], input=json.dumps(kimi_event), text=True, check=True)
            with closing(sqlite3.connect(state / 'experience.sqlite3')) as conn:
                row = conn.execute("SELECT message_id, content FROM events WHERE client='kimi'").fetchone()
                self.assertEqual(row[0], "native-id")
                self.assertIn("observed result", row[1])
            normalize = runpy.run_path(str(BRIDGE))["normalize"]
            base = {"cwd": directory, "session_id": "kimi-capture"}
            prompt = normalize(dict(base, hook_event_name="UserPromptSubmit", prompt=[
                {"type": "text", "text": "review this"},
                {"type": "image_url", "image_url": "private-image-bytes"},
            ]), "kimi")[1]
            self.assertEqual(prompt["content"], "review this")
            self.assertFalse(prompt["content_missing"])
            self.assertTrue(normalize(dict(base, hook_event_name="Stop"), "kimi")[1]["content_missing"])
            clipped = normalize(dict(kimi_event, tool_output="x" * 2000), "kimi")[1]
            self.assertTrue(clipped["truncated"])
            failed = dict(base, hook_event_name="PostToolUseFailure", tool_name="Bash",
                          tool_call_id="failed-id", error={"message": "command failed"})
            original([sys.executable, str(BRIDGE), "--client", "kimi", "--project", directory,
                      "--state", str(state)], input=json.dumps(failed), text=True, check=True)
            with closing(sqlite3.connect(state / 'experience.sqlite3')) as conn:
                content = conn.execute("SELECT content FROM events WHERE message_id='failed-id'").fetchone()[0]
                self.assertIn("Failed:", content)
                self.assertIn("command failed", content)
            kimi_event["cwd"] = str(project / "other")
            original([sys.executable, str(BRIDGE), "--client", "kimi", "--project", directory,
                      "--state", str(state)], input=json.dumps(kimi_event), text=True, check=True)
            with closing(sqlite3.connect(state / 'experience.sqlite3')) as conn:
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM events WHERE client='kimi'").fetchone()[0], 2)


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
