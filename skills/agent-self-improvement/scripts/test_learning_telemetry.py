import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from learning_project import initialize, read_config, write_json
from learning_telemetry import cleanup, export, prepare, sanitize


class TelemetryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        initialize(self.project)
        self.state = self.project / '.agents/learning'
        config = read_config(self.project)
        config['telemetry'].update(enabled=True, required_tags=[], project_metadata_key='project', project_metadata_value='stem')
        write_json(self.state / 'project.json', config)
        self.now = datetime(2026, 10, 27, tzinfo=UTC)

    def row(self, start, project='stem'):
        return dict(id='a', traceId='trace', startTime=start, metadata={'project': project}, type='TOOL', output={'secret': 'private'})

    def test_monthly_windows_overlap_archive_and_cleanup(self):
        calls = []
        def fetch(spec, start, end, cursor):
            calls.append((start, end, cursor))
            return {'data': [self.row(start), self.row(start, 'other')], 'meta': {}}
        result = export(self.project, fetch, self.now)
        self.assertEqual(result['pages'], 3)
        self.assertEqual(result['rejected'], 3)
        self.assertEqual(len(list((self.state / 'archive').glob('*/*.json'))), 3)
        prepared = prepare(self.project, 'run', ['2026-09', '2026-10'])
        self.assertEqual(prepared['entries'], 3)
        self.assertNotIn('private', Path(prepared['cache']).read_text())
        with self.assertRaises(ValueError):
            cleanup(self.project, 'run')
        write_json(self.state / 'runs/run/completion.json', {'decisions': 'durable'})
        cleanup(self.project, 'run')
        self.assertFalse(Path(prepared['cache']).exists())
        self.assertEqual(len(list((self.state / 'archive').glob('*/*.json'))), 3)
        export(self.project, fetch, self.now)
        self.assertEqual(len(calls), 4)  # 48-hour overlap, not another full month.

    def test_partial_failure_does_not_advance(self):
        def fetch(spec, start, end, cursor):
            if cursor:
                raise RuntimeError('http_429')
            return {'data': [self.row(start)], 'meta': {'cursor': 'next'}}
        result = export(self.project, fetch, self.now)
        self.assertEqual(result['status'], 'http_429')
        self.assertFalse((self.state / 'telemetry-watermark.json').exists())
        self.assertEqual(len(list((self.state / 'archive').glob('*/*.json'))), 1)

    def test_empty_is_not_quota_and_missing_mapping_no_network(self):
        result = export(self.project, lambda *args: {'data': [], 'meta': {}}, self.now)
        self.assertEqual(result['status'], 'empty_unknown_reason')
        config = read_config(self.project)
        config['telemetry']['project_metadata_key'] = None
        write_json(self.state / 'project.json', config)
        result = export(self.project, lambda *args: self.fail('network called'), self.now)
        self.assertTrue(result['database_only'])

    def test_cursor_cycle_and_traversal(self):
        result = export(self.project, lambda *args: {'data': [], 'meta': {'cursor': 'same'}}, self.now)
        self.assertEqual(result['status'], 'repeated_cursor')
        for run in ('../archive', 'a/b'):
            with self.assertRaises(ValueError):
                cleanup(self.project, run)
        self.assertEqual(sanitize({'Authorization': 'Basic sensitive'})['Authorization'], '[REDACTED]')

    def test_resume_after_page_budget_and_oversize(self):
        config = read_config(self.project)
        config['telemetry']['max_pages'] = 1
        write_json(self.state / 'project.json', config)
        export(self.project, lambda spec, start, end, cursor: {'data': [self.row(start)], 'meta': {'cursor': 'resume'}}, self.now)
        cursors = []
        def fetch(spec, start, end, cursor):
            cursors.append(cursor)
            return {'data': [], 'meta': {}}
        export(self.project, fetch, self.now)
        self.assertEqual(cursors[0], 'resume')
        self.assertFalse((self.state / 'telemetry-watermark.json').exists())

    def test_reduces_large_pages_and_excludes_validation(self):
        def fetch(spec, start, end, cursor):
            if spec.get('page_size', 10) > 2:
                raise RuntimeError('response_too_large')
            return {'data': [], 'meta': {}}
        self.assertEqual(export(self.project, fetch, self.now)['status'], 'empty_unknown_reason')
        from learning_telemetry import assess
        row = self.row(self.now.isoformat())
        row['tags'] = ['learning:validation']
        self.assertFalse(assess(row, read_config(self.project))['outcome_candidate'])


if __name__ == '__main__':
    unittest.main()
