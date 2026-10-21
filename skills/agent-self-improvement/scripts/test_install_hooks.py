"""Codex native hook installation tests (Windows and Linux)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

INSTALL = Path(__file__).with_name("install_hooks.py")


class HookInstallerTests(unittest.TestCase):
    def test_preview_merge_and_remove(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / ".codex" / "hooks.json"
            path.parent.mkdir()
            path.write_text(json.dumps({
                "hooks": {"PostToolUse": [{
                    "matcher": "Bash",
                    "hooks": [{"type": "command", "command": "echo existing"}],
                }]},
            }), encoding="utf-8")
            def call(*args):
                return subprocess.run(
                    [sys.executable, str(INSTALL), "--project", str(root), *args],
                    capture_output=True, text=True, check=True,
                )
            call()
            original = json.loads(path.read_text())
            self.assertEqual(len(original["hooks"]["PostToolUse"]), 1)
            call("--approve")
            installed = json.loads(path.read_text())
            self.assertEqual(len(installed["hooks"]["PostToolUse"]), 2)
            self.assertIn("commandWindows", installed["hooks"]["Stop"][-1]["hooks"][0])
            call("--remove", "--approve")
            remaining = json.loads(path.read_text())
            self.assertEqual(len(remaining["hooks"]["PostToolUse"]), 1)
            self.assertEqual(remaining["hooks"]["PostToolUse"][0]["matcher"], "Bash")


if __name__ == "__main__":
    unittest.main()
