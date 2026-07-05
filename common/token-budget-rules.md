---
id: 'agents.common.token-budget-rules'
title: 'Token Budget Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/context-budget'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/planning-rules|Planning Rules]]'
    - '[[common/token-economy-rules|Token Economy Rules]]'
depends_on: []
---

# Token Budget Rules

Purpose: spend context on correctness instead of broad, repetitive reading.

## Rules

- Read repository policy and selected skill instructions before optimizing for
  token usage.
- Use path indexes and overlays before broad searches when they exist.
- Prefer targeted reads, nearby patterns, and precise `rg` queries.
- Stop reading when enough evidence exists to make a safe change.
- Do not read `README.md` for runtime routing, validation, source inventory, or
  fallback context.
- Compress final output, not task understanding.

## Escalation

Increase context budget only when targeted inspection reveals unclear ownership,
cross-module behavior, architecture risk, or conflicting evidence.
