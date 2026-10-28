"""Regression coverage for the consolidated project-learning release."""
import os
import tempfile
import unittest
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

from learning import capture, default_root, run_triage, set_mode
from learning_exchange import drain
from learning_memory import FIELDS, bind, open_store, save_records, session_context
from learning_project import initialize, read_config, write_json
from learning_tagging import connection_status, set_connection
from learning_telemetry import export_selected, prepare


class RevisionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.project = self.root / 'project with spaces'
        self.project.mkdir()
        with patch('learning.legacy_root', return_value=self.root / 'absent'):
            initialize(self.project)
        self.state = self.project / '.agents/learning'

    def test_default_state_spellings_and_explicit_precedence(self):
        for args in (['--project', str(self.project)], ['--project=' + str(self.project)]):
            with patch('sys.argv', ['learning.py', 'status', *args]), patch.dict(os.environ, {}, clear=True):
                self.assertEqual(default_root(), self.state)
            with patch('sys.argv', ['learning.py', '--state', str(self.root / 'explicit'), 'status', *args]), patch.dict(os.environ, {'AGENT_LEARNING_STATE': str(self.root / 'env')}, clear=True):
                self.assertEqual(default_root(), self.root / 'explicit')
        other = self.root / 'other'
        other.mkdir()
        with patch('sys.argv', ['learning.py', 'status', '--project=' + str(other)]), patch.dict(os.environ, {}, clear=True), patch('learning.legacy_root', return_value=self.root / 'absent'):
            self.assertEqual(default_root(), other / '.agents/learning')

    def test_legacy_history_requires_explicit_migration(self):
        other = self.root / 'legacy-project'
        other.mkdir()
        legacy = self.root / 'legacy'
        with closing(open_store(legacy)) as conn:
            bind(conn, other)
        before = (legacy / 'experience.sqlite3').read_bytes()
        with patch('learning.legacy_root', return_value=legacy):
            with self.assertRaisesRegex(ValueError, 'Legacy'):
                initialize(other)
            initialize(other, legacy=legacy)
        self.assertEqual((legacy / 'experience.sqlite3').read_bytes(), before)

    def test_paged_snapshot_does_not_skip_or_include_late_events(self):
        with closing(open_store(self.state)) as conn:
            set_mode(conn, self.project, True)
            for i in range(5):
                capture(conn, self.project, dict(client='test', session_id='s', message_id=str(i), kind='user', content=str(i)))
            page = session_context(conn, self.project, 'test', 's', limit=2)
            found = list(page['events'])
            capture(conn, self.project, dict(client='test', session_id='s', message_id='late', kind='user', content='late'))
            while page['next_cursor']:
                page = session_context(conn, self.project, 'test', 's', limit=2, cursor=page['next_cursor'])
                found.extend(page['events'])
            self.assertEqual([r['content'] for r in found], list(map(str, range(5))))
            self.assertEqual(len(session_context(conn, self.project, 'test', 's')['events']), 6)

    def test_triage_only_uncovered_events_and_explicit_reconsideration(self):
        with closing(open_store(self.state)) as conn:
            set_mode(conn, self.project, True)
            for i in range(2):
                capture(conn, self.project, dict(client='test', session_id='s', message_id=str(i), kind='user_correction', content='Correction ' + str(i)))
            ids = [r[0] for r in conn.execute('SELECT id FROM events ORDER BY rowid')]
            payload = {k: [] if k.endswith('_ids') else '' for k in FIELDS['episode']}
            payload.update(task='Review first correction', coverage='partial', source_event_ids=ids[:1], curation_state='reviewed', curation_reason='First event inspected')
            item = dict(id='episode', revision=1, project_id=read_config(self.project)['project_id'], episode_id='episode', kind='episode', status='candidate', payload=payload, provenance=dict(agent='test', client='test', skill_version='1.9.0', session_id='s'), created_at='2026-10-28T00:00:00+00:00')
            save_records(conn, item['project_id'], [item])
            self.assertEqual(run_triage(conn, self.state, self.project)['evidence_events'], 1)
            self.assertEqual(run_triage(conn, self.state, self.project)['evidence_events'], 1)
            self.assertEqual(run_triage(conn, self.state, self.project, reconsider=True)['evidence_events'], 2)

    def test_sync_is_off_and_unverified_repository_never_contacts_network(self):
        self.assertEqual(drain(self.project, lambda *a: self.fail('network'))['status'], 'disabled')
        with self.assertRaisesRegex(ValueError, 'unverified'):
            drain(self.project, lambda *a: self.fail('network'), explicit=True)
        config = read_config(self.project)
        config['remote'] = 'other/repository'
        write_json(self.state / 'project.json', config)
        with closing(open_store(self.state)) as conn, conn:
            conn.execute('UPDATE memory_projects SET sync_repository=?', ('approved/repository',))
        with self.assertRaisesRegex(ValueError, 'Conflicting'):
            drain(self.project, lambda *a: self.fail('network'), explicit=True)

    def test_connection_placeholders_refusal_reuse_and_overrides(self):
        credentials = self.root / 'global.json'
        write_json(credentials, dict(enabled=False, public_key='pk-lf-YOUR_KEY', secret_key='sk-lf-YOUR_SECRET', base_url='https://cloud.langfuse.com'))
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(connection_status(self.project, credentials)['credentials_present'])
            with self.assertRaisesRegex(ValueError, 'placeholder'):
                set_connection(self.project, True, True, credentials, authenticate=lambda *args: None)
            write_json(credentials, dict(enabled=False, public_key='pk-lf-test-public-value', secret_key='sk-lf-test-secret-value', base_url='https://cloud.langfuse.com'))
            original = credentials.read_bytes()
            self.assertEqual(set_connection(self.project, True, True, credentials, authenticate=lambda *args: None)['status'], 'configured_pending_readback')
            self.assertEqual(set_connection(self.project, False, True, credentials)['status'], 'disabled')
            self.assertEqual(credentials.read_bytes(), original)
            def invalid(*args):
                raise RuntimeError('http_401')
            with self.assertRaisesRegex(ValueError, 'Authentication'):
                set_connection(self.project, True, True, credentials, authenticate=invalid)
            self.assertFalse(read_config(self.project)['telemetry']['enabled'])
        with patch.dict(os.environ, {'TRACE_TO_LANGFUSE': 'true'}):
            with self.assertRaisesRegex(ValueError, 'overrides'):
                set_connection(self.project, False, True, credentials)

    def test_selected_windows_cache_and_archive_filter(self):
        config = read_config(self.project)
        config['telemetry'].update(enabled=True, required_tags=['project:test'])
        write_json(self.state / 'project.json', config)
        windows = [('2026-10-20T00:00:00Z', '2026-10-21T00:00:00Z'), ('2026-10-24T00:00:00Z', '2026-10-25T00:00:00Z')]
        calls = []
        def fetch(spec, start, end, cursor):
            calls.append((start, end))
            return dict(data=[dict(id=start, traceId=start, tags=['project:test'], startTime=start, input='fixture')], meta={})
        now = datetime(2026, 10, 28, tzinfo=UTC)
        first = export_selected(self.project, windows, fetch, now)
        self.assertEqual(first['pages'], 2)
        self.assertEqual(export_selected(self.project, windows, fetch, now)['cached_windows'], 2)
        self.assertEqual(len(calls), 2)
        self.assertEqual(prepare(self.project, 'selected', ['2026-10'], windows[:1])['entries'], 1)
        self.assertEqual(export_selected(self.project, [], fetch, now)['status'], 'unmatched')
        self.assertEqual(len(calls), 2)

    def test_selected_resume_budget_missing_dates_and_failure(self):
        config = read_config(self.project)
        config['telemetry'].update(enabled=True, required_tags=['project:test'], max_pages=1)
        write_json(self.state / 'project.json', config)
        window = [('2026-10-20T00:00:00Z', '2026-10-21T00:00:00Z')]
        now = datetime(2026, 10, 28, tzinfo=UTC)
        calls = []
        def fetch(spec, start, end, cursor):
            calls.append(cursor)
            return dict(data=[], meta={'cursor': 'next'} if not cursor else {})
        first = export_selected(self.project, window, fetch, now)
        self.assertEqual(first['status'], 'page_budget_exhausted')
        self.assertFalse(first['coverage_complete'])
        second = export_selected(self.project, window, fetch, now)
        self.assertTrue(second['coverage_complete'])
        self.assertEqual(calls, [None, 'next'])
        old = [('2020-01-01T00:00:00Z', '2020-01-02T00:00:00Z')]
        self.assertFalse(export_selected(self.project, old, lambda *a: self.fail('old date fetched'), now)['coverage_complete'])
        another = [('2026-10-22T00:00:00Z', '2026-10-23T00:00:00Z')]
        def unavailable(*args):
            raise RuntimeError('http_401')
        self.assertEqual(export_selected(self.project, another, unavailable, now)['status'], 'http_401')

    def test_explicit_memory_identity_and_default_local_only(self):
        other = self.root / 'new'
        other.mkdir()
        with patch('learning.legacy_root', return_value=self.root / 'absent'):
            initialize(other, memory_id='existing-portable-id')
        config = read_config(other)
        self.assertEqual(config['project_id'], 'existing-portable-id')
        self.assertIsNone(config['remote'])
        self.assertFalse(config['telemetry']['enabled'])
        self.assertFalse(config['auto_sync'])
        self.assertFalse((other / '.codex').exists())


if __name__ == '__main__':
    unittest.main()
