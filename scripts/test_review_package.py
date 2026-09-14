#!/usr/bin/env python3
"""Exercise review packaging against real temporary Git repositories, offline."""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "skills/frontend-quality-reviewer/scripts/review_package.py"
SPEC = importlib.util.spec_from_file_location("review_package", HELPER)
kit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kit)


class ReviewPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@local.invalid")
        self.git("config", "user.name", "Fixture")
        self.write(".gitignore", ".agents/project/\n")
        self.write("app.txt", "baseline\n")
        self.write("other.txt", "user work\n")
        self.commit("baseline")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.write("app.txt", "baseline\nearly change\n")
        self.commit("first task commit")
        self.write("second.txt", "late change\n")
        self.commit("second task commit")
        self.plan = ".agents/project/active-plan.md"
        self.write(self.plan, "# G-001\nS-001 [AC-001]: implement\n")

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.root), *args],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "-qm", message)

    def capture(self, **options):
        return kit.package(self.root, self.plan, self.base, **options)

    def body(self, result):
        return (self.root / result["path"]).read_text()

    def test_all_task_commits_not_only_head_parent(self):
        result = self.capture()
        body = self.body(result)
        self.assertIn("+early change", body)
        self.assertIn("+late change", body)
        self.assertIn("first task commit", body)
        self.assertEqual(result["base"], self.base)
        self.assertEqual(result["verification"], "not-run-by-packager")

    def test_committed_range_excludes_unstaged_user_changes(self):
        self.write("app.txt", "uncommitted user change\n")
        self.assertNotIn("uncommitted user change", self.body(self.capture()))

    def test_worktree_captures_staged_unstaged_untracked_owned_only(self):
        self.write("app.txt", "staged\n")
        self.git("add", "app.txt")
        self.write("app.txt", "staged\nunstaged\n")
        self.write("new.txt", "untracked\n")
        self.write("other.txt", "PRIVATE UNRELATED CHANGE\n")
        result = self.capture(worktree=True, paths=["app.txt", "new.txt"])
        body = self.body(result)
        self.assertIn("+staged", body)
        self.assertIn("+unstaged", body)
        self.assertIn("+untracked", body)
        self.assertNotIn("PRIVATE UNRELATED CHANGE", body)
        self.assertEqual(result["untracked_files"], ["new.txt"])
        self.assertEqual(set(result["file_sha256"]), {"app.txt", "new.txt"})
        self.assertIn("other.txt", self.git("status", "--porcelain"))

    def test_fresh_fix_diff_and_different_plan_never_overwrite(self):
        first = self.capture()
        fixed_base = self.git("rev-parse", "HEAD").strip()
        self.write("second.txt", "fixed\n")
        self.commit("fix")
        second = kit.package(self.root, self.plan, fixed_base)
        self.assertNotEqual(first["path"], second["path"])
        self.assertNotIn("+early change", self.body(second))
        self.assertIn("+fixed", self.body(second))
        self.write(".agents/project/other-plan.md", "# Other plan\n")
        other = kit.package(self.root, ".agents/project/other-plan.md", self.base)
        self.assertNotEqual(Path(first["path"]).parent, Path(other["path"]).parent)
        self.assertTrue((self.root / first["path"]).exists())

    def test_same_input_noop_and_private_permissions(self):
        first = self.capture()
        second = self.capture()
        self.assertEqual(first["path"], second["path"])
        self.assertEqual(second["status"], "unchanged")
        if os.name == "posix":
            self.assertEqual((self.root / first["path"]).stat().st_mode & 0o777, 0o600)

    def test_worktree_requires_explicit_ownership_and_current_head(self):
        for options in (
            {"worktree": True},
            {"worktree": True, "head": self.base, "paths": ["app.txt"]},
        ):
            with self.assertRaises(ValueError):
                self.capture(**options)
        self.assertFalse((self.root / ".agents/project/runs").exists())

    def test_traversal_and_symlinks_rejected_without_writes(self):
        for bad in (
            "../outside",
            "/tmp/outside",
            "C:/outside",
            "dir\\outside",
            ".git/config",
        ):
            with self.subTest(path=bad), self.assertRaises(ValueError):
                self.capture(worktree=True, paths=[bad])
        outside = self.root / "outside"
        outside.mkdir()
        (self.root / ".agents/project/runs").symlink_to(
            outside, target_is_directory=True
        )
        with self.assertRaises(ValueError):
            self.capture()
        self.assertEqual(list(outside.iterdir()), [])

    def test_changes_during_capture_are_rejected(self):
        calls = 0
        original = kit.snapshot

        def mutating(root, paths):
            nonlocal calls
            calls += 1
            if calls == 2:
                self.write("app.txt", "racing writer\n")
            return original(root, paths)

        with (
            patch.object(kit, "snapshot", side_effect=mutating),
            self.assertRaises(ValueError),
        ):
            self.capture(worktree=True, paths=["app.txt"])
        self.assertFalse((self.root / ".agents/project/runs").exists())

    def test_size_budget_blocks_before_artifact_write(self):
        with patch.object(kit, "MAX_BYTES", 20), self.assertRaises(ValueError):
            self.capture()
        self.assertFalse((self.root / ".agents/project/runs").exists())

    def test_output_requires_ignored_local_storage(self):
        self.write(".gitignore", "")
        with self.assertRaises(ValueError):
            self.capture()
        self.assertFalse((self.root / ".agents/project/runs").exists())

    def test_stale_worktree_capture_creates_distinct_evidence(self):
        first = self.capture(worktree=True, paths=["app.txt"])
        self.write("app.txt", "new state\n")
        second = self.capture(worktree=True, paths=["app.txt"])
        self.assertNotEqual(first["path"], second["path"])
        self.assertNotEqual(first["file_sha256"], second["file_sha256"])
        self.assertTrue((self.root / first["path"]).exists())

    def test_reversed_or_option_like_refs_are_rejected(self):
        for base, head in (("HEAD", self.base), ("--help", "HEAD")):
            with self.assertRaises(ValueError):
                kit.package(self.root, self.plan, base, head)
        self.assertFalse((self.root / ".agents/project/runs").exists())

    def test_filename_glob_characters_are_literal(self):
        self.write("item[1].txt", "owned literal name\n")
        self.write("item1.txt", "unowned similar name\n")
        result = self.capture(worktree=True, paths=["item[1].txt"])
        self.assertEqual(set(result["file_sha256"]), {"item[1].txt"})
        self.assertIn("+owned literal name", self.body(result))
        self.assertNotIn("unowned similar name", self.body(result))

    def test_cli_returns_reference_not_diff(self):
        result = subprocess.run(
            [
                sys.executable,
                str(HELPER),
                "--root",
                str(self.root),
                "--plan",
                self.plan,
                "--base",
                self.base,
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / json.loads(result.stdout)["path"]).is_file())
        self.assertNotIn("+early change", result.stdout)


if __name__ == "__main__":
    unittest.main()
