"""Project run binding: evidence and analysis are prerequisites, not completion prose."""
import json
import re
import sqlite3
from contextlib import closing
from pathlib import Path

from learning_memory import records
from learning_processing import digest
from learning_project import read_config


def load(project, run):
    if not isinstance(run, str) or not re.fullmatch(r'[a-zA-Z0-9_-]{1,80}', run):
        raise ValueError('A valid --run from begin is required')
    project = Path(project).resolve()
    path = project / '.agents/learning/runs' / run / 'analysis.json'
    analysis = json.loads(path.read_text(encoding='utf-8'))
    if analysis['run_id'] != run or analysis['project_id'] != read_config(project)['project_id']:
        raise ValueError('Run belongs to a different project')
    return path, analysis


def sources(project, ids):
    config = read_config(project)
    state = Path(project).resolve() / '.agents/learning'
    with closing(sqlite3.connect((state / 'experience.sqlite3').as_uri() + '?mode=ro', uri=True)) as conn:
        latest = {r['id']: r for r in records(conn, config['project_id'])}
        found, events = {}, {}
        def visit(identifier):
            if identifier in found:
                return
            if identifier not in latest:
                raise ValueError('Missing supporting memory: ' + str(identifier))
            record = latest[identifier]
            found[identifier] = digest(record)
            for key, values in record['payload'].items():
                if key == 'source_event_ids':
                    for event in values:
                        row = conn.execute('SELECT * FROM events WHERE id=? AND project_id=?',
                            (event, config['capture_project_id'])).fetchone()
                        events[event] = digest(row)  # Missing original events remain explicit.
                elif key.endswith('_ids') and isinstance(values, list):
                    for ref in values:
                        visit(ref)
            if record['episode_id'] != identifier:
                visit(record['episode_id'])
        for identifier in ids:
            visit(identifier)
    return {'memory': found, 'events': events}


def analysis_digest(analysis):
    return digest({k: analysis[k] for k in ('run_id', 'project_id', 'record_ids',
        'record_digests', 'source_digests', 'rule_snapshot', 'analysis_dependencies', 'analysis_required')})


def rule_snapshot(project):
    from learning_cycle import hash_text, processing_receipt, skill_inventory
    project = Path(project).resolve()
    inventory = skill_inventory(project) if any((project / '.agents/skills').glob('*/SKILL.md')) or any((project / 'skills').glob('*/SKILL.md')) else {}
    dependencies = processing_receipt([], {}, project, project)['dependencies']
    for path in [project / 'AGENTS.md', project / '.agents/AGENTS.md', *sorted((project / '.agents/common').rglob('*.md'))]:
        if path.is_file() and not path.is_symlink():
            dependencies['project:' + path.relative_to(project).as_posix()] = hash_text(path.read_text(encoding='utf-8-sig'))
    return ({path: {'sha256': item['sha256'], 'references': item['references']} for path, item in inventory.items()}, dependencies)


def validate_analysis(project, analysis):
    if analysis.get('source_digests') != sources(project, analysis['record_ids']):
        raise ValueError('Supporting evidence changed; begin a reviewed run')
    for identifier in analysis['record_ids']:
        fields = analysis['analysis_required'].get(identifier, {})
        required = {'scope', 'source_assessment', 'expected_vs_actual', 'causal_hypotheses',
                    'relevant_rules', 'measurable_goal', 'alternatives_and_sources', 'decision', 'verification'}
        if set(fields) != required or any(v is None or v in ('', [], {}) for v in fields.values()):
            raise ValueError('Complete diagnosis for every selected record')
        assessment = fields['source_assessment']
        if not isinstance(assessment, dict) or assessment.get('sufficiency') not in {'sufficient', 'insufficient', 'conflicting'}:
            raise ValueError('Source assessment must state sufficiency and context limitations')
        if not isinstance(assessment.get('limitations'), str) or not assessment['limitations'].strip():
            raise ValueError('State source limitations or explain why none were found')
        refs = assessment.get('archive_refs')
        if not isinstance(refs, list) or (not refs and not assessment.get('missing_telemetry_reason')):
            raise ValueError('Cite archived context or explain its absence')
        for ref in refs:
            relative = Path(ref['path'])
            archive = Path(project).resolve() / '.agents/learning/archive'
            path = (archive / relative).resolve(strict=True)
            if not path.is_relative_to(archive) or path.suffix != '.json':
                raise ValueError('Invalid archive reference')
            record = json.loads(path.read_text(encoding='utf-8'))
            if digest(record) != path.stem or record.get('project_id') != analysis['project_id']:
                raise ValueError('Archive reference identity/hash mismatch')
            if ref.get('usage') not in {'context', 'evidence'}:
                raise ValueError('Archive use must be classified')
            if ref['usage'] == 'evidence' and not record.get('assessment', {}).get('outcome_candidate'):
                raise ValueError('Observation is not outcome evidence')
        relevant = fields['relevant_rules']
        if not isinstance(relevant, list) or not relevant or any(p not in analysis['rule_snapshot'] for p in relevant):
            raise ValueError('Relevant rules must reference inspected rule paths')


def verify_rules(project, analysis, proposal=None):
    current, dependencies = rule_snapshot(project)
    if dependencies != analysis['analysis_dependencies']:
        raise ValueError('Analysis instructions changed; reassess the run')
    expected = dict(analysis['rule_snapshot'])
    if proposal and proposal.get('state') in {'applying', 'applied'}:
        repo = Path(proposal['repo'])
        for name, value in proposal.get('applied_hashes', {}).items():
            key = (repo / name).relative_to(Path(project)).as_posix()
            if key not in expected:
                raise ValueError('Applied rule was not inspected')
            if proposal['state'] == 'applying' and current.get(key) == expected[key]:
                continue  # Resume a partially applied journal.
            expected[key] = dict(expected[key], sha256=value)
    if current != expected:
        raise ValueError('Inspected rules changed; reassess the run')


def verify_binding(proposal, state, require_link=True):
    binding = proposal.get('run_binding')
    if not binding:
        repo = Path(proposal['repo']).resolve()
        host = repo.parent if repo.name == '.agents' else repo
        if (Path(state) / 'project.json').exists() or (host / '.agents/learning/project.json').exists():
            raise ValueError('Legacy proposal lacks a run binding; explicit reassessment required')
        return
    project = Path(binding['project']).resolve()
    if Path(state).resolve() != project / '.agents/learning':
        raise ValueError('Run and state do not belong to the same project')
    _, analysis = load(project, binding['run_id'])
    if require_link and analysis.get('proposal') != str(Path(state).resolve() / 'proposals' / (proposal['id'] + '.json')):
        raise ValueError('Run does not link this proposal; recover its binding before execution')
    validate_analysis(project, analysis)
    verify_rules(project, analysis, proposal)
    if analysis_digest(analysis) != binding['analysis_digest']:
        raise ValueError('Analysis changed after proposal creation')
    if proposal['project_id'] != read_config(project)['capture_project_id']:
        raise ValueError('Proposal project differs from run')
    if set(analysis['record_ids']) != {r['id'] for r in proposal['processing']['records']}:
        raise ValueError('Proposal work differs from run')
    for decision in proposal['decisions']:
        assessment = analysis['analysis_required'][decision['record_id']]['source_assessment']
        if assessment['sufficiency'] != 'sufficient' and decision['outcome'] != 'deferred':
            raise ValueError('Insufficient or conflicting evidence must be deferred')
