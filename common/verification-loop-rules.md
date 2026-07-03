---
id: 'agents.common.verification-loop-rules'
title: 'Verification Loop Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/agent-loop'
    - 'quality/verification'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/stop-criteria-rules|Stop Criteria Rules]]'
    - '[[common/bounded-retry-rules|Bounded Retry Rules]]'
    - '[[common/lint-verification-rules|Lint Verification Rules]]'
depends_on: []
---

# Verification Loop Rules

Purpose: connect frontend implementation work to existing project verification without creating new tooling or testing workflows by default.

## Code-Changing Loop

For code-changing frontend work:

```text
implement smallest scoped slice
run smallest relevant existing verification
classify failures
fix related failures when safe and in scope
rerun the same verification
stop when criteria pass or retry rules stop the loop
report evidence
```

## Verification Source Order

Use the smallest reliable existing check:

1. exact failing command, reproduction, route, or interaction;
2. relevant lint command;
3. relevant typecheck command;
4. relevant build command;
5. rendered visual QA when visual behavior is in scope;
6. manual source inspection only when executable verification is unavailable.

Do not invent new scripts, package dependencies, testing frameworks, or CI jobs without explicit approval.

## Failure Classification

Classify verification output as:

```text
passed
failed: related to current change
failed: likely pre-existing
failed: unrelated environment/tool issue
blocked: required command or tool unavailable
unknown: evidence insufficient
```

## Rerun Rules

- Rerun the same verification after a related fix.
- Do not switch to an easier command just to claim success.
- If a narrower command proves the fix but a broader command still fails, report both.
- If verification is blocked, report the blocked check and the confidence impact.

## Final Evidence

Final reports for code-changing loops must include:

```text
commands or rendered checks run
results
attempt count
unresolved failures
blocked checks
confidence level
```

## Validation Gate

A loop cannot be reported as successful unless the acceptance criteria pass or unresolved deviations are explicitly documented as out of scope, blocked, or user-approved.
