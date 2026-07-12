---
id: 'agents.common.planning-rules'
title: 'Planning Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/planning'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/execution-plan-manager/SKILL|Execution Plan Manager]]'
    - '[[common/planning-analysis-rules|Planning Analysis Rules]]'
    - '[[templates/execution-plan|Execution Plan Template]]'
depends_on: []
---

# Planning Rules

Purpose: split frontend work into small, evidence-backed slices.

## Slice Rules

- Identify durable execution slices as `S-###` and reference every acceptance
  criterion they cover, for example `S-001 [AC-001, AC-002]`.
- Each slice must have one target surface and one verification method.
- Prefer component, route, bug hypothesis, spec handoff, or visual QA slices.
- Do not combine architecture migration, dependency changes, and UI
  implementation in one slice.
- Add an approval gate before package installs, framework migration, build
  tooling changes, UI libraries, testing workflows, or broad refactors.
- Record skipped slices instead of silently dropping them.
- Keep slice identifiers stable after execution begins. Never renumber completed,
  blocked, skipped, or superseded slices.

## Enabling Slices

A slice with no direct user-facing acceptance criterion must use the `ENABLER`
label and name the later slices it unlocks:

```text
S-003 [ENABLER -> S-004, S-005] Confirm the existing route ownership.
```

Do not use `ENABLER` for generic setup, speculative infrastructure, broad
research, package installation, or work that has no approved downstream slice.
Approval gates still apply to dependencies, tools, configuration, tests, and
architecture changes.

## Identifier Boundaries

- Durable standard and deep plans use zero-padded `S-###` identifiers.
- Compact response-only plans may omit identifiers when they contain at most two
  direct slices and do not require resume state or cross-slice traceability.
- `Fast Lookup` and `Lightweight Workflow` do not create execution plans or IDs.

## Coverage Map

Every durable plan must map active acceptance criteria to implementation slices
and verification without copying the full criterion text:

```text
AC-001 -> S-001, S-002 -> existing check or rendered evidence -> planned
```

Allowed coverage states are:

```text
planned | in-progress | verified | blocked | superseded
```

- Every active `AC-###` must map to at least one `S-###` and one verification
  source before implementation begins.
- `ENABLER` slices appear through their downstream dependency links; they do not
  substitute for criterion coverage.
- Mark a criterion `verified` only after the named evidence passes. A completed
  slice or checked box alone is not verification.
- Record the exact missing command, tool, context, or approval for `blocked`.
- Link `superseded` criteria to their replacement instead of deleting history.
- Keep the map compact: reference identifiers and evidence, not duplicated goal
  or plan prose.

## Context Budget

- `Glance`: routing, status, or shallow explanation.
- `Scoped`: affected files, relevant overlays, and nearby patterns.
- `Deep`: onboarding, architecture, broad redesign, unclear root cause, or
  repeated failure.

Use the smallest budget that can produce a correct result.

Before standard or deep implementation begins, use
`common/planning-analysis-rules.md` when the execution plan has multiple slices,
approval boundaries, shared file ownership, or unresolved assumptions. The
analysis pass is read-only and does not repair the plan.
