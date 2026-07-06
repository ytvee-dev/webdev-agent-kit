---
id: 'agents.common.refactor-safety-rules'
title: 'Refactor Safety Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/refactor'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-refactor-surgeon/SKILL|Frontend Refactor Surgeon]]'
depends_on: []
---

# Refactor Safety Rules

Purpose: preserve frontend behavior while improving structure.

## Rules

- Define the behavior boundary before editing.
- Preserve public API, rendered output, route behavior, state ownership, and
  accessibility unless the user approved a behavior change.
- Make mechanical changes in small steps.
- Do not combine refactor work with new features unless explicitly requested.
- Avoid broad rewrites when targeted extraction or simplification is enough.
- Run the same relevant verification before final reporting.
