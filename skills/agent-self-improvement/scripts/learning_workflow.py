"""Explicitly requested preparation and completion; no background execution."""
import argparse
import hashlib
import json
import sqlite3
import time
import uuid
from contextlib import closing
from datetime import UTC, datetime, timedelta
from pathlib import Path

from learning_exchange import drain, enqueue
from learning_memory import records
from learning_project import read_config, write_json
from learning_telemetry import cleanup, export, prepare, timestamp


def verification_plan(paths, changes=()):
    # A natural-language classifier cannot prove absence of behavioral impact.
    # Only a mechanically identical text (apart from CRLF) gets reduced depth.
    unchanged = bool(changes) and all(
        isinstance(c.get('find'), str) and isinstance(c.get('replace'), str)
        and c['find'].replace('\r\n', '\n') == c['replace'].replace('\r\n', '\n')
        for c in changes)
    high = not unchanged
    return {'risk': 'high' if high else 'standard', 'structural': True, 'textual_is_behavioral': False,
            'scenarios': ['incident', 'held_out', 'negative_scope'] + (['partial_queue', 'recovery', 'false_success'] if high else []),
            'repetitions': 2 if high else 1, 'variants': ['baseline', 'candidate'], 'timeout_seconds': 180,
            'pass_condition': 'actual environment outcomes, all candidate constraints, no observed regression',
            'frozen_before_edit': True,
            'impact': 'behavior_unknown' if high else 'text_equivalent',
            'impact_basis': 'Semantic edits require full coverage' if high else 'Exact equality after CRLF normalization'}


def curate_queue(project):
    """Index raw sessions for separate semantic curation; never invent a lesson."""
    state = Path(project).resolve() / '.agents/learning'
    config = read_config(project)
    with closing(sqlite3.connect(state / 'experience.sqlite3')) as conn, conn:
        conn.execute('CREATE TABLE IF NOT EXISTS curation_queue (client TEXT, session_id TEXT, event_count INTEGER, last_event TEXT, state TEXT, PRIMARY KEY(client, session_id))')
        rows = conn.execute('SELECT client,session_id,COUNT(*),MAX(timestamp) FROM events WHERE project_id=? GROUP BY client,session_id', (config['capture_project_id'],)).fetchall()
        for client, session, count, last in rows:
            conn.execute("INSERT INTO curation_queue VALUES (?,?,?,?,'pending') ON CONFLICT(client,session_id) DO UPDATE SET event_count=excluded.event_count,last_event=excluded.last_event,state='pending' WHERE curation_queue.event_count != excluded.event_count OR curation_queue.last_event != excluded.last_event", (client, session, count, last))
        from learning_memory import curated_event_ids
        covered = curated_event_ids(conn, project)
        for client, session, count, last in rows:
            source_ids = {r[0] for r in conn.execute('SELECT id FROM events WHERE project_id=? AND client=? AND session_id=?', (config['capture_project_id'], client, session))}
            queue_state = 'curated' if source_ids and source_ids <= covered else 'pending'
            conn.execute('UPDATE curation_queue SET state=? WHERE client=? AND session_id=?', (queue_state, client, session))
        return {'sessions_pending': conn.execute("SELECT COUNT(*) FROM curation_queue WHERE state='pending'").fetchone()[0]}


def maintenance(project):
    raise ValueError('Background maintenance is disabled. Run explicit workflow stages only at the user request.')


