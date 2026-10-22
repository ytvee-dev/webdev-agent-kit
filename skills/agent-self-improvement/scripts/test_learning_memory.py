"""Executable storage/exchange regression tests; no live model claims."""
import copy
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from learning import capture, create_store, set_mode
from learning_memory import (
    FIELDS,
    bind,
    configure,
    import_package,
    open_store,
    package,
    recall,
    records,
    save_records,
    session_context,
    sync,
)


class ProjectMemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / 'project'
        self.project.mkdir()
        self.state = self.root / 'state'
        self.conn = open_store(self.state)
        self.addCleanup(self.conn.close)
        self.pid = bind(self.conn, self.project)

    def record(self, kind, name):
        payload = {key: [] if key.endswith('_ids') else '' for key in FIELDS[kind]}
        if kind == 'episode':
            payload.update(coverage='partial', task='Currency formatting', source_event_ids=['local-event'])
        if kind == 'evidence':
            payload.update(source_type='agent_report', source_ref='local-event', availability='local_only', observed_at='2026-10-22T00:00:00+00:00')
        if kind == 'finding':
            payload.update(cause_status='hypothesis', evidence_ids=['evidence'])
        if kind == 'lesson':
            payload.update(instruction='Check currency consumers', scope='project', evidence_ids=['evidence'], finding_ids=['finding'])
        if kind == 'evaluation':
            payload['held_out'] = True
        return dict(id=name, revision=1, project_id=self.pid, episode_id='episode', kind=kind, status='candidate', payload=payload,
                    provenance=dict(agent='test', client='test', skill_version='1.6.0', session_id='session'), created_at='2026-10-22T00:00:00+00:00')

    def sample(self):
        return [self.record(kind, kind) for kind in ('episode', 'evidence', 'finding', 'lesson')]

    def test_roundtrip_idempotence_and_project_isolation(self):
        sample = self.sample()
        self.assertEqual(save_records(self.conn, self.pid, sample), 4)
        exported = package(self.conn, self.pid)
        with open_store(self.root / 'other') as other:
            pid = bind(other, self.root / 'clone', self.pid)
            self.assertEqual(import_package(other, pid, exported), 4)
            self.assertEqual(import_package(other, pid, exported), 0)
            self.assertEqual(records(other, pid), records(self.conn, self.pid))
            foreign = bind(other, self.root / 'unrelated')
            with self.assertRaisesRegex(ValueError, 'another project'):
                import_package(other, foreign, exported)
            self.assertEqual(records(other, foreign), [])

    def test_unknown_schema_missing_fields_and_atomic_failure(self):
        data = package(self.conn, self.pid)
        data['schema_version'] = 999
        with self.assertRaisesRegex(ValueError, 'schema'):
            import_package(self.conn, self.pid, data)
        items = self.sample()
        del items[-1]['payload']['instruction']
        with self.assertRaisesRegex(ValueError, 'fields'):
            save_records(self.conn, self.pid, items)
        self.assertEqual(records(self.conn, self.pid), [])

    def test_narrative_does_not_confirm_cause(self):
        items = self.sample()
        items[2]['payload']['cause_status'] = 'confirmed'
        with self.assertRaisesRegex(ValueError, 'reports alone'):
            save_records(self.conn, self.pid, items)

    def test_conflict_and_revision_recall(self):
        items = self.sample()
        save_records(self.conn, self.pid, items)
        conflict = copy.deepcopy(items[-1])
        conflict['payload']['instruction'] = 'Always currency'
        with self.assertRaisesRegex(ValueError, 'Revision conflict'):
            save_records(self.conn, self.pid, [conflict])
        self.assertEqual(recall(self.conn, self.pid, 'currency'), [])
        accepted = copy.deepcopy(items[-1])
        accepted.update(revision=2, status='accepted')
        save_records(self.conn, self.pid, [accepted])
        self.assertEqual(len(recall(self.conn, self.pid, 'currency')), 1)
        accepted.update(revision=3, status='stale')
        save_records(self.conn, self.pid, [accepted])
        self.assertEqual(recall(self.conn, self.pid, 'currency'), [])

    def test_all_session_events_and_no_raw_export(self):
        set_mode(self.conn, self.project, True)
        for n in range(75):
            capture(self.conn, self.project, dict(client='test', session_id='session', message_id=str(n), kind='user', content='PRIVATE_RAW_TRANSCRIPT' + str(n)))
        context = session_context(self.conn, self.project, 'test', 'session')
        self.assertEqual(len(context['events']), 75)
        self.assertEqual(context['coverage'], 'unknown')
        save_records(self.conn, self.pid, self.sample())
        self.assertNotIn('PRIVATE_RAW_TRANSCRIPT', json.dumps(package(self.conn, self.pid)))
        with self.assertRaises(ValueError):
            session_context(self.conn, self.root / 'foreign', 'test', 'session')

    def test_legacy_backup_and_schema(self):
        legacy = self.root / 'legacy'
        with create_store(legacy) as conn:
            set_mode(conn, self.project, True)
            capture(conn, self.project, dict(client='test', session_id='s', kind='user', content='preserve me'))
        with open_store(legacy) as upgraded:
            self.assertEqual(upgraded.execute('PRAGMA user_version').fetchone()[0], 2)
            self.assertEqual(upgraded.execute('SELECT content FROM events').fetchone()[0], 'preserve me')
            self.assertEqual(upgraded.execute('PRAGMA foreign_keys').fetchone()[0], 1)
        backups = list(legacy.glob('experience.pre-v2-*.sqlite3'))
        self.assertEqual(len(backups), 1)
        with open_store(legacy):
            pass
        self.assertEqual(len(list(legacy.glob('experience.pre-v2-*.sqlite3'))), 1)
        with sqlite3.connect(backups[0]) as conn:
            self.assertEqual(conn.execute('SELECT content FROM events').fetchone()[0], 'preserve me')

    def test_future_database_rejected(self):
        self.conn.execute('PRAGMA user_version=999')
        with self.assertRaisesRegex(ValueError, 'Unsupported'):
            open_store(self.state)

    def test_secret_and_broken_relation_rejected(self):
        items = self.sample()
        items[-1]['payload']['instruction'] = 'password=secret123456'
        with self.assertRaisesRegex(ValueError, 'secret'):
            save_records(self.conn, self.pid, items)
        items = self.sample()
        items[-1]['payload']['finding_ids'] = ['absent']
        with self.assertRaisesRegex(ValueError, 'reference'):
            save_records(self.conn, self.pid, items)

    def test_manual_sync_contract(self):
        save_records(self.conn, self.pid, self.sample())
        remote = {'private': True, 'permissions': {'push': True}, 'size': 0}
        with patch('learning_memory.gh', return_value=remote) as api:
            configure(self.conn, self.pid, 'owner/memory')
            self.assertEqual(api.call_count, 1)  # configuring never uploads
        with patch('learning_memory.gh', side_effect=[remote, ValueError('missing'), {}]) as api:
            result = sync(self.conn, self.pid, 'push')
            self.assertEqual(result['records'], 4)
            self.assertIn('projects/' + self.pid + '/packages/', result['path'])
            self.assertEqual(api.call_count, 3)
        with patch('learning_memory.gh', return_value={'private': False}):
            with self.assertRaisesRegex(ValueError, 'private'):
                sync(self.conn, self.pid, 'push')

    def test_revision_cannot_invalidate_confirmed_findings(self):
        items = self.sample()
        items[1]['payload']['source_type'] = 'diff'
        items[2]['payload']['cause_status'] = 'confirmed'
        save_records(self.conn, self.pid, items)
        revision = copy.deepcopy(items[1])
        revision['revision'] = 2
        revision['payload']['source_type'] = 'agent_report'
        with self.assertRaisesRegex(ValueError, 'reports alone'):
            save_records(self.conn, self.pid, [revision])
        self.assertEqual(len(records(self.conn, self.pid)), 4)

    def test_structured_only_proposal_without_raw_events(self):
        from argparse import Namespace

        from learning_cycle import propose
        save_records(self.conn, self.pid, self.sample())
        repo = self.root / 'kit'
        skill = repo / 'skills' / 'example' / 'SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text('---\nname: example\ndescription: example\n---\nCheck things.\n')
        proposal = self.root / 'proposal.json'
        proposal.write_text(json.dumps({'schema_version': 1, 'changes': []}))
        result = propose(Namespace(repo=str(repo), project=str(self.project), state=str(self.state), engine=None, proposal_file=str(proposal), skill=[]))
        self.assertIn('proposal', result)

    def test_pull_deduplicates_historical_packages(self):
        import base64

        from learning_memory import canonical, digest
        data = {'schema_version': 2, 'project_id': self.pid, 'records': self.sample()}
        name = 'projects/' + self.pid + '/packages/' + digest(data) + '.json'
        self.conn.execute('UPDATE memory_projects SET sync_repository=? WHERE id=?', ('owner/memory', self.pid))
        self.conn.commit()
        tree = {'tree': [{'path': name, 'type': 'blob', 'sha': 'test', 'size': 5000}] * 2501}
        def api(path, *args, **kwargs):
            if '/git/trees/' in path:
                return tree
            if '/git/blobs/' in path:
                return {'content': base64.b64encode(canonical(data).encode()).decode()}
            return {'private': True, 'size': 1, 'default_branch': 'main'}
        with patch('learning_memory.gh', side_effect=api):
            self.assertEqual(sync(self.conn, self.pid, 'pull')['records'], 4)

    def test_binding_cannot_silently_change(self):
        self.assertEqual(bind(self.conn, self.project), self.pid)
        with self.assertRaisesRegex(ValueError, 'reassignment'):
            bind(self.conn, self.project, 'another')


if __name__ == '__main__':
    unittest.main()
