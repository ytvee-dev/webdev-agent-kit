import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from learning_exchange import drain, enqueue
from learning_project import initialize, read_config, write_json
from learning_workflow import begin, curate_queue, verification_plan


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        initialize(self.project)
        self.state = self.project / '.agents/learning'
        config = read_config(self.project)
        config.update(remote='example/private-memory', auto_sync=True, sync_on_finish=True)
        write_json(self.state / 'project.json', config)
        with closing(sqlite3.connect(self.state / 'experience.sqlite3')) as conn, conn:
            conn.execute('UPDATE memory_projects SET sync_repository=?', ('example/private-memory',))

    def test_background_entrypoints_fail_before_work(self):
        from learning_schedule import install
        from learning_workflow import maintenance
        with patch('learning_workflow.curate_queue') as curate, patch('learning_workflow.export') as export, patch('learning_workflow.drain') as drain, patch('learning_schedule.subprocess.run') as process:
            with self.assertRaisesRegex(ValueError, 'disabled'):
                maintenance(self.project)
            with self.assertRaisesRegex(ValueError, 'disabled'):
                install(self.project)
            for operation in (curate, export, drain, process):
                operation.assert_not_called()

    def test_git_batch_readback_lost_response_and_conflict(self):
        import hashlib

        from learning_exchange import drain_batch
        enqueue(self.project)
        stored, pending = {}, {}
        commits = []
        lose_response = [True]
        config = read_config(self.project)
        prefix = config['remote_folder'] + '/'
        def api(route, *args, **kwargs):
            if route == 'repos/' + config['remote']:
                return {'private': True, 'default_branch': 'main'}
            if '/git/ref/heads/' in route:
                return {'object': {'sha': 'head'}}
            if '/git/commits/' in route:
                return {'tree': {'sha': 'root'}}
            if route.endswith('/git/trees/root'):
                return {'tree': [{'path': config['remote_folder'], 'type': 'tree', 'sha': 'project'}]}
            if route.endswith('/git/trees/project?recursive=1'):
                return {'tree': [{'path': name, 'sha': sha, 'type': 'blob', 'mode': '100644'} for name, sha in stored.items()]}
            body = json.loads(kwargs['input_data'])
            if route.endswith('/git/trees'):
                for entry in body['tree']:
                    data = entry['content'].encode()
                    pending[entry['path'].removeprefix(prefix)] = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                return {'sha': 'new-tree'}
            if route.endswith('/git/commits'):
                commits.append(body)
                return {'sha': 'new-commit'}
            if '/git/refs/heads/' in route:
                self.assertFalse(body['force'])
                stored.update(pending)
                if lose_response[0]:
                    lose_response[0] = False
                    raise ValueError('Lost PATCH response')
                return {}
            raise AssertionError(route)
        first = drain_batch(self.project, api)
        self.assertEqual(first['stage'], 'advance_branch')
        self.assertTrue(list((self.state / 'outbox').glob('*.json')))
        self.assertEqual(drain_batch(self.project, api)['status'], 'synced')
        self.assertEqual(len(commits), 1)
        sent = next((self.state / 'outbox').glob('*.sent'))
        sent.rename(sent.with_suffix('.json'))
        stored[next(iter(stored))] = 'conflicting-blob'
        self.assertEqual(drain_batch(self.project, api)['reason'], 'remote_conflict')
        self.assertTrue(list((self.state / 'outbox').glob('*.json')))

    def test_snapshot_retry_and_used_receipts(self):
        from learning_processing import connect
        config = read_config(self.project)
        conn = connect(self.state)
        with conn:
            conn.execute('INSERT INTO learning_decisions (project_id,repo,record_id,record_digest,skill_digest,outcome,proposal,updated_at,reason,recheck_when,details) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                         (config['capture_project_id'], str(self.project / '.agents'), 'lesson', 'recordhash', 'rulehash', 'applied', 'example.json', '2026-10-27', 'verified', '', '{"used":true}'))
        conn.close()
        first = enqueue(self.project)
        self.assertEqual(enqueue(self.project)['snapshot'], first['snapshot'])
        payload = json.loads((self.state / 'snapshots' / (first['snapshot'] + '.json')).read_text())
        self.assertTrue(payload['processing_history'][0]['details']['used'])
        self.assertFalse(payload['raw_events_included'])
        from learning_exchange import restore
        path = self.state / 'snapshots' / (first['snapshot'] + '.json')
        self.assertEqual(restore(self.project, path)['patches_applied'], 0)
        self.assertEqual(restore(self.project, path)['history_restored_for_review'], 1)
        def unavailable(*args, **kwargs):
            raise ValueError('offline')
        self.assertEqual(drain(self.project, unavailable)['status'], 'pending_retry')
        self.assertEqual(len(list((self.state / 'outbox').glob('*.json'))), 1)
        saved = {}
        def api(route, *args, **kwargs):
            if '/contents/' not in route:
                return {'private': True}
            if args:
                saved[route] = json.loads(kwargs['input_data'])['content']
                raise ValueError('lost response')
            return {'content': saved[route]}
        self.assertEqual(drain(self.project, api)['uploaded'], 1)
        self.assertEqual(enqueue(self.project)['pending'], 0)

    def test_public_remote_and_outbox_escape(self):
        enqueue(self.project)
        self.assertEqual(drain(self.project, lambda *args: {'private': False})['status'], 'pending_retry')
        job = next((self.state / 'outbox').glob('*.json'))
        write_json(job, {'path': '../../outside', 'sha256': 'x'})
        self.assertEqual(drain(self.project, lambda *args: {'private': True})['status'], 'blocked_review')
        self.assertTrue(job.exists())

    def test_risk_and_empty_queue_do_not_train(self):
        self.assertEqual(verification_plan(['skills/button/SKILL.md'])['repetitions'], 2)
        self.assertEqual(len(verification_plan(['skills/agent-self-improvement/SKILL.md'])['scenarios']), 6)
        self.assertEqual(verification_plan(['skills/button/SKILL.md'], [{'replace': 'Change approval checks'}])['risk'], 'high')
        self.assertEqual(curate_queue(self.project)['sessions_pending'], 0)
        with self.assertRaises(ValueError):
            begin(self.project, ['missing'])



if __name__ == '__main__':
    unittest.main()