def begin(project, ids):
    state = Path(project).resolve() / '.agents/learning'
    config = read_config(project)
    with closing(sqlite3.connect(state / 'experience.sqlite3')) as conn:
        latest = {r['id']: r for r in records(conn, config['project_id'])}
    if not ids or len(ids) > 32 or len(ids) != len(set(ids)):
        raise ValueError('Select 1..32 unique work records')
    if any(i not in latest or latest[i]['kind'] not in {'lesson', 'requirement'} for i in ids):
        raise ValueError('Work must reference known lessons or requirements')
    selected = [latest[i] for i in ids]
    from learning_run import rule_snapshot, sources
    source_digests = sources(project, ids)
    days = set()
    # Include the same recursive evidence graph that is pinned for verification.
    # Curation timestamps cannot stand in for actual incident dates.
    with closing(sqlite3.connect(state / 'experience.sqlite3')) as conn:
        for event_id in source_digests['events']:
            row = conn.execute('SELECT timestamp FROM events WHERE id=? AND project_id=?', (event_id, config['capture_project_id'])).fetchone()
            if row:
                days.add(timestamp(row[0]).astimezone(UTC).date())
    windows = [(datetime.combine(day, datetime.min.time(), tzinfo=UTC).isoformat(),
                min(datetime.combine(day + timedelta(days=1), datetime.min.time(), tzinfo=UTC), datetime.now(UTC)).isoformat())
               for day in sorted(days)]
    months = sorted({start[:7] for start, _ in windows})
    run = uuid.uuid4().hex
    from learning_processing import LearningBusy
    try:
        if not windows or len(windows) > 32:
            telemetry = {'database_only': True, 'coverage_complete': False, 'reason': 'source_dates_unavailable_or_excessive'}
        else:
            results = []
            budget = {'deadline': time.monotonic() + 120,
                      'pages_remaining': min(1000, config['telemetry'].get('max_pages', 100))}
            for window in windows:
                result = export(project, window=window, budget=budget)
                results.append(result)
                if not result.get('coverage_complete'):
                    break
            telemetry = {'windows': results, 'database_only': all(r.get('database_only', True) for r in results),
                         'coverage_complete': len(results) == len(windows) and all(r.get('coverage_complete') for r in results)}
    except LearningBusy:
        telemetry = {'database_only': True, 'coverage_complete': False, 'reason': 'busy'}
    cache = prepare(project, run, months, windows=windows)
    artifact = {'run_id': run, 'project_id': config['project_id'], 'record_ids': ids,
                'record_digests': {r['id']: hashlib.sha256(json.dumps(r, sort_keys=True).encode()).hexdigest() for r in selected},
                'telemetry': telemetry, 'cache': cache,
                'analysis_required': {i: {'scope': 'project_requirement' if latest[i]['kind'] == 'requirement' else latest[i]['payload'].get('scope'),
                    'source_assessment': None, 'expected_vs_actual': None, 'causal_hypotheses': None,
                    'relevant_rules': None, 'measurable_goal': None, 'alternatives_and_sources': None,
                    'decision': None, 'verification': None} for i in ids}}
    artifact['source_digests'] = source_digests
    artifact['rule_snapshot'], artifact['analysis_dependencies'] = rule_snapshot(project)
    artifact['reflection'] = None
    write_json(state / 'runs' / run / 'analysis.json', artifact)
    return artifact


def finish(project, run):
    from learning_processing import lock
    from learning_run import load
    _, analysis = load(project, run)
    proposal_path = analysis.get('proposal')
    if not proposal_path:
        raise ValueError('Run lacks its exact linked proposal')
    state = Path(project).resolve() / '.agents/learning'
    path = Path(proposal_path).resolve(strict=True)
    if not path.is_relative_to(state / 'proposals'):
        raise ValueError('Proposal is outside this project store')
    proposal = json.loads(path.read_text(encoding='utf-8'))
    with lock(state, proposal['repo']):
        return finish_locked(project, run)


