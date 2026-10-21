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

# Optional client integrations (preview)

These examples are **not activated on installation**. Install only after an explicit project opt-in with `python <absolute-path-to-learning.py> on --project <absolute-project-root>`. Review existing client config and preserve its existing hooks.

## Codex

Codex supports `UserPromptSubmit`, `PostToolUse`, and `SessionEnd` in trusted `hooks.json`. Configure the following alongside existing hooks, resolving the Python bridge to an **absolute path** under the installed Kit. Change the placeholder before applying:

```json
{
  "hooks": {
    "UserPromptSubmit": [{ "hooks": [{ "type": "command", "command": "python /ABSOLUTE/PATH/TO/assets/integrations/hook_bridge.py --client codex", "async": true, "timeout": 5 }] }],
    "PostToolUse": [{ "hooks": [{ "type": "command", "command": "python /ABSOLUTE/PATH/TO/assets/integrations/hook_bridge.py --client codex", "async": true, "timeout": 5 }] }]
  }
}
```

Inspect and trust the hooks using the client UI. The bridge stores prompt text and tool names, **not complete assistant replies, tool inputs, attachments or transcript copies**. Transcript path is not followed automatically.

## Claude Code

Use supported native `UserPromptSubmit` and `PostToolUse` command hooks, pointing to the same absolute `hook_bridge.py`, with `--client claude-code`. Merge with existing hooks rather than replacing settings. Treat as an opt-in preview until the exact payload is observed in a real session.

## OpenCode

Copy `opencode/experience-recorder.js` into `.opencode/plugins/experience-recorder.js` and set `AGENT_LEARNING_SCRIPT` to the absolute path of `scripts/learning.py`. The plugin uses `session.idle` and the documented SDK `session.messages` method to capture text parts, tool-name metadata and file-part metadata. **Files are not automatically copied**. Set `learning on` for the project; off immediately prevents new capture at CLI level. This is a preview and needs a real OpenCode compatibility test.

## File bytes

Where a client exposes only a link, path or file-part metadata, the attachment stays metadata-only. To save a user-supplied file, explicitly run:

```sh
python <path-to-learning.py> attach --project <root> --client opencode --session <source-session-id> --file <approved-path>
```

## Scheduling

The `run` command performs deterministic offline triage of explicitly tagged user corrections. It does not run a model, edit skills, or publish code. It is safe to schedule in a trusted local OS scheduler for analysis only; do not describe this as automated prompt optimization.
