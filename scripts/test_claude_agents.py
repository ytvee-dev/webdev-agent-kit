#!/usr/bin/env python3

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from build_release_archives import build_archive
from build_skill_targets import build_claude_plugin_target
from validate_claude_agents import ROOT, validate_agents
from validate_release_archive import validate_archive


class ClaudeAgentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build_claude_plugin_target()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.agents = self.root / "agents"
        shutil.copytree(ROOT / "dist/claude-code/agents", self.agents)

    def change(self, name, old, new):
        path = self.agents / f"{name}.md"
        self.assertIn(old, path.read_text())
        path.write_text(path.read_text().replace(old, new))

    def test_generated_roles_and_archive(self):
        self.assertEqual(validate_agents(self.agents), [])
        archive = self.root / "claude.tar.gz"
        build_archive("claude-code", archive)
        self.assertEqual(validate_archive(archive, "claude-code"), [])

    def test_missing_role_is_rejected(self):
        (self.agents / "wdk-lookup.md").unlink()
        self.assertTrue(
            any("inventory" in error for error in validate_agents(self.agents))
        )

    def test_read_only_roles_cannot_get_shell_or_edit_tools(self):
        for tool in ("Bash", "Edit", "Agent"):
            with self.subTest(tool=tool):
                path = self.agents / "wdk-reviewer.md"
                original = path.read_text()
                path.write_text(
                    re.sub(
                        r"^tools:.*$",
                        "tools: " + json.dumps(["Read", "Glob", "Grep", tool]),
                        original,
                        flags=re.MULTILINE,
                    )
                )
                self.assertTrue(
                    any(
                        "permissions" in error for error in validate_agents(self.agents)
                    )
                )
                path.write_text(original)

    def test_worker_cannot_delegate(self):
        self.change("wdk-worker", '"Bash"]', '"Bash", "Agent"]')
        self.assertTrue(
            any("permissions" in error for error in validate_agents(self.agents))
        )

    def test_fixed_model_and_graph_leaks_are_rejected(self):
        self.change(
            "wdk-architect", "model: 'inherit'", "model: 'opus'\nid: source-only"
        )
        errors = validate_agents(self.agents)
        self.assertTrue(any("inherit" in error for error in errors))
        self.assertTrue(any("portable" in error for error in errors))

    def test_missing_handoff_boundary_is_rejected(self):
        self.change("wdk-worker-light", "Do not delegate", "Delegate freely")
        self.assertTrue(
            any("handoff" in error for error in validate_agents(self.agents))
        )

    def test_plugin_policy_and_skill_roots(self):
        plugin = ROOT / "dist/claude-code"
        self.assertTrue((plugin / "AGENTS.md").is_file())
        for skill in (plugin / "skills").glob("*/SKILL.md"):
            with self.subTest(skill=skill.parent.name):
                text = skill.read_text()
                self.assertIn("${CLAUDE_SKILL_DIR}/../../AGENTS.md", text)
                self.assertEqual(
                    (skill.parent / "../../AGENTS.md").resolve(), plugin / "AGENTS.md"
                )


if __name__ == "__main__":
    unittest.main()
