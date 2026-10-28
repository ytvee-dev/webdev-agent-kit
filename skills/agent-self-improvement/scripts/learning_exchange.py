"""Immutable per-project snapshots and retryable private-repository outbox."""
import base64
import hashlib
import json
import re
import sqlite3
import subprocess
import time
from contextlib import closing
from pathlib import Path

from learning_memory import gh, records, repository
from learning_processing import lock
from learning_project import read_config, write_json
from learning_telemetry import sanitize


def enqueue(project):
    project = Path(project).resolve()
    state = project / '.agents/learning'
    if not (state / 'project.json').exists():
        return {'status': 'unconfigured'}
    config = read_config(project)
    with lock(state, state / 'exchange'):
        with closing(sqlite3.connect((state / 'experience.sqlite3').as_uri() + '?mode=ro', uri=True)) as conn:
            conn.execute('BEGIN')
            memory = records(conn, config['project_id'])
            decisions = []
            if conn.execute("SELECT 1 FROM sqlite_master WHERE name='learning_decisions'").fetchone():
                conn.row_factory = sqlite3.Row
                for row in conn.execute('SELECT * FROM learning_decisions WHERE project_id=? ORDER BY sequence', (config['capture_project_id'],)):
                    value = dict(row)
                    value.pop('sequence')
                    value['project_id'] = config['project_id']
                    target = Path(value.pop('repo')).resolve()
                    value['target_scope'] = 'project' if target in (project, project / '.agents') else 'external_target'
                    value['target_root'] = '.agents' if target == project / '.agents' else '.' if target == project else None
                    # Historical external targets are audit only, never portable permission to apply.
                    value['proposal'] = Path(value['proposal']).name
                    value['details'] = json.loads(value['details'])
                    decisions.append(value)
            latest = {r['id']: r for r in memory}
            routing = {name: [] for name in ('project_requirements', 'project_lessons', 'kit_candidates')}
            for record in latest.values():
                route = ('project_requirements' if record['kind'] == 'requirement' else
                         'kit_candidates' if record['kind'] == 'lesson' and record['payload'].get('scope') == 'transfer_candidate' else
                         'project_lessons' if record['kind'] == 'lesson' else None)
                if route:
                    routing[route].append({'id': record['id'], 'revision': record['revision']})
            payload = {'schema_version': 1, 'project_id': config['project_id'], 'records': memory, 'routing': routing,
                       'processing_history': decisions, 'raw_events_included': False}
        # Remove host paths and secrets from exchange; local DB remains authoritative.
        encoded = json.dumps(sanitize(payload), sort_keys=True, ensure_ascii=False)
        encoded = encoded.replace(json.dumps(str(project))[1:-1], '<project>')
        content = encoded.encode('utf-8')
        digest = hashlib.sha256(content).hexdigest()
        snapshot = state / 'snapshots' / (digest + '.json')
        if not snapshot.exists():
            snapshot.write_bytes(content)
        paths = [snapshot] + sorted((state / 'archive').glob('*/*.json'))
        count = 0
        for path in paths:
            relative = path.relative_to(state).as_posix()
            key = hashlib.sha256(relative.encode()).hexdigest()
            if (state / 'outbox' / (key + '.sent')).exists():
                continue
            write_json(state / 'outbox' / (key + '.json'), {'path': relative,
                       'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
            count += 1
        return {'status': 'queued', 'snapshot': digest, 'pending': count}


def drain(project, api=gh, limit=100):
    if api is gh:
        return drain_batch(project, api, limit)
    state = Path(project).resolve() / '.agents/learning'
    config = read_config(project)
    if not config.get('auto_sync'):
        return {'status': 'disabled'}
    remote = repository(config['remote'])
    folder = config['remote_folder']
    if not re.fullmatch(r'[A-Za-z0-9_.-]+', folder) or folder in {'.', '..'}:
        raise ValueError('Invalid remote project folder')
    uploaded = 0
    stage = 'repository_metadata'
    create_error = None
    deadline = time.monotonic() + 90
    with lock(state, state / 'exchange'):
        try:
            if api('repos/' + remote).get('private') is not True:
                raise ValueError('Remote must be private')
            for entry in sorted((state / 'outbox').glob('*.json'))[:max(1, min(limit, 100))]:
                if time.monotonic() >= deadline:
                    break
                stage = 'read_local_artifact'
                job = json.loads(entry.read_text())
                relative = Path(job['path'])
                path = (state / relative).resolve(strict=True)
                if not path.is_relative_to(state.resolve()) or relative.parts[0] not in {'snapshots', 'archive'}:
                    raise ValueError('Outbox path outside approved artifacts')
                data = path.read_bytes()
                if hashlib.sha256(data).hexdigest() != job['sha256'] or len(data) > 8 * 1024 * 1024:
                    raise ValueError('Artifact changed or too large')
                route = 'repos/' + remote + '/contents/' + folder + '/' + relative.as_posix()
                # PUT is create-only: retry after a lost response verifies exact existing content.
                try:
                    stage = 'create_remote_artifact'
                    create_error = None
                    api(route, '--method', 'PUT', '--input', '-', input_data=json.dumps({
                        'message': 'Archive project learning evidence', 'content': base64.b64encode(data).decode()}))
                except ValueError as exc:
                    create_error = getattr(exc, 'code', type(exc).__name__)
                stage = 'verify_remote_artifact'
                existing = api(route)
                restored = base64.b64decode(existing.get('content', ''))
                if restored != data:
                    raise ValueError('Remote artifact conflict; no overwrite')
                stage = 'acknowledge_delivery'
                entry.rename(entry.with_suffix('.sent'))
                uploaded += 1
            remaining = len(list((state / 'outbox').glob('*.json')))
            result = {'status': 'pending_retry' if remaining else 'synced', 'uploaded': uploaded, 'remaining': remaining}
        except (ValueError, OSError, TimeoutError, subprocess.TimeoutExpired) as exc:
            result = {'status': 'pending_retry', 'uploaded': uploaded, 'stage': stage,
                      'reason': getattr(exc, 'code', 'remote_conflict' if str(exc) == 'Remote artifact conflict; no overwrite' else type(exc).__name__),
                      'remaining': len(list((state / 'outbox').glob('*.json'))),
                      'retry': 'explicit_request_only', 'create_error': create_error}
        write_json(state / 'sync-status.json', result)
        return result


def drain_batch(project, api=gh, limit=100):
    """Create one bounded immutable tree commit; verify reachable blob IDs before ack."""
    state = Path(project).resolve() / '.agents/learning'
    config = read_config(project)
    if not config.get('auto_sync'):
        return {'status': 'disabled'}
    remote, folder = repository(config['remote']), config['remote_folder']
    if not re.fullmatch(r'[A-Za-z0-9_.-]+', folder) or folder in {'.', '..'}:
        raise ValueError('Invalid remote project folder')
    route = 'repos/' + remote
    transport = api
    deadline = time.monotonic() + 90
    def api(*args, **kwargs):
        if time.monotonic() >= deadline:
            raise TimeoutError('Batch time budget exhausted')
        return transport(*args, **kwargs)
    stage, uploaded = 'repository_metadata', 0
    with lock(state, state / 'exchange'):
        try:
            meta = api(route)
            if meta.get('private') is not True:
                raise ValueError('Remote must be private')
            branch = meta['default_branch']
            def tree_at_head():
                head = api(route + '/git/ref/heads/' + branch)['object']['sha']
                commit = api(route + '/git/commits/' + head)
                tree = commit['tree']['sha']
                top = api(route + '/git/trees/' + tree)
                if top.get('truncated'):
                    raise ValueError('Incomplete repository tree')
                node = next((n for n in top['tree'] if n['path'] == folder), None)
                if node and node['type'] != 'tree':
                    raise ValueError('Remote project folder conflicts')
                content = api(route + '/git/trees/' + node['sha'] + '?recursive=1') if node else {'tree': []}
                if content.get('truncated'):
                    raise ValueError('Incomplete project tree')
                return head, tree, {n['path']: n['sha'] if n['type'] == 'blob' and n.get('mode') == '100644'
                                   else 'unsupported-mode:' + n['sha'] for n in content['tree']}
            stage = 'read_remote_tree'
            head, base_tree, existing = tree_at_head()
            jobs, additions, size = [], [], 0
            for entry in sorted((state / 'outbox').glob('*.json'))[:max(1, min(limit, 100))]:
                stage = 'read_local_artifact'
                job = json.loads(entry.read_text(encoding='utf-8'))
                relative = Path(job['path'])
                path = (state / relative).resolve(strict=True)
                if not path.is_relative_to(state) or relative.parts[0] not in {'snapshots', 'archive'}:
                    raise ValueError('Outbox path outside approved artifacts')
                data = path.read_bytes()
                if len(data) > 8 * 1024 * 1024 or hashlib.sha256(data).hexdigest() != job['sha256']:
                    raise ValueError('Artifact changed or too large')
                # Git blob IDs commit to both object type/length and exact bytes.
                blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                name = relative.as_posix()
                if name in existing and existing[name] != blob:
                    raise ValueError('Remote artifact conflict; no overwrite')
                if name not in existing:
                    addition = {'path': folder + '/' + name, 'mode': '100644', 'type': 'blob', 'content': data.decode('utf-8')}
                    cost = len(json.dumps(addition).encode())
                    if size + cost > 4 * 1024 * 1024 and jobs:
                        break
                    # A single permitted artifact may exceed the normal batch budget.
                    additions.append(addition)
                    size += cost
                jobs.append((entry, name, blob))
            if additions:
                stage = 'create_tree'
                tree = api(route + '/git/trees', '--method', 'POST', '--input', '-',
                           input_data=json.dumps({'base_tree': base_tree, 'tree': additions}))['sha']
                stage = 'create_commit'
                commit = api(route + '/git/commits', '--method', 'POST', '--input', '-', input_data=json.dumps({
                    'message': 'Archive project learning evidence', 'tree': tree, 'parents': [head]}))['sha']
                stage = 'advance_branch'
                api(route + '/git/refs/heads/' + branch, '--method', 'PATCH', '--input', '-',
                    input_data=json.dumps({'sha': commit, 'force': False}))
                stage = 'verify_remote_tree'
                _, _, existing = tree_at_head()
            stage = 'acknowledge_delivery'
            for entry, name, blob in jobs:
                if existing.get(name) != blob:
                    raise ValueError('Remote artifact readback differs')
                entry.rename(entry.with_suffix('.sent'))
                uploaded += 1
            remaining = len(list((state / 'outbox').glob('*.json')))
            result = {'status': 'pending_retry' if remaining else 'synced', 'uploaded': uploaded,
                      'remaining': remaining, 'batch_bytes': size, 'delivery': 'verified_git_blobs',
                      'retry': 'explicit_request_only'}
        except (ValueError, OSError, KeyError, TimeoutError, subprocess.TimeoutExpired) as exc:
            result = {'status': 'pending_retry', 'uploaded': uploaded, 'stage': stage,
                      'reason': getattr(exc, 'code', 'remote_conflict' if str(exc) == 'Remote artifact conflict; no overwrite' else type(exc).__name__),
                      'remaining': len(list((state / 'outbox').glob('*.json'))), 'retry': 'explicit_request_only'}
        write_json(state / 'sync-status.json', result)
        return result


def notify(project):
    """Local dirty marker only; explicit sync or requested completion does network I/O."""
    state = Path(project).resolve() / '.agents/learning'
    if (state / 'project.json').is_file():
        write_json(state / 'queue/sync.json', {'requested': True})


def restore(project, snapshot):
    """Explicit same-project restore. Import audit history, never execute remote patches."""
    from learning_memory import open_store, save_records
    from learning_processing import connect
    project = Path(project).resolve()
    state = project / '.agents/learning'
    config = read_config(project)
    path = Path(snapshot).resolve(strict=True)
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != path.stem:
        raise ValueError('Snapshot filename/content hash mismatch')
    value = json.loads(content)
    if value.get('schema_version') != 1 or value.get('project_id') != config['project_id'] or value.get('raw_events_included') is not False:
        raise ValueError('Wrong project or snapshot format')
    with lock(state, state / 'exchange'):
        with closing(open_store(state)) as conn:
            inserted = save_records(conn, config['project_id'], value['records'], enforce_quality=False)
        with closing(connect(state)) as conn, conn:
            conn.execute('CREATE TABLE IF NOT EXISTS restored_processing (digest TEXT PRIMARY KEY, snapshot TEXT NOT NULL, receipt TEXT NOT NULL)')
            for receipt in value['processing_history']:
                # Keep historical used markers as audit evidence. Do not synthesize local apply:
                # exact rule/evidence correspondence must be established before adopting a receipt.
                encoded = json.dumps(receipt, sort_keys=True)
                conn.execute('INSERT OR IGNORE INTO restored_processing VALUES (?,?,?)',
                             (hashlib.sha256(encoded.encode()).hexdigest(), path.stem, encoded))
        return {'inserted': inserted, 'history_restored_for_review': len(value['processing_history']),
                'patches_applied': 0, 'local_usage_automatically_adopted': False}
