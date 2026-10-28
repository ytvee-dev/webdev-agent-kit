"""Acceptance regressions; disposable databases and injected telemetry only."""
import json
import tempfile
import unittest
from argparse import Namespace
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from learning_memory import open_store, save_records
from learning_processing import connect, lock
from learning_project import initialize, read_config, write_json
from learning_tagging import validate
from learning_workflow import begin, finish, verification_plan


class ClosureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        initialize(self.project)
        self.state = self.project / '.agents/learning'
        self.config = read_config(self.project)
        from test_learning_memory import ProjectMemoryTests
        fixture = ProjectMemoryTests()
        fixture.pid = self.config['project_id']
        with closing(open_store(self.state)) as conn:
            save_records(conn, self.config['project_id'], fixture.sample())

    def prepared(self, change=False):
        from learning_cycle import apply, check, propose
        target = self.project / '.agents/skills/example/SKILL.md'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('---\nname: example\ndescription: test\n---\nVerify.\n', encoding='utf-8')
        if change:
            from learning_memory import records
            with closing(open_store(self.state)) as conn:
                evidence = next(r for r in records(conn, self.config['project_id']) if r['kind'] == 'evidence')
                evidence.update(revision=2, status='verified')
                evidence['payload'].update(source_type='test', source_ref='fixture-test', availability='local_only',
                    summary='Observed failure', source_revision='fixture-v1', procedure='Check outcome', result='failed')
                save_records(conn, self.config['project_id'], [evidence])
        with patch('learning_workflow.export', return_value={'database_only': True}):
            analysis = begin(self.project, ['lesson'])
        folder = self.state / 'runs' / analysis['run_id']
        analysis['analysis_required']['lesson'] = {k: 'fixture diagnosis' for k in analysis['analysis_required']['lesson']}
        analysis['analysis_required']['lesson']['source_assessment'] = {
            'sufficiency': 'sufficient', 'limitations': 'Synthetic test only', 'archive_refs': [], 'missing_telemetry_reason': 'offline fixture'}
        analysis['analysis_required']['lesson']['relevant_rules'] = ['.agents/skills/example/SKILL.md']
        analysis['reflection'] = dict(checked='fixture outcome', failed='none', limitations='synthetic test', next_improvement='none justified')
        write_json(folder / 'analysis.json', analysis)
        source = self.project / 'suggestion.json'
        write_json(source, {'schema_version': 1, 'decisions': [{'record_id': 'lesson',
            'outcome': 'pending' if change else 'no_change', 'reason': 'Fixture rule reviewed'}],
            'changes': [{'path': '.agents/skills/example/SKILL.md', 'find': 'Verify.',
                'replace': 'Verify results.', 'evidence_ids': ['lesson', 'evidence']}] if change else []})
        args = Namespace(project=str(self.project), state=str(self.state), repo=str(self.project),
            run=analysis['run_id'], engine=None, proposal_file=str(source), batch_size=8, force=False, timeout=30)
        proposal = propose(args)
        args.proposal = proposal['proposal']
        if change:
            check(args)
            args.approve, args.accept_unevaluated = True, True  # Disposable mechanics test only.
            apply(args)
        return analysis, folder, args

    def test_linked_completion_is_idempotent_and_offline_queue_survives(self):
        analysis, folder, args = self.prepared(change=True)
        with patch('learning_workflow.drain', return_value={'status': 'pending_retry'}):
            first = finish(self.project, analysis['run_id'])
            receipt = (folder / 'completion.json').read_bytes()
            with closing(connect(self.state)) as conn:
                count = conn.execute('SELECT COUNT(*) FROM learning_decisions').fetchone()[0]
            finish(self.project, analysis['run_id'])
        self.assertEqual((folder / 'completion.json').read_bytes(), receipt)
        with closing(connect(self.state)) as conn:
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM learning_decisions').fetchone()[0], count)
        self.assertEqual(first['sync']['status'], 'pending_retry')
        self.assertTrue(list((self.state / 'outbox').glob('*.json')))

    def test_changed_rule_or_missing_reflection_blocks_finish(self):
        analysis, folder, args = self.prepared()
        current = json.loads((folder / 'analysis.json').read_text())
        current['reflection'] = None
        write_json(folder / 'analysis.json', current)
        with self.assertRaisesRegex(ValueError, 'reflection'):
            finish(self.project, analysis['run_id'])
        current['reflection'] = analysis['reflection']
        write_json(folder / 'analysis.json', current)
        (self.project / '.agents/skills/example/SKILL.md').write_text('Changed rule', encoding='utf-8')
        with self.assertRaises(ValueError):
            finish(self.project, analysis['run_id'])
        self.assertTrue((folder / 'telemetry.jsonl').exists())

    def test_used_marker_is_required_for_linked_apply(self):
        analysis, folder, args = self.prepared(change=True)
        with closing(connect(self.state)) as conn, conn:
            conn.execute("UPDATE learning_decisions SET details=json_set(details, '$.used', json('false')) WHERE outcome='applied'")
        with self.assertRaisesRegex(ValueError, 'used receipt'):
            finish(self.project, analysis['run_id'])
        self.assertTrue((folder / 'telemetry.jsonl').exists())

    def test_linked_apply_recovers_after_files_before_receipts(self):
        from learning_cycle import apply
        with patch('learning_cycle.complete_processing', side_effect=RuntimeError('simulated crash')):
            with self.assertRaisesRegex(RuntimeError, 'simulated crash'):
                self.prepared(change=True)
        path = next((self.state / 'proposals').glob('*.json'))
        proposal = json.loads(path.read_text())
        target = self.project / '.agents/skills/example/SKILL.md'
        before = target.read_bytes()
        args = Namespace(state=str(self.state), repo=str(self.project), proposal=str(path),
                         approve=True, accept_unevaluated=True)
        self.assertEqual(apply(args)['result'], 'already_applied')
        self.assertEqual(target.read_bytes(), before)
        with patch('learning_workflow.drain', return_value={'status': 'pending_retry'}):
            finish(self.project, proposal['run_binding']['run_id'])

    def test_wrong_project_and_missing_run_rejected_before_analysis(self):
        from learning_cycle import propose
        with patch('learning_cycle.propose_locked') as implementation:
            with self.assertRaisesRegex(ValueError, '--run'):
                propose(Namespace(project=str(self.project), repo=str(self.project), state=str(self.state)))
            implementation.assert_not_called()
            with self.assertRaisesRegex(ValueError, 'own state'):
                propose(Namespace(project=str(self.project), repo=str(self.project), state=str(self.project / 'other-state')))
            implementation.assert_not_called()
        analysis, folder, args = self.prepared()
        current = json.loads((folder / 'analysis.json').read_text())
        current['project_id'] = 'other-project'
        write_json(folder / 'analysis.json', current)
        with self.assertRaisesRegex(ValueError, 'different project'):
            finish(self.project, analysis['run_id'])

    def test_legacy_recovery_requires_explicit_flag_and_never_repatches(self):
        from learning_cycle import apply
        analysis, folder, args = self.prepared(change=True)
        path = Path(args.proposal)
        proposal = json.loads(path.read_text())
        proposal.pop('run_binding')
        write_json(path, proposal)
        with self.assertRaisesRegex(ValueError, 'Legacy proposal'):
            apply(args)
        original_state = args.state
        args.state = str(self.project / 'other-state')
        with self.assertRaisesRegex(ValueError, 'Legacy proposal'):
            apply(args)
        args.state = original_state
        before = (self.project / '.agents/skills/example/SKILL.md').read_bytes()
        args.recover_legacy = True
        self.assertEqual(apply(args)['result'], 'already_applied')
        self.assertEqual((self.project / '.agents/skills/example/SKILL.md').read_bytes(), before)

    def test_changed_supporting_source_rejects_finish(self):
        from learning_memory import records
        analysis, folder, args = self.prepared()
        with closing(open_store(self.state)) as conn:
            record = next(r for r in records(conn, self.config['project_id']) if r['id'] == 'evidence')
            record['revision'] += 1
            record['payload']['summary'] = 'New contrary evidence'
            save_records(conn, self.config['project_id'], [record])
        with self.assertRaisesRegex(ValueError, 'evidence changed'):
            finish(self.project, analysis['run_id'])

    def test_foreign_run_and_changed_analysis_are_rejected(self):
        analysis, folder, args = self.prepared()
        proposal = json.loads(Path(args.proposal).read_text())
        proposal['run_binding']['run_id'] = 'other-run'
        write_json(Path(args.proposal), proposal)
        with self.assertRaises((OSError, ValueError)):
            finish(self.project, analysis['run_id'])
        proposal['run_binding']['run_id'] = analysis['run_id']
        write_json(Path(args.proposal), proposal)
        current = json.loads((folder / 'analysis.json').read_text())
        current['analysis_required']['lesson']['measurable_goal'] = 'Changed goal'
        write_json(folder / 'analysis.json', current)
        with self.assertRaisesRegex(ValueError, 'Analysis changed'):
            finish(self.project, analysis['run_id'])

    def test_unknown_risk_and_crlf_equivalence(self):
        self.assertEqual(verification_plan(['a'])['risk'], 'high')
        self.assertEqual(verification_plan(['a'], [{'find': 'same\r\n', 'replace': 'same\n'}])['risk'], 'standard')

    def test_telemetry_unavailable_and_foreign_tags(self):
        def unavailable(*args):
            raise RuntimeError('not_connected')
        self.assertEqual(validate(self.project, unavailable)['status'], 'unavailable')
        tags = ['webdev-agent-kit', 'project-id:' + self.config['project_id'], 'project-id:foreign']
        self.assertEqual(validate(self.project, lambda *args: {'data': [{'tags': tags}]})['status'], 'mismatch')

    def test_stale_used_receipt_cannot_finish_new_run(self):
        with closing(connect(self.state)) as conn, conn:
            conn.execute('INSERT INTO learning_decisions (project_id,repo,record_id,record_digest,skill_digest,outcome,proposal,updated_at,reason,recheck_when,details) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                (self.config['capture_project_id'], str(self.project), 'lesson', 'stale', 'stale', 'applied', 'old.json', '2020', 'old', '', '{"used":true}'))
        with patch('learning_workflow.export', return_value={'database_only': True}):
            analysis = begin(self.project, ['lesson'])
        folder = self.state / 'runs' / analysis['run_id']
        analysis['analysis_required']['lesson'] = {key: 'reviewed fixture' for key in analysis['analysis_required']['lesson']}
        write_json(folder / 'analysis.json', analysis)
        with patch('learning_workflow.drain') as drain:
            with self.assertRaises(ValueError):
                finish(self.project, analysis['run_id'])
            drain.assert_not_called()
        self.assertTrue((folder / 'telemetry.jsonl').exists())
        self.assertFalse((folder / 'completion.json').exists())

    def test_busy_optional_telemetry_preserves_db_run(self):
        with lock(self.state, self.state / 'telemetry'):
            result = begin(self.project, ['lesson'])
        self.assertTrue(result['telemetry']['database_only'])
        self.assertEqual(result['telemetry']['reason'], 'busy')

    def test_unknown_multilingual_change_requires_high_depth(self):
        plan = verification_plan(['skills/general/SKILL.md'],
            [{'find': 'Ask before deleting data.', 'replace': '\u0423\u0434\u0430\u043b\u044f\u0442\u044c \u0431\u0435\u0437 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u044f'}])
        self.assertEqual(plan['risk'], 'high')

    def test_control_trace_found_after_first_page(self):
        write_json(self.state / 'tag-probe.json', {'session_id': 'control'})
        tags = ['webdev-agent-kit', 'project-id:' + self.config['project_id']]
        calls = []
        def fetch(spec, start, end, cursor=None):
            calls.append(cursor)
            row = {'id': 'a', 'traceId': 't', 'tags': tags,
                   'sessionId': 'control' if cursor else 'ordinary'}
            return {'data': [row], 'meta': {} if cursor else {'cursor': 'next'}}
        result = validate(self.project, fetch)
        self.assertEqual(result['status'], 'verified')
        self.assertEqual(calls, [None, 'next'])


if __name__ == '__main__':
    unittest.main()
