---
id: 'agents.adapters.codex'
title: 'Codex Client Adapter'
doc_type: 'client-adapter'
layer: 'adapter'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/adapter'
    - 'client/codex'
parent:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
related:
    - '[[common/codex-model-routing-policy]]'
    - '[[templates/root-pointers/AGENTS.codex|Codex AGENTS Pointer Template]]'
depends_on:
    - '[[common/core/runtime-core-policy|Portable Runtime Core Policy]]'
---

# Codex Client Adapter

Map portable behavior to Codex without redefining workflow policy.

## Discovery And Instructions

Use `.agents/AGENTS.md` through the approved minimal root `AGENTS.md` pointer.
Skills live in `.agents/skills`; `agents/openai.yaml` is UI metadata, not a model
binding or capability proof. Preserve existing host instructions; create or
merge a pointer only with explicit approval.

## Tools And Configuration

Use the active tool registry or validated project facts as capability evidence.
Native tools can satisfy capabilities without MCP. Keep sandbox and approvals
separate; never bypass either. Report blocked checks after bounded fallback.

For approved GPT setup, onboarding uses its `references/codex-model-bootstrap.md`.
For task delegation with a local model-routing profile, load
`common/codex-model-routing-policy.md` before broad context. No config writes
during ordinary work, silent model upgrades, or changes to global defaults.

## Output

Use the portable output contract. Mention client details only when consequential.
