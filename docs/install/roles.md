---
id: 'agents.docs.install.roles'
title: 'Select Frontend And Designer Roles'
doc_type: 'installation-guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'installation'
    - 'agents/roles'
parent:
    - '[[docs/install/README]]'
related:
    - '[[common/webdev-role-selection]]'
    - '[[docs/install/gpt-model-routing]]'
    - '[[docs/install/claude-agents]]'
depends_on: []
---

# Select Frontend And Designer Roles

Conversational roles define the focus of the current task. They do not select a
model, create a native subagent, change client settings or authorize design writes.
The same selection instructions apply to Codex, Claude Code and Cursor.

Use the exact page with an explicit request:

```text
Load https://github.com/ytvee-dev/webdev-agent-kit/wiki/Frontend-Meta-instructions
and apply the frontend role in this conversation.
```

```text
Load https://github.com/ytvee-dev/webdev-agent-kit/wiki/Designer-Meta-instructions
and apply the designer role in this conversation.
```

Once the Kit instructions are loaded, you can shorten those requests to
`WebDev role: frontend` or `WebDev role: designer`. `developer` also selects
frontend. These are conversational prompts, not guaranteed slash commands or
native client UI controls. Earlier installations may need the full prompt.

Reading or reviewing a wiki page does not switch roles. A selected role persists
for the conversation while preserving the task and decisions. If the page is
unavailable, the agent reports whether it has a verified cached copy; without
one, the current role remains active. A role-only request performs no task edits.

The wiki describes the department's scope. Available tools, installed skills
and the user's task determine what can actually execute. Design-system mapping
and pilot drafts in this release need explicit field-testing scope and do not
promise Figma/code synchronization or completed implementation.

## Models And Activation

Use [Codex model routing](gpt-model-routing.md) or
[Claude native roles](claude-agents.md) to configure subagents. Codex 1.1.0
introduced role activation during full adaptation. Release checks cover the
clients actually tested, not every installation. Project trust
or a managed-policy denial must be resolved by its owner. After setup, run a small
read-only task with the affected role. A configuration file alone is not proof
that the role works.

When reporting issue #71, separate conversational selection, native discovery,
effective model/effort, permissions and actual task output. This release does
not claim to have exercised the original reported project or restored its trust.
