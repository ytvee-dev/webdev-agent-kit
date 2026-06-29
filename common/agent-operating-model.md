---
id: 'agents.common.agent-operating-model'
title: 'Agent Operating Model'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/operating-model'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/goal-contract|Goal Contract]]'
    - '[[common/planning-rules|Planning Rules]]'
    - '[[common/execution-loops|Execution Loops]]'
depends_on: []
---

# Agent Operating Model

Purpose: keep frontend work goal-aware, scoped, and verifiable without creating
heavy process for narrow tasks.

## Operating Loop

Use one loop unless the task requires a durable plan:

1. Classify the prompt and workflow level.
2. Read the minimum authoritative context.
3. Define the goal or confirm the existing goal.
4. Plan the smallest useful slice.
5. Execute only that slice.
6. Verify with the smallest relevant available check.
7. Report changes, evidence, skipped work, and next step.

## Defaults

- Keep lightweight tasks lightweight.
- Use compact response-only goals and plans for standard tasks when durable
  project files are unnecessary.
- Use durable `project/**` state only for deep or resumable work.
- Prefer local project conventions before generic framework advice.
- Keep reusable workflows in `common/**` and `skills/**`.
- Keep project-specific state in local-only `project/**`.

## Stop Conditions

Stop before continuing when:

- the next step needs user approval;
- the task would install packages, change tooling, or scaffold application code;
- the change would touch production systems or secrets;
- the current evidence contradicts the plan;
- the goal cannot be satisfied without guessing product intent.

