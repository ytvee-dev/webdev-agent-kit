---
id: 'agents.skills.agent-self-improvement.assets.integrations'
title: 'Client Integration Examples'
doc_type: 'skill-reference'
layer: 'skill'
status: 'draft'
publishable: true
local_only: false
skill: 'agent-self-improvement'
tags:
    - 'agents/learning'
parent:
    - '[[skills/agent-self-improvement/SKILL|Agent Self Improvement]]'
related: []
depends_on: []
---

# Local client integrations and full learning cycle

These integrations are **not activated on installation**. Install only after an explicit project opt-in with `python <absolute-path-to-learning.py> on --project <absolute-project-root>`. Review existing client config and preserve its existing hooks.

## Codex

Codex supports `UserPromptSubmit`, `PostToolUse`, and `Stop` in trusted `hooks.json`. Configure the following alongside existing hooks, resolving the Python bridge to an **absolute path** under the installed Kit. Change the placeholder before applying:

```json
{
  "hooks": {
    "UserPromptSubmit": [{ "hooks": [{ "type": "command", "statusMessage": "Record user prompt", "command": "python /ABSOLUTE/PATH/TO/assets/integrations/hook_bridge.py --client codex", "async": true, "timeout": 5 }] }],
    "PostToolUse": [{ "hooks": [{ "type": "command", "statusMessage": "Record tool result", "command": "python /ABSOLUTE/PATH/TO/assets/integrations/hook_bridge.py --client codex", "async": true, "timeout": 5 }] }]
  }
}
```

Prefer `scripts/install_hooks.py --project ROOT` to preview and add `--approve`
only for an authorized capture setup. It supplies stable event-specific
`statusMessage` labels, including `Record assistant response` for Stop.
Known older prefixed defaults and corrupted question-mark labels are repaired.
Other custom labels and handler/group settings are preserved; identical
reinstallation performs no file write. Agents need not invent names during
adaptation. Localize labels only when requested, preserving their event meaning.
Changed definitions may require native trust review again; never edit trust hashes.
See https://learn.chatgpt.com/docs/hooks#config-shape and
https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks.

Inspect and trust the hooks using the client UI. The bridge records exposed user prompts, assistant Stop message content and tool response excerpts, **not a complete authenticated transcript or attachment bytes**. Transcript path is not followed automatically.

## Claude Code

Use supported native `UserPromptSubmit` and `PostToolUse` command hooks, pointing to the same absolute `hook_bridge.py`, with `--client claude-code`. Merge with existing hooks rather than replacing settings. Treat as an opt-in preview until the exact payload is observed in a real session.

## OpenCode

Copy `opencode/experience-recorder.js` into `.opencode/plugins/experience-recorder.js` and set `AGENT_LEARNING_SCRIPT` to the absolute path of `scripts/learning.py`. The plugin uses `session.idle` and the documented SDK `session.messages` method to capture text parts, tool-name metadata and file-part metadata. **Inline base64 `data:` file parts are copied with size limits; remote file references remain metadata-only.** Enable collection with `learning.py on --project <root>`; off immediately prevents new capture at CLI level. This is a preview and needs a real OpenCode compatibility test.

## File bytes

Where a client exposes only a link, path or file-part metadata, the attachment stays metadata-only. To save a user-supplied file, explicitly run:

```sh
python <path-to-learning.py> attach --project <root> --client opencode --session <source-session-id> --file <approved-path>
```

## Scheduling

The `learning.py run` command performs deterministic triage. For explicitly requested proposals, use `learning_cycle.py propose`, followed by `check`. Never schedule these commands.

## Windows Codex: install without replacing existing hooks

From PowerShell in the **source Kit checkout or installed package**, adjust paths:

```powershell
$skill = "C:\path\to\webdev-agent-kit\skills\agent-self-improvement"
$project = "C:\path\to\your-project"
python "$skill\scripts\learning.py" on --project "$project"
python "$skill\scripts\install_hooks.py" --project "$project"
# Inspect the preview, then explicitly approve:
python "$skill\scripts\install_hooks.py" --project "$project" --approve
```

