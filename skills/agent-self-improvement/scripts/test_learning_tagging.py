import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from learning_project import initialize, read_config, write_json
from learning_tagging import configure, validate
from learning_telemetry import assess


class TaggingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        initialize(self.project)
        configure(self.project)

    def test_setup_preserves_settings_and_requires_real_readback(self):
        path = self.project / '.codex/langfuse.json'
        write_json(path, {'enabled': False, 'tags': ['custom', 'project:existing']})
        with patch.dict(os.environ, {}, clear=True):
            first = configure(self.project)
            self.assertEqual(configure(self.project), first)
        self.assertFalse(json.loads(path.read_text())['enabled'])
        self.assertIn('custom', first['tags'])
        self.assertEqual(validate(self.project, lambda *args: {'data': []})['status'], 'not_found')
        row = {'id': 'a', 'traceId': 't', 'tags': first['tags']}
        self.assertEqual(validate(self.project, lambda *args: {'data': [row]})['status'], 'pending_readback')
        write_json(self.project / '.agents/learning/tag-probe.json', {'session_id': 'probe'})
        row['sessionId'] = 'probe'
        self.assertEqual(validate(self.project, lambda *args: {'data': [row]})['status'], 'verified')

    def test_wrong_project_and_env_override(self):
        with patch.dict(os.environ, {'LANGFUSE_CODEX_TAGS': 'global'}):
            with self.assertRaisesRegex(ValueError, 'overrides'):
                configure(self.project)
        with patch.dict(os.environ, {}, clear=True):
            configure(self.project)

    def test_two_projects_remain_isolated_when_one_is_disabled(self):
        other = self.project / 'other'
        other.mkdir()
        initialize(other, local_only=True)
        with patch.dict(os.environ, {}, clear=True):
            first = configure(self.project)
            second = configure(other)
        self.assertNotEqual(read_config(self.project)['project_id'], read_config(other)['project_id'])
        row = {'id': 'foreign', 'traceId': 'foreign', 'tags': second['tags']}
        self.assertEqual(validate(self.project, lambda *args: {'data': [row]})['status'], 'mismatch')
        first_path = self.project / '.codex/langfuse.json'
        second_path = other / '.codex/langfuse.json'
        write_json(first_path, {'enabled': True, 'tags': first['tags']})
        before = first_path.read_bytes()
        write_json(second_path, {'enabled': False, 'tags': second['tags']})
        self.assertEqual(first_path.read_bytes(), before)
        self.assertEqual(configure(other)['tags'], second['tags'])

    def test_friendly_tag_only_is_limited_to_historical_scope(self):
        config = read_config(self.project)
        tags = config['telemetry']['required_tags']
        self.assertTrue(assess({'tags': tags, 'startTime': '2020-01-01T00:00:00Z'}, config)['project_match'])
        self.assertFalse(assess({'tags': tags, 'startTime': '2099-01-01T00:00:00Z'}, config)['project_match'])
        self.assertFalse(assess({'tags': tags}, config)['project_match'])
        config = read_config(self.project)
        tags = config['telemetry']['required_tags'] + ['project-id:foreign']
        self.assertFalse(assess({'tags': tags}, config)['project_match'])
        write_json(self.project / '.codex/langfuse.json', {'tags': ['project-id:foreign']})
        with self.assertRaisesRegex(ValueError, 'Different project'):
            configure(self.project)


if __name__ == '__main__':
    unittest.main()
