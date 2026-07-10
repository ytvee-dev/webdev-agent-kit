---
id: 'agents.common.policy-precedence'
title: 'Policy Precedence'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'policy/precedence'
    - 'workflow/safety'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/core/runtime-core-policy|Portable Runtime Core Policy]]'
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[profiles/react-typescript/PROFILE|React TypeScript Profile]]'
depends_on: []
---

# Policy Precedence

Purpose: resolve instruction conflicts consistently across runtime clients without repeating priority rules inside individual skills.

## Precedence Order

When two applicable instructions conflict, the higher level wins:

1. System, client security, and sandbox restrictions.
2. Current direct user request.
3. Explicitly confirmed scope and approvals.
4. Existing host-project instructions.
5. Verified `project/**` facts.
6. Selected skill workflow.
7. Active frontend profile.
8. Generic kit defaults.

This order resolves instruction authority, not factual truth. Use the owning evidence policy to decide which technical claim is proven.

## Resolution Rules

1. Identify the smallest conflicting statements and their levels.
2. Apply the higher-level statement only to the conflict; preserve compatible lower-level guidance.
3. Treat an explicit current request as approval only for actions it clearly names. Do not infer approval for dependencies, external writes, irreversible actions, or scope expansion.
4. Use host-project instructions and `project/**` facts only when they apply to the current path and task.
5. A skill may narrow execution but cannot expand user scope or permissions.
6. A profile supplies defaults only; verified project facts and the selected skill may specialize them.
7. If same-level instructions remain materially ambiguous, ask for the smallest decision needed instead of guessing.

## Authoring Boundary

Keep this ordered contract here. Other runtime files may link to it and state a narrow local exception, but must not copy, reorder, or redefine the global precedence list.

Avoid absolute claims that a skill, profile, adapter, or reusable rule always wins. Security and sandbox restrictions remain non-overridable; all other conflicts use the ordered contract above.
