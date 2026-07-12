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

## Contract Fields

- `Goal ID`: stable `G-###` identifier for a durable goal. Compact response-only
  goals may omit it.
- `User Goal`: the desired outcome in user or product terms.
- `Scope`: files, routes, screens, or workflows included.
- `Out Of Scope`: work the agent must not perform.
- `Constraints`: approvals, stack boundaries, no-production rules, and
  project-specific limits.
- `Clarifications`: optional accepted decisions that resolved material
  ambiguity during goal definition.
- `Done When`: observable acceptance criteria identified as `AC-###` for a
  durable goal.
- `Workflow Level`: `Standard Workflow` or `Deep Workflow`.
- `Next Skill Or Step`: the handoff target.

## Identifier Contract

- Use zero-padded, stable identifiers: `G-001`, `AC-001`, `AC-002`.
- Assign criterion identifiers only to observable outcomes, not implementation
  activity.
- Keep existing identifiers stable after execution begins. Do not renumber or
  reuse an identifier when criteria are reordered, removed, or superseded.
- Mark an obsolete criterion as `superseded` and link its replacement instead
  of silently deleting its history from a durable goal.
- Response-only standard goals may omit identifiers when no plan, resume state,
  or cross-slice traceability is needed.

## Rules

- Do not create a durable goal contract for lightweight work.
- Do not hide unresolved product questions inside implementation assumptions.
- Keep constraints specific to the task; avoid generic filler.
- If a durable file is needed, write local-only state under `project/**`.
- Reuse `templates/goal-contract.md` for durable contracts.
- Do not require a durable goal, identifiers, or traceability ceremony for
  `Fast Lookup` or `Lightweight Workflow` tasks.

## Clarification Gate

Use clarification only for `Standard Workflow` or `Deep Workflow` when an
unresolved choice would materially change scope, user behavior, architecture,
security, ownership, or verification.

1. Use the current request, confirmed decisions, host instructions, and verified
   project facts before asking a question.
2. Rank unresolved choices by impact and uncertainty.
3. Ask exactly one question at a time and no more than three questions in one
   goal-definition pass.
4. Prefer a short set of mutually exclusive choices or a constrained short
   answer. Recommend an option only when evidence supports the recommendation.
5. Stop when material ambiguity is resolved, the user asks to proceed, or the
   three-question limit is reached.
6. Apply each accepted answer immediately to Scope, Out Of Scope, Constraints,
   or Done When. Keep only a compact decision record under Clarifications when
   the goal is durable.

If the question limit is reached while a material choice still blocks correct
planning, record that choice as an explicit blocker instead of silently guessing.

Do not ask the user to repeat known information, confirm a verifiable project
fact, choose low-impact style details, or decide implementation details that can
be resolved safely during planning. A clarification answer authorizes only the
choice it states; package, tool, test, configuration, and irreversible-action
approval boundaries remain separate.