def finish_locked(project, run):
    state = Path(project).resolve() / '.agents/learning'
    # Validate path before reading any caller-controlled location.
    import re
    if not re.fullmatch(r'[a-zA-Z0-9_-]{1,80}', run):
        raise ValueError('Invalid run ID')
    folder = state / 'runs' / run
    analysis = json.loads((folder / 'analysis.json').read_text(encoding='utf-8'))
    config = read_config(project)
    if analysis['project_id'] != config['project_id']:
        raise ValueError('Wrong project analysis')
    from learning_run import validate_analysis, verify_binding
    validate_analysis(project, analysis)
    proposal_path = analysis.get('proposal')
    if not proposal_path:
        raise ValueError('Run lacks its exact linked proposal')
    proposal_path = Path(proposal_path).resolve(strict=True)
    if not proposal_path.is_relative_to(state.resolve() / 'proposals'):
        raise ValueError('Proposal is outside this project store')
    proposal = json.loads(proposal_path.read_text(encoding='utf-8'))
    verify_binding(proposal, state)
    if proposal['run_binding']['run_id'] != run:
        raise ValueError('Proposal belongs to another run')
    from learning_cycle import (
        hash_text,
        processing_receipt,
        skill_inventory,
        verify_dependencies,
        verify_evidence,
    )
    verify_dependencies(proposal)
    verify_evidence(proposal, state)
    inventory = skill_inventory(Path(proposal['repo']))
    receipt = processing_receipt(proposal['work_items'],
        {key: inventory[key] for key in proposal['processing_skills']}, project, Path(proposal['repo']))
    expected_records = {r['id']: r for r in receipt['records']}
    planned_decisions = {d['record_id']: d for d in proposal['decisions']}
    for original in proposal['processing']['records']:
        if planned_decisions[original['id']]['outcome'] != 'pending':
            expected_records[original['id']] = original
    reflection = analysis.get('reflection')
    if not isinstance(reflection, dict) or set(reflection) != {'checked', 'failed', 'limitations', 'next_improvement'} or any(not isinstance(v, str) or not v.strip() for v in reflection.values()):
        raise ValueError('Complete reflection before finishing the run')
    with closing(sqlite3.connect(state / 'experience.sqlite3')) as conn:
        conn.execute('BEGIN')
        latest = {r['id']: r for r in records(conn, config['project_id'])}
        decisions = []
        for identifier in analysis['record_ids']:
            if identifier not in latest or hashlib.sha256(json.dumps(latest[identifier], sort_keys=True).encode()).hexdigest() != analysis['record_digests'].get(identifier):
                raise ValueError('Selected record changed; reassess before completion')
            item = analysis['analysis_required'].get(identifier, {})
            required = {'scope', 'source_assessment', 'expected_vs_actual', 'causal_hypotheses', 'relevant_rules',
                        'measurable_goal', 'alternatives_and_sources', 'decision', 'verification'}
            if set(item) != required or any(value is None or value in ('', [], {}) for value in item.values()):
                raise ValueError('Complete evidence assessment and diagnosis for every selected record')
            expected = expected_records[identifier]
            row = conn.execute('SELECT outcome,details,proposal FROM learning_decisions WHERE project_id=? AND record_id=? AND repo=? AND record_digest=? AND skill_digest=? AND proposal=? ORDER BY sequence DESC LIMIT 1',
                (config['capture_project_id'], identifier, proposal['repo'], expected['digest'], expected['skill_digest'], str(proposal_path))).fetchone()
            if not row or row[0] not in {'applied', 'no_change', 'deferred'}:
                raise ValueError('Work lacks a durable per-record decision')
            planned = planned_decisions[identifier]['outcome']
            if row[0] != ('applied' if planned == 'pending' else planned):
                raise ValueError('Decision differs from the linked proposal')
            if row[0] == 'applied' and json.loads(row[1]).get('used') is not True:
                raise ValueError('Missing used receipt')
            if row[0] == 'applied':
                details = json.loads(row[1])
                if proposal['state'] != 'applied' or details.get('checks') != proposal.get('checks') or not (proposal.get('checks') or {}).get('structural_passed'):
                    raise ValueError('Applied proposal lacks matching checks')
                if not proposal.get('applied_hashes') or details.get('applied_hashes') != proposal['applied_hashes']:
                    raise ValueError('Applied rule versions are missing')
                for name, expected_hash in proposal['applied_hashes'].items():
                    target = (Path(proposal['repo']) / name).resolve()
                    if not target.is_relative_to(Path(proposal['repo'])) or hash_text(target.read_text(encoding='utf-8-sig')) != expected_hash:
                        raise ValueError('Installed rule changed after application')
            decisions.append({'record_id': identifier, 'outcome': row[0], 'proposal': row[2]})
    # Keep analysis, cited archive IDs and receipts; discard only the reconstructed cache.
    if not (folder / 'completion.json').exists():
        write_json(folder / 'completion.json', {'decisions': decisions, 'finished_at': datetime.now(UTC).isoformat(),
                   'reflection': reflection})
    snapshot = enqueue(project)
    sync = drain(project)
    return {'snapshot': snapshot, 'sync': sync, 'cleanup': cleanup(project, run)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('maintenance', 'begin', 'finish', 'snapshot', 'sync', 'archive', 'curation-queue', 'restore'))
    parser.add_argument('--project', required=True)
    parser.add_argument('--record', action='append', default=[])
    parser.add_argument('--run')
    parser.add_argument('--file')
    args = parser.parse_args()
    if args.command == 'maintenance':
        parser.error('Background maintenance is disabled; explicit workflow stages only.')
    if args.command == 'restore':
        from learning_exchange import restore
        print(json.dumps(restore(args.project, args.file)))
        return
    functions = {'maintenance': maintenance, 'snapshot': enqueue, 'sync': drain, 'archive': export, 'curation-queue': curate_queue}
    result = begin(args.project, args.record) if args.command == 'begin' else finish(args.project, args.run) if args.command == 'finish' else functions[args.command](args.project)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
