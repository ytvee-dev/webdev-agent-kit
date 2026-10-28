"""Project isolation, consent, capture integrity and pressure regressions."""
import base64
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from learning import capture, retain_raw, set_mode
from learning_exchange import drain, enqueue, restore
from learning_health import health_status, usage
from learning_memory import open_store, save_records, session_context
from learning_project import initialize, read_config, write_json
from learning_state import state_root
from learning_workflow import begin


class CaptureSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.project = self.root / 'project with spaces'
        self.project.mkdir()
        self.state = self.root / 'external memory'
        self.env = patch.dict(os.environ, {'AGENT_LEARNING_STATE': str(self.state)})
        self.env.start()
        self.addCleanup(self.env.stop)
        initialize(self.project)

    def consent(self, enabled=True, remote='example/private-memory'):
        config = read_config(self.project)
        config.update(remote=remote, auto_sync=enabled, sync_on_finish=enabled,
                      snapshot_choice='enabled' if enabled else 'declined')
        write_json(self.state / 'project.json', config)
        with closing(open_store(self.state)) as conn, conn:
            conn.execute('UPDATE memory_projects SET sync_repository=?', (remote,))
        return config

    def test_cli_resolver_all_spellings_and_other_working_directory(self):
        script = Path(__file__).with_name('learning.py')
        for project_args in (['--project', str(self.project)], ['--project=' + str(self.project)]):
            result = subprocess.run([sys.executable, str(script), '--state', str(self.state), 'status', *project_args],
                                    cwd=self.root, capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(result.stdout)['state'], str(self.state))
        self.assertFalse((self.project / '.agents/learning').exists())
        other = self.root / 'second project'
        other.mkdir()
        with self.assertRaisesRegex(ValueError, 'another project'):
            initialize(other)
        with patch.dict(os.environ, {'AGENT_LEARNING_STATE': str(self.root / 'second memory')}):
            initialize(other)
            self.assertNotEqual(read_config(other)['project_id'], read_config_at(self.state)['project_id'])

    def test_unconfigured_status_and_capture_do_not_create_store(self):
        script = Path(__file__).with_name('learning.py')
        missing = self.root / 'never initialized'
        for command in ('status', 'capture'):
            result = subprocess.run([sys.executable, str(script), '--state', str(missing), command,
                                     '--project', str(self.project)], input='{}', text=True,
                                    capture_output=True, check=True)
            self.assertFalse(json.loads(result.stdout)['recording'])
            self.assertFalse(missing.exists())

    def test_no_snapshot_without_consent_and_decline_preserves_old_queue(self):
        self.assertEqual(enqueue(self.project)['status'], 'disabled')
        self.assertFalse(list((self.state / 'snapshots').glob('*')))
        self.consent()
        enqueue(self.project)
        before = {p.name: p.read_bytes() for p in (self.state / 'outbox').glob('*')}
        self.consent(False)
        with patch('learning_exchange.gh') as api:
            self.assertEqual(enqueue(self.project)['status'], 'disabled')
            self.assertEqual(drain(self.project)['status'], 'disabled')
            api.assert_not_called()
        self.assertEqual(before, {p.name: p.read_bytes() for p in (self.state / 'outbox').glob('*')})

    def test_snapshot_excludes_archives_and_queue_is_destination_bound(self):
        self.consent()
        write_json(self.state / 'archive/2026-01/trace.json', {'secret': 'not for export'})
        result = enqueue(self.project)
        payload = json.loads((self.state / 'snapshots' / (result['snapshot'] + '.json')).read_text(encoding='utf-8'))
        self.assertFalse(payload['raw_events_included'])
        jobs = [json.loads(p.read_text(encoding='utf-8')) for p in (self.state / 'outbox').glob('*.json')]
        self.assertEqual(len(jobs), 1)
        self.assertTrue(jobs[0]['path'].startswith('snapshots/'))
        self.consent(remote='example/new-destination')
        calls = []
        def api(route, *args, **kwargs):
            calls.append(route)
            return {'private': True}
        result = drain(self.project, api)
        self.assertEqual(result['uploaded'], 0)
        self.assertEqual(calls, ['repos/example/new-destination'])
        enqueue(self.project)
        self.assertEqual(len(list((self.state / 'outbox').glob('*.json'))), 2)

    def test_capture_ids_timestamps_and_health_without_contents(self):
        event = dict(client='test', session_id='session', message_id='one', kind='user',
                     content='token=secret-value-value', timestamp='2020-01-01T00:00:00+00:00')
        with closing(open_store(self.state)) as conn:
            set_mode(conn, self.project, True)
            first = capture(conn, self.project, event)
            self.assertTrue(capture(conn, self.project, event)['duplicate'])
            del event['message_id']
            second = capture(conn, self.project, event)
            third = capture(conn, self.project, event)
            self.assertNotEqual(second['id'], third['id'])
            page = session_context(conn, self.project, 'test', 'session')
            metadata = page['events'][0]['capture_metadata']
            self.assertNotEqual(metadata['source_timestamp'], metadata['received_at'])
            self.assertNotIn('secret-value-value', str(page))
            self.assertTrue(first['recorded'])
        self.assertEqual(health_status(self.project)['status'], 'observed')
        self.assertNotIn(b'secret-value-value', (self.state / 'capture-health.sqlite3').read_bytes())

    def test_empty_private_repository_bootstraps_with_readback(self):
        from learning_exchange import drain_batch
        self.consent()
        enqueue(self.project)
        stored = {}
        def api(route, *args, **kwargs):
            if route.endswith('/branches?per_page=1'):
                return []
            if '/contents/' not in route:
                return {'private': True, 'size': 0, 'default_branch': 'main'}
            if kwargs.get('input_data'):
                stored[route] = json.loads(kwargs['input_data'])['content']
                return {}
            return {'content': stored[route]}
        self.assertEqual(drain_batch(self.project, api)['status'], 'synced')
        self.assertEqual(len(stored), 1)
        self.assertFalse(json.loads(base64.b64decode(next(iter(stored.values()))))['raw_events_included'])

    def test_hook_bounds_input_and_storage_lock_without_blocking_host(self):
        bridge = Path(__file__).resolve().parents[1] / 'assets/integrations/hook_bridge.py'
        oversized = subprocess.run([sys.executable, str(bridge), '--client', 'codex'],
                                  input='x' * 262145, text=True, capture_output=True, timeout=8)
        self.assertEqual(oversized.returncode, 0)
        with closing(open_store(self.state)) as conn:
            set_mode(conn, self.project, True)
            conn.execute('BEGIN IMMEDIATE')
            locked = subprocess.run([sys.executable, str(bridge), '--client', 'codex'],
                                    input=json.dumps(dict(hook_event_name='Stop', cwd=str(self.project),
                                        session_id='s', turn_id='1', last_assistant_message='test')),
                                    text=True, capture_output=True, timeout=8)
            conn.rollback()
        self.assertEqual(locked.returncode, 0)
        self.assertEqual(json.loads(locked.stdout), {})
        counters = health_status(self.project)['counters']
        self.assertTrue(any(r['status'] == 'error' for r in counters))

    def test_installed_hook_retains_external_state_without_environment_override(self):
        import shlex
        installer = Path(__file__).with_name('install_hooks.py')
        subprocess.run([sys.executable, str(installer), '--project', str(self.project),
                        '--state', str(self.state), '--approve'], capture_output=True, check=True)
        hooks = json.loads((self.project / '.codex/hooks.json').read_text(encoding='utf-8'))
        command = hooks['hooks']['Stop'][-1]['hooks'][0]['command']
        with closing(open_store(self.state)) as conn:
            set_mode(conn, self.project, True)
        env = dict(os.environ)
        env.pop('AGENT_LEARNING_STATE', None)
        result = subprocess.run(shlex.split(command), env=env, capture_output=True, text=True, check=True,
                                input=json.dumps(dict(hook_event_name='Stop', cwd=str(self.project),
                                    session_id='s', turn_id='stable', last_assistant_message='captured')))
        self.assertEqual(json.loads(result.stdout), {})
        with closing(open_store(self.state)) as conn:
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM events').fetchone()[0], 1)
        self.assertFalse((self.project / '.agents/learning').exists())

    def test_pressure_asks_without_deleting_or_disabling(self):
        config = read_config(self.project)
        config['storage_limits'] = {'events': 1, 'database_bytes': 1}
        write_json(self.state / 'project.json', config)
        with closing(open_store(self.state)) as conn:
            set_mode(conn, self.project, True)
            capture(conn, self.project, dict(client='test', session_id='session', message_id='one',
                    kind='user', content='old unprocessed event', timestamp='2020-01-01T00:00:00+00:00'))
        result = usage(self.project)
        self.assertTrue(result['cleanup_permission_required'])
        self.assertEqual(result['events'], 1)
        self.assertEqual(result['preview']['eligible'], 0)
        with closing(open_store(self.state)) as conn:
            self.assertEqual(conn.execute('SELECT recording FROM projects').fetchone()[0], 1)
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM events').fetchone()[0], 1)

    def test_restore_structured_snapshot_and_external_analysis(self):
        from test_learning_memory import ProjectMemoryTests
        config = self.consent()
        fixture = ProjectMemoryTests()
        fixture.pid = config['project_id']
        with closing(open_store(self.state)) as conn:
            save_records(conn, config['project_id'], fixture.sample())
        with patch('learning_workflow.export_selected', return_value={'database_only': True}):
            analysis = begin(self.project, ['lesson'])
        self.assertTrue((self.state / 'runs' / analysis['run_id'] / 'analysis.json').is_file())
        snapshot = enqueue(self.project)['snapshot']
        backup = self.state / 'snapshots' / (snapshot + '.json')
        with patch.dict(os.environ, {'AGENT_LEARNING_STATE': str(self.root / 'restored')}):
            initialize(self.project, memory_id=config['project_id'])
            self.assertGreater(restore(self.project, backup)['inserted'], 0)
            self.assertEqual(state_root(self.project), self.root / 'restored')

    def test_referenced_evidence_survives_explicit_cleanup(self):
        from test_learning_memory import ProjectMemoryTests
        config = read_config(self.project)
        fixture = ProjectMemoryTests()
        fixture.pid = config['project_id']
        with closing(open_store(self.state)) as conn:
            set_mode(conn, self.project, True)
            event = capture(conn, self.project, dict(client='test', session_id='session', message_id='one',
                            kind='user', content='evidence', timestamp='2020-01-01T00:00:00+00:00'))
            items = fixture.sample()
            episode = next(r for r in items if r['kind'] == 'episode')
            episode['payload'].update(source_event_ids=[event['id']], curation_state='reviewed', curation_reason='Reviewed this source event')
            save_records(conn, config['project_id'], items)
            result = retain_raw(conn, self.project, 30, apply=True, processed_only=True)
            self.assertEqual(result['deleted'], 0)
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM events').fetchone()[0], 1)


def read_config_at(state):
    return json.loads((state / 'project.json').read_text(encoding='utf-8'))
