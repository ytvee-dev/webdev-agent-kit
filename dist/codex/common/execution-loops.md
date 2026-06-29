---
id: 'agents.common.execution-loops'
title: 'Execution Loops'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/execution'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/checkpoint-rules|Checkpoint Rules]]'
    - '[[templates/progress-log|Progress Log Template]]'
depends_on: []
---

# Execution Loops

Purpose: keep implementation, debugging, refactoring, review, and verification
work in short loops with clear evidence.

## Standard Loop

1. Confirm the slice goal.
2. Inspect only required context.
3. Make the smallest scoped change.
4. Run the relevant check.
5. Fix issues caused by the change.
6. Update progress or report evidence.

## Debug Loop

1. Record the symptom and reproduction path.
2. Form one hypothesis.
3. Inspect evidence for that hypothesis.
4. Apply the smallest fix.
5. Re-run the failing check or reproduce the behavior.

## Refactor Loop

1. Define the behavior boundary.
2. Identify safe mechanical steps.
3. Change one boundary at a time.
4. Run the same verification after each meaningful step.
5. Stop if behavior changes without approval.

