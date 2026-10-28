"""Inspect or remove a legacy project task. Scheduling is no longer supported."""
import argparse
import json
import os
import subprocess
from pathlib import Path

from learning_memory import identifier
from learning_project import read_config, write_json
from learning_state import state_root


def install(project):
    raise ValueError('Scheduled learning is disabled. Use status or remove; learning requires an explicit user request.')


def inspect(project):
    project = Path(project).resolve()
    name = 'WebDev-Learning-' + identifier(read_config(project)['project_id'])
    if os.name != 'nt':
        return {'status': 'unsupported_scheduler', 'task': name}
    script = ("$ErrorActionPreference='Stop'; $t = @(Get-ScheduledTask | Where-Object { $_.TaskName -eq '" + name + "' }); "
              "if ($t.Count -gt 1) { throw 'Ambiguous task' }; "
              "if ($t.Count -eq 0) { '{\"present\":false}' } else { "
              "@{present=$true; actions=@($t[0].Actions | Select-Object Execute,Arguments)} | ConvertTo-Json -Depth 4 }")
    result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', script],
                            capture_output=True, text=True, timeout=30, check=True,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    value = json.loads(result.stdout)
    if value['present']:
        expected = str(Path(__file__).with_name('learning_workflow.py').resolve())
        actions = value['actions']
        if len(actions) != 1 or expected not in (actions[0].get('Arguments') or '') or str(project) not in (actions[0].get('Arguments') or ''):
            raise ValueError('Task ownership differs; refusing removal')
    return {'status': 'installed' if value['present'] else 'absent', 'task': name}


def remove(project):
    result = inspect(project)
    if result['status'] == 'unsupported_scheduler':
        return result
    if result['status'] == 'installed':
        name = result['task']
        script = ("$ErrorActionPreference='Stop'; Stop-ScheduledTask -TaskName '" + name +
                  "'; Unregister-ScheduledTask -TaskName '" + name + "' -Confirm:$false")
        subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', script],
                       capture_output=True, text=True, timeout=30, check=True,
                       creationflags=subprocess.CREATE_NO_WINDOW)
        result = inspect(project)
        if result['status'] != 'absent':
            raise ValueError('Task removal not verified')
    outcome = dict(result, status='disabled', scheduling_allowed=False)
    write_json(state_root(project) / 'scheduler.json', outcome)
    return outcome


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', nargs='?', default='install', choices=('status', 'remove', 'install'))
    parser.add_argument('--project', required=True)
    parser.add_argument("--state", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps({'status': inspect, 'remove': remove, 'install': install}[args.command](args.project)))
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        parser.exit(2, str(exc) + '\n')


if __name__ == '__main__':
    main()
