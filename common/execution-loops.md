---
id: 'agents.common.execution-loops'
title: 'Execution Feedback Cycles'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/execution'
    - 'workflow/agent-loop'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/checkpoint-rules|Checkpoint Rules]]'
    - '[[common/feedback-cycle-policy|Feedback Cycle Policy]]'
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
    - '[[common/bounded-retry-rules|Bounded Retry Rules]]'
    - '[[templates/progress-log|Progress Log Template]]'
depends_on: []
---

# Execution Feedback Cycles

Purpose: keep implementation, debugging, refactoring, review, and verification work in short evidence-based feedback cycles.

These are workflow cycles only. They never authorize iterative constructs in host project code.

Use `common/agent-loop-policy.md` when a cycle must repeat until measurable acceptance criteria pass, when retry limits matter, or when independent review and loop memory are required.

## Standard Cycle

1. Confirm the slice goal.
2. Inspect only required context.
3. Make the smallest scoped change.
4. Run the relevant check.
5. Fix issues caused by the change.
6. Update progress or report evidence.

## Debug Cycle

1. Record the symptom and reproduction path.
2. Form one hypothesis.
3. Inspect evidence for that hypothesis.
4. Apply the smallest fix.
5. Re-run the failing check or reproduce the behavior.
6. If the check fails again, change hypothesis before retrying.

## Refactor Cycle

1. Define the behavior boundary.
2. Identify safe mechanical steps.
3. Change one boundary at a time.
4. Run the same verification after each meaningful step.
5. Stop if behavior changes without approval.

## Bounded Loop Escalation

Escalate from an execution cycle to a Loop Workflow Contract when:

- the user asks to continue until a measurable condition passes;
- verification has already failed;
- repair may need multiple attempts;
- the task needs independent review;
- the task needs durable loop memory.

Do not escalate lightweight work into loop planning unless repeated failure or explicit user instruction justifies it.
