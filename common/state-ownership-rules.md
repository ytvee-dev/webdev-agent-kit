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
    - '[[common/target-stack-policy|Target Stack Policy]]'
depends_on: []
---

# State Ownership Rules

Purpose: keep React local state, Redux state, and TanStack remote state ownership explicit.

## Rules

- Keep local UI state inside React components or local hooks by default.
- Promote state only when multiple surfaces need a shared owner.
- Use Redux only for storing and mutating application objects according to existing project slices.
- Do not put server communication, data processing, domain workflows, or use-case layers in Redux.
- Do not duplicate TanStack-owned remote data into Redux unless the existing project convention requires it.
- Do not store derived state unless the existing project convention requires it.
- Do not add state libraries without explicit approval.
- During refactors, preserve public state contracts unless behavior change is approved.
