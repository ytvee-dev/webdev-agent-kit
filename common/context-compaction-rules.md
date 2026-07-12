---
id: 'agents.common.context-compaction-rules'
title: 'Context Compaction Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/context'
    - 'workflow/agent-loop'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/checkpoint-rules|Checkpoint Rules]]'
    - '[[templates/loop-workflow-contract|Loop Workflow Contract Template]]'
depends_on: []
---

# Context Compaction Rules

Purpose: preserve the facts an agent needs after long sessions, summarization, host-level compaction, or stop/resume transitions.

Use these rules during standard or deep workflows, bounded loops, repeated failures, and resumable work.

## Preserve In Every Compact Summary

```text
current objective
accepted constraints
allowed scope
acceptance criteria
stable goal, criterion, slice, and finding identifiers when present
files read
files changed
commands or checks run
verification results
failed attempts and changed strategies
user decisions
blockers
next exact step
```

## Preserve Separately From Conversation

Durable project facts belong in `project/**`, not reusable bundle docs.

Use local-only project files only when the work is genuinely resumable, repeated, or likely to matter in later sessions.

Recommended files:

```text
project/active-plan.md
project/progress-log.md
project/decision-log.md
project/loop-memory.md
```

## Loop Memory Rules

When loop memory is used, keep three sections:

```text
Tried: attempts, result, evidence
Verified: confirmed facts and how they were verified
Open: unresolved questions and safe next strategies
```

Do not store guesses as verified facts. Convert failures into reusable rules only after evidence supports them.

When durable identifiers exist, preserve them exactly across summaries,
checkpoints, and loop memory. Do not renumber `G-###`, `AC-###`, or `S-###`
during compaction.

## Anti-Bloat Rules

- Do not copy full logs into memory when a concise failure summary is enough.
- Do not record every inspected file if it was irrelevant.
- Do not publish project facts into reusable bundle docs.
- Do not let memory override current source evidence.

## Validation Gate

A compact summary is useful only if another agent can resume the task without re-deriving the objective, constraints, verification state, and next step.
