import hashlib
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from learning import capture, default_root, project_id, set_mode
from learning_memory import bind, open_store
from learning_project import initialize


class ProjectStateTests(unittest.TestCase):
    def test_migration_roundtrip_and_idempotence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project, other, legacy = root / "project", root / "other", root / "legacy"
            project.mkdir()
            other.mkdir()
            with closing(open_store(legacy)) as conn:
                pid = bind(conn, project)
                bind(conn, other)
                for p in (project, other):
                    set_mode(conn, p, True)
                    capture(
                        conn,
                        p,
                        {
                            "client": "test",
                            "session_id": "s",
                            "message_id": "m",
                            "kind": "user",
                            "content": p.name,
                        },
                    )
                with conn:
                    conn.execute(
                        "CREATE TABLE learning_processing (project_id TEXT,repo TEXT,record_id TEXT,record_digest TEXT,skill_digest TEXT,outcome TEXT,proposal TEXT,updated_at TEXT)"
                    )
                    for p in (project, other):
                        conn.execute(
                            "INSERT INTO learning_processing VALUES (?,?,?,?,?,?,?,?)",
                            (
                                project_id(p),
                                str(p),
                                "old",
                                "r",
                                "s",
                                "reviewed",
                                "",
                                "today",
                            ),
                        )
            old_id = project_id(project)
            before = hashlib.sha256(
                (legacy / "experience.sqlite3").read_bytes()
            ).hexdigest()
            result = initialize(project, legacy)
            self.assertEqual(result["project_id"], pid)
            self.assertEqual(project_id(project), old_id)
            self.assertEqual(
                initialize(project, legacy)["result"], "already_initialized"
            )
            with closing(
                sqlite3.connect(project / ".agents/learning/experience.sqlite3")
            ) as conn:
                self.assertEqual(
                    conn.execute("SELECT content FROM events").fetchall(),
                    [("project",)],
                )
                self.assertEqual(
                    conn.execute("SELECT id FROM memory_projects").fetchall(), [(pid,)]
                )
                self.assertEqual(
                    conn.execute("PRAGMA integrity_check").fetchone()[0], "ok"
                )
                self.assertEqual(
                    conn.execute(
                        "SELECT outcome,details FROM learning_decisions"
                    ).fetchall(),
                    [("deferred", '{"legacy":true}')],
                )
            self.assertEqual(
                before,
                hashlib.sha256(
                    (legacy / "experience.sqlite3").read_bytes()
                ).hexdigest(),
            )
            moved = root / "renamed"
            project.rename(moved)
            self.assertEqual(project_id(moved), old_id)
            with (
                patch("sys.argv", ["learning.py", "status", "--project", str(moved)]),
                patch.dict("os.environ", {}, clear=True),
            ):
                self.assertEqual(default_root(), moved.resolve() / ".agents/learning")

    def test_partial_state_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            target = project / ".agents/learning"
            target.mkdir(parents=True)
            (target / "keep").write_text("data")
            with self.assertRaisesRegex(ValueError, "Partial"):
                initialize(project)
            self.assertEqual((target / "keep").read_text(), "data")
            fresh = project / 'fresh'
            fresh.mkdir()
            with self.assertRaisesRegex(ValueError, 'Legacy database not found'):
                initialize(fresh, project / 'missing')
            self.assertFalse((fresh / '.agents/learning').exists())
            unrelated = project / 'unrelated'
            with closing(open_store(unrelated)) as conn:
                bind(conn, project)
            with self.assertRaisesRegex(ValueError, 'absent from the legacy'):
                initialize(fresh, unrelated)
            self.assertFalse((fresh / '.agents/learning').exists())
            stages = list((fresh / '.agents').glob('.learning-migrate-*'))
            self.assertEqual(len(stages), 1)
            self.assertEqual((stages[0] / '.gitignore').read_text(), '*\n')
            # An ignored failed stage never becomes active state or prevents retry.
            self.assertEqual(initialize(fresh)['result'], 'initialized')


if __name__ == "__main__":
    unittest.main()
