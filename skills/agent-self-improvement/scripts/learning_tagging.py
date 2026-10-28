"""Configure the installed tracing plugin's project-local tags and validate isolation."""
import argparse
import base64
import json
import os
import subprocess
import time
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

from learning_project import read_config, write_json
from learning_state import state_root
from learning_telemetry import assess, request_page


def effective_connection(project, global_config=None):
    global_path = Path(global_config) if global_config else Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')) / 'langfuse.json'
    local_path = Path(project).resolve() / '.codex/langfuse.json'
    effective = {}
    for path in (global_path, local_path):
        if path.is_file():
            effective.update(json.loads(path.read_text(encoding='utf-8')))
    conflicts = [name for name in ('TRACE_TO_LANGFUSE', 'LANGFUSE_CODEX_ENABLED', 'LANGFUSE_CODEX_TAGS') if os.environ.get(name)]
    for name in ('public_key', 'secret_key', 'base_url'):
        for prefix in ('LANGFUSE_', 'LANGFUSE_CODEX_'):
            if os.environ.get(prefix + name.upper()):
                effective[name] = os.environ[prefix + name.upper()]
    return effective, conflicts


def connection_status(project, global_config=None):
    effective, conflicts = effective_connection(project, global_config)
    public, secret = effective.get('public_key', ''), effective.get('secret_key', '')
    placeholders = ('...', 'PLACEHOLDER', 'YOUR_', 'Р’РђРЁ_', '<', '>')
    ready = (isinstance(public, str) and isinstance(secret, str)
             and public.startswith('pk-lf-') and secret.startswith('sk-lf-')
             and len(public) > 12 and len(secret) > 12
             and not any(token in (public + secret).upper() for token in placeholders)
             and str(effective.get('base_url', '')).startswith('https://'))
    return {'credentials_present': ready, 'authentication': 'unverified',
            'enabled_in_files': effective.get('enabled') is True,
            'environment_conflicts': conflicts, 'status': 'pending_readback'}


def verify_credentials(project, effective):
    config = read_config(project)
    now = datetime.now(UTC)
    authorization = 'Basic ' + base64.b64encode((effective['public_key'] + ':' + effective['secret_key']).encode()).decode()
    spec = dict(config['telemetry'], base_url=effective['base_url'],
                required_tags=['project-id:' + config['project_id']], fields='core', page_size=1)
    request_page(spec, (now - timedelta(minutes=1)).isoformat(), now.isoformat(), authorization=authorization)


def set_connection(project, enabled, approve=False, global_config=None, authenticate=verify_credentials):
    if not approve:
        raise ValueError('Explicit connection or disable consent required (--approve)')
    project = Path(project).resolve()
    status = connection_status(project, global_config)
    if status['environment_conflicts']:
        raise ValueError('Resolve tracing environment overrides before changing project enablement')
    if enabled and not status['credentials_present']:
        raise ValueError('Missing or placeholder credentials; tracing remains unchanged')
    if enabled:
        effective, _ = effective_connection(project, global_config)
        try:
            authenticate(project, effective)
        except (ValueError, OSError, RuntimeError):
            set_connection(project, False, approve=True, global_config=global_config)
            config = read_config(project)
            config['telemetry']['connection_choice'] = 'pending_credentials'
            write_json(state_root(project) / 'project.json', config)
            raise ValueError('Authentication unavailable or failed; project tracing disabled') from None
        configure(project)
    path = project / '.codex/langfuse.json'
    existing = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    write_json(path, dict(existing, enabled=enabled))
    config = read_config(project)
    config['telemetry']['enabled'] = enabled
    if enabled:
        effective, _ = effective_connection(project, global_config)
        config['telemetry']['base_url'] = effective['base_url']
    config['telemetry']['connection_choice'] = 'connected' if enabled else 'declined'
    config['telemetry']['tag_validation'] = 'pending_readback' if enabled else 'disabled'
    write_json(state_root(project) / 'project.json', config)
    return {'status': 'configured_pending_readback' if enabled else 'disabled',
            'project_id': config['project_id']}


def configure(project):
    project = Path(project).resolve()
    config = read_config(project)
    path = project / '.codex/langfuse.json'
    old = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    tags = old.get('tags', [])
    if not isinstance(tags, list):
        raise ValueError('Existing plugin tags must be a list')
    identity = 'project-id:' + config['project_id']
    if any(t.startswith('project-id:') and t != identity for t in tags):
        raise ValueError('Different project ID in tracing configuration; inspect copied project identity')
    # A friendly tag is retained for historical archives; stable identity is canonical for new logs.
    aliases = [t for t in tags if t.startswith('project:')]
    if len(aliases) > 1:
        raise ValueError('Ambiguous project tags')
    friendly = aliases[0] if aliases else 'project:' + project.name
    expected = list(dict.fromkeys(tags + ['webdev-agent-kit', friendly, identity]))
    override = os.environ.get('LANGFUSE_CODEX_TAGS')
    if override:
        raise ValueError('LANGFUSE_CODEX_TAGS overrides project-local tags; resolve before setup')
    backup = state_root(project) / 'tracing-config.before.json'
    if not backup.exists():
        write_json(backup, {'existed': path.exists(), 'config': old})
    write_json(path, dict(old, tags=expected))
    config['telemetry'].update(required_tags=['webdev-agent-kit', friendly],
                               stable_tag=identity, historical_tag=friendly,
                               tag_validation='configured_pending_readback')
    write_json(state_root(project) / 'project.json', config)
    if json.loads(path.read_text(encoding='utf-8'))['tags'] != expected:
        raise ValueError('Tag configuration readback failed')
    return {'status': 'configured_pending_readback', 'tags': expected,
            'source': 'project-local configuration of existing Codex tracing Stop hook'}


