"""Codex native hook installation tests (Windows and Linux)."""
import json
import shlex
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
            original_bytes = path.read_bytes()
            repeat = json.loads(call("--approve").stdout)
            self.assertFalse(repeat["changed"])
            self.assertEqual(path.read_bytes(), original_bytes)
            installed = json.loads(path.read_text())
            self.assertEqual(len(installed["hooks"]["PostToolUse"]), 2)
            labels = [installed["hooks"][event][-1]["hooks"][0]["statusMessage"]
                      for event in ("UserPromptSubmit", "PostToolUse", "Stop")]
            self.assertEqual(len(set(labels)), 3)
            self.assertEqual(labels, ["Record user prompt", "Record tool result",
                                      "Record assistant response"])
            installed["hooks"]["Stop"][-1]["hooks"][0]["statusMessage"] = "My custom label"
            installed["hooks"]["Stop"][-1]["hooks"][0]["timeout"] = 9
            old_command = installed["hooks"]["Stop"][-1]["hooks"][0]["command"]
            old_args = shlex.split(old_command)
            old_args[0] = "/previous/python3"
            installed["hooks"]["Stop"][-1]["hooks"][0]["command"] = shlex.join(old_args)
            installed["hooks"]["UserPromptSubmit"][-1]["hooks"][0]["statusMessage"] = "WebDev: ????? ???????"
            installed["hooks"]["PostToolUse"][-1]["hooks"][0]["statusMessage"] = "WebDev: record tool result"
            path.write_text(json.dumps(installed), encoding="utf-8")
            call("--approve")
            installed = json.loads(path.read_text())
            self.assertEqual(installed["hooks"]["Stop"][-1]["hooks"][0]["statusMessage"],
                             "My custom label")
            self.assertEqual(len(installed["hooks"]["Stop"]), 1)
            self.assertEqual(installed["hooks"]["Stop"][-1]["hooks"][0]["timeout"], 9)
            self.assertEqual(installed["hooks"]["UserPromptSubmit"][-1]["hooks"][0]["statusMessage"], "Record user prompt")
            self.assertEqual(installed["hooks"]["PostToolUse"][-1]["hooks"][0]["statusMessage"], "Record tool result")
            unchanged = path.read_bytes()
            backup = path.with_suffix(".json.bak").read_bytes()
            self.assertFalse(json.loads(call("--approve").stdout)["changed"])
            self.assertEqual(path.read_bytes(), unchanged)
            self.assertEqual(path.with_suffix(".json.bak").read_bytes(), backup)
            self.assertIn("commandWindows", installed["hooks"]["Stop"][-1]["hooks"][0])
            call("--remove", "--approve")
            remaining = json.loads(path.read_text())
            self.assertEqual(len(remaining["hooks"]["PostToolUse"]), 1)
            self.assertEqual(remaining["hooks"]["PostToolUse"][0]["matcher"], "Bash")
            self.assertEqual(remaining["hooks"]["Stop"], [])


if __name__ == "__main__":
    unittest.main()
