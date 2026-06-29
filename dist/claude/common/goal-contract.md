---
id: 'agents.common.goal-contract'
title: 'Goal Contract'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/goal-contract'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/goal-planner/SKILL|Goal Planner]]'
    - '[[templates/goal-contract|Goal Contract Template]]'
depends_on: []
---

# Goal Contract

Purpose: define what the user is asking for before a standard or deep frontend
workflow starts implementation.

## Required Fields

- `User Goal`: the desired outcome in user or product terms.
- `Scope`: files, routes, screens, or workflows included.
- `Out Of Scope`: work the agent must not perform.
- `Constraints`: approvals, stack boundaries, no-production rules, and
  project-specific limits.
- `Done When`: observable acceptance criteria.
- `Workflow Level`: `Standard Workflow` or `Deep Workflow`.
- `Next Skill Or Step`: the handoff target.

## Rules

- Do not create a durable goal contract for lightweight work.
- Do not hide unresolved product questions inside implementation assumptions.
- Keep constraints specific to the task; avoid generic filler.
- If a durable file is needed, write local-only state under `project/**`.
- Reuse `templates/goal-contract.md` for durable contracts.