def validate(project, fetch=request_page):
    project = Path(project).resolve()
    config = read_config(project)
    spec = config['telemetry']
    now = datetime.now(UTC)
    # Strict stable-ID lookup. Friendly tags alone never certify the new installation.
    strict = dict(spec, required_tags=['webdev-agent-kit', 'project-id:' + config['project_id']],
                  fields='core,basic,trace_context')
    probe_file = state_root(project) / 'tag-probe.json'
    probe = json.loads(probe_file.read_text(encoding='utf-8')) if probe_file.exists() else None
    cursor, seen, good, rejected = None, set(), [], 0
    exhausted = False
    deadline = time.monotonic() + 120
    try:
        for page in range(20):
            if time.monotonic() >= deadline:
                raise RuntimeError('time_budget_exhausted')
            response = fetch(strict, (now - timedelta(days=1)).isoformat(), now.isoformat(), cursor)
            rows = response.get('data', [])
            for row in rows:
                if assess(row, dict(config, telemetry=strict))['project_match']:
                    good.append(row)
                else:
                    rejected += 1
            cursor = response.get('meta', {}).get('cursor')
            if not cursor:
                exhausted = True
                break
            if cursor in seen:
                raise RuntimeError('repeated_cursor')
            seen.add(cursor)
            if good and (not probe or any(r.get('sessionId') == probe['session_id'] for r in good)):
                break
        probe_found = bool(probe and any(r.get('sessionId') == probe['session_id'] for r in good))
        result = {'status': 'mismatch' if rejected else 'verified' if probe_found else 'pending_readback' if good else 'not_found' if exhausted else 'pending',
                  'matching_observations': len(good), 'rejected': rejected,
                  'probe_status': 'found' if probe_found else 'not_found' if exhausted else 'pending',
                  'pages_checked': page + 1, 'range_exhausted': exhausted,
                  'checked_at': now.isoformat(), 'trace_ids': sorted({r['traceId'] for r in good if r.get('traceId')})[:5]}
    except (RuntimeError, OSError) as exc:
        result = {'status': 'unavailable', 'database_only': True,
                  'reason': str(exc) if isinstance(exc, RuntimeError) else type(exc).__name__}
    write_json(state_root(project) / 'tag-validation.json', result)
    return result


def probe(project, hook):
    """Exercise the existing uploader with harmless synthetic events, not a model run."""
    project = Path(project).resolve()
    hook = Path(hook).resolve(strict=True)
    config = json.loads((project / '.codex/langfuse.json').read_text(encoding='utf-8'))
    if config.get('enabled') is False:
        raise ValueError('Tracing is explicitly disabled')
    session, turn = str(uuid.uuid4()), str(uuid.uuid4())
    now = datetime.now(UTC)
    folder = state_root(project) / 'runs/tag-validation'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (session + '.jsonl')
    events = [('session_meta', {'id': session, 'cwd': str(project), 'source': 'tag-validation'}),
              ('event_msg', {'type': 'task_started', 'turn_id': turn}),
              ('event_msg', {'type': 'user_message', 'message': 'Synthetic project-tag validation. Exclude from instruction learning.'}),
              ('response_item', {'type': 'function_call', 'call_id': 'probe', 'name': 'tag_validation', 'arguments': '{}'}),
              ('response_item', {'type': 'function_call_output', 'call_id': 'probe', 'output': 'Synthetic fixture only; no model or task was executed.'}),
              ('event_msg', {'type': 'agent_message', 'message': 'Synthetic tracing check.'}),
              ('event_msg', {'type': 'task_complete', 'turn_id': turn})]
    path.write_text(''.join(json.dumps({'type': kind, 'timestamp': (now + timedelta(milliseconds=i)).isoformat(), 'payload': payload}) + '\n' for i, (kind, payload) in enumerate(events)), encoding='utf-8')
    env = dict(os.environ, LANGFUSE_CODEX_FAIL_ON_ERROR='true',
               LANGFUSE_CODEX_TAGS=json.dumps(config['tags'] + ['learning:validation']))
    result = subprocess.run(['node', str(hook)], cwd=project, input=json.dumps({'transcript_path': str(path), 'turn_id': turn}),
                            text=True, capture_output=True, timeout=45, env=env)
    report = {'session_id': session, 'turn_id': turn, 'status': 'sent_pending_readback' if result.returncode == 0 else 'hook_failed',
              'synthetic': True, 'model_called': False, 'hook': str(hook)}
    write_json(state_root(project) / 'tag-probe.json', report)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('configure', 'validate', 'probe', 'status', 'enable', 'disable'))
    parser.add_argument('--project', required=True)
    parser.add_argument('--hook')
    parser.add_argument('--approve', action='store_true')
    parser.add_argument("--state", type=Path)
    args = parser.parse_args()
    if args.command in {'enable', 'disable'}:
        result = set_connection(args.project, args.command == 'enable', args.approve)
    elif args.command == 'status':
        result = connection_status(args.project)
    else:
        result = probe(args.project, args.hook) if args.command == 'probe' else (configure if args.command == 'configure' else validate)(args.project)
    print(json.dumps(result))
