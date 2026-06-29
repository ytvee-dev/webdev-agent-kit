---
id: 'agents.common.state-ownership-rules'
title: 'State Ownership Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/state'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-architecture-planner/SKILL|Frontend Architecture Planner]]'
depends_on: []
---

# State Ownership Rules

Purpose: keep frontend state local, explicit, and aligned with existing project
ownership.

## Rules

- Keep UI state local by default.
- Promote state only when multiple surfaces need a shared owner.
- Do not store derived state unless the existing project convention requires
  it.
- Preserve existing stores, hooks, contexts, and server/client boundaries.
- Do not add state libraries without explicit approval.
- During refactors, preserve public state contracts unless behavior change is
  approved.

