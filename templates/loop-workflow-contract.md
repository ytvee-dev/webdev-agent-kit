---
id: 'agents.templates.loop-workflow-contract'
title: 'Loop Workflow Contract Template'
doc_type: 'template'
layer: 'template'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/template'
    - 'workflow/agent-loop'
parent:
    - '[[skills/loop-workflow-planner/SKILL|Loop Workflow Planner]]'
related:
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/stop-criteria-rules|Stop Criteria Rules]]'
    - '[[common/bounded-retry-rules|Bounded Retry Rules]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
    - '[[common/independent-review-rules|Independent Review Rules]]'
depends_on: []
---

# Loop Workflow Contract

Goal ID: G-###

Target Slices: S-###

## Objective

...

## Allowed Scope

```text
files or surfaces allowed:
files or surfaces excluded:
explicit approvals required:
```

## Acceptance Criteria

```text
criterion: AC-###
success condition:
verification source:
failure condition:
blocked condition:
```

## Loop Type

```text
one-pass verification | bounded retry | goal-based loop | open exploration
```

## Max Attempts Or Turns

...

## Retry Strategy

```text
what changes after a failed attempt:
what must not be repeated:
what counts as unrelated failure:
```

## Attempt Record

```text
attempt:
criteria: AC-###
slices: S-###
changed strategy:
evidence:
result:
```

## Verification

```text
commands:
rendered checks:
manual checks:
blocked checks:
```

## Independent Review

```text
required: yes | no
reviewer skill or mechanism:
pass/fail criteria:
```

## Memory Update

```text
needed: yes | no
project file:
what to record:
```

## Stop Conditions

```text
stop on success:
stop on attempt limit:
stop on blocked verification:
stop on scope expansion:
stop on approval requirement:
```

## Escalation Conditions

...

## Final Evidence

```text
attempts made:
files changed:
checks run:
results:
remaining risks:
next slice: S-###
```