The installer merges into `<project>\.codex\hooks.json`, preserves unrelated handlers, makes a backup, and adds the native `commandWindows` override. Restart Codex and review/trust changes using `/hooks`. Opt-out with `learning.py off --project ...`; remove hooks with `install_hooks.py --remove --approve`. Hooks do **not** give access to a complete or stable raw transcript; they record exposed user prompts, assistant Stop messages, and tool response excerpts. Use manual `attach` for screenshots whose bytes are unavailable.

## OpenCode opt-in

Copy `opencode/experience-recorder.js` to `<project>\.opencode\plugins\experience-recorder.js`. Set `AGENT_LEARNING_SCRIPT` to the absolute installed `learning.py` path; optional `AGENT_LEARNING_PYTHON` points to your Python interpreter. Enable per-project recording with `learning.py on`. Restart OpenCode. `session.idle` imports message text, observed skill-tool calls and file metadata. When the SDK returns an inline base64 data URL, its bytes can be stored automatically with limits. Remote URLs and arbitrary local paths are never fetched.

## Run complete local cycle

For this project-local workflow, use the project root as `--repo` and the reviewed run returned by `begin`. Source-Kit transfer is separate:

```powershell
$project = "C:\path\to\your-project"
$skill = "$project\.agents\skills\agent-self-improvement"
$repo = $project
python "$skill\scripts\learning_cycle.py" propose --run "<reviewed-run-id>" --project "$project" --repo "$repo" --engine codex
# Or: --engine opencode
```

The command uses your already-authorized CLI/model, processes the recent permitted experiences, selects up to six relevant skills (preferring observed invocations), generates a restricted proposal and runs structural validation in a disposable directory. For a specific target, add `--skill frontend-bugfix-debugger` (repeatable). It never loads every skill into one prompt. If accepted, read the saved `proposal.json` and `.diff`, then apply explicitly:

```powershell
python "$skill\scripts\learning_cycle.py" apply --repo "$repo" --proposal "C:\path\to\proposal.json" --approve
```

Before applying, supply independent held-out cases for the affected skill. The benchmark compares **baseline vs. candidate** under the same configured model and records per-case assertions:

```powershell
python "$skill\scripts\learning_benchmark.py" --repo "$repo" --proposal "C:\path\to\proposal.json" --cases "C:\path\to\heldout-cases.json" --engine codex
# Or: --engine opencode
```

Each case specifies an id, changed skill path, independent task prompt, and required/forbidden phrases:

```json
{
  "cases": [
    {
      "id": "correctness-1",
      "skill": "skills/frontend-bugfix-debugger/SKILL.md",
      "task": "A user reports the button no longer saves. Describe what you would do.",
      "required": ["reproduce", "verify"],
      "forbidden": ["skip verification"]
    }
  ]
}
```

Cases must be defined independently of the training examples. These lexical assertions are only a *minimum regression screen*, not proof of task success. For live coding quality, also run the Kit's existing full-agent behavior fixtures and review traces. A **synthetic replay cannot unlock live benchmark approval**. To apply without a live benchmark, the user must acknowledge the evaluation gap explicitly:

```powershell
python "$skill\scripts\learning_cycle.py" apply --repo "$repo" --proposal "C:\path\to\proposal.json" --approve --accept-unevaluated
```

The bypass never authorizes unattended execution.

## Explicit invocation only

Do not create Windows tasks, systemd timers or background workers. Legacy `auto`
and `maintenance` commands reject execution. Use `learning_schedule.py status`
or `remove --project <root>` to inspect/remove an old project task. Local capture
does not authorize learning or network maintenance.

## One-command local acceptance on Windows

From PowerShell after installing Python, without modifying live agents:

```powershell
& "$skill\scripts\smoke_windows.ps1" -Project $project -Repo $repo
# Only after explicit opt-in and reviewing stored experience:
& "$skill\scripts\smoke_windows.ps1" -Project $project -Repo $repo -Engine codex -RunLive -RunId "<reviewed-run-id>"
```

The first command uses synthetic test data and reports collection state. The second uses the selected installed Codex/OpenCode model to prepare a **review-only** proposal and may send your approved local evidence to its provider. Neither command applies changes.

## Offline acceptance without model costs

```powershell
python -m unittest discover -s "$skill\scripts" -p "test_*.py" -v
```

Tests use synthetic conversations and offline proposal fixtures. A separate **real** client smoke test remains necessary to verify Codex/Windows and OpenCode event payloads and the actual model authentication flow.
