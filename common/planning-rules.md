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
    - '[[templates/execution-plan|Execution Plan Template]]'
depends_on: []
---

# Planning Rules

Purpose: split frontend work into small, evidence-backed slices.

## Slice Rules

- Each slice must have one target surface and one verification method.
- Prefer component, route, bug hypothesis, spec handoff, or visual QA slices.
- Do not combine architecture migration, dependency changes, and UI
  implementation in one slice.
- Add an approval gate before package installs, framework migration, build
  tooling changes, UI libraries, testing workflows, or broad refactors.
- Record skipped slices instead of silently dropping them.

## Context Budget

- `Glance`: routing, status, or shallow explanation.
- `Scoped`: affected files, relevant overlays, and nearby patterns.
- `Deep`: onboarding, architecture, broad redesign, unclear root cause, or
  repeated failure.

Use the smallest budget that can produce a correct result.
