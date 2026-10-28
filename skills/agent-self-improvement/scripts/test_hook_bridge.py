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
            with patch.dict(os.environ, {'AGENT_LEARNING_STATE': str(state)}), patch.object(sys, 'argv', [str(BRIDGE), '--client', 'codex']), patch.object(sys, 'stdin', io.StringIO(json.dumps(event))), patch.object(sys, 'stdout', io.StringIO()), patch('subprocess.run', side_effect=capture_only):
                runpy.run_path(str(BRIDGE), run_name='__main__')
            self.assertEqual(len(calls), 1)
            with closing(sqlite3.connect(state / 'experience.sqlite3')) as conn:
                self.assertEqual(conn.execute('SELECT COUNT(*) FROM events').fetchone()[0], 1)
            self.assertFalse(list((state / 'outbox').glob('*.json')))
            self.assertFalse(list((state / 'runs').glob('*')))
            self.assertFalse(list((state / 'archive').glob('*/*.json')))

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
