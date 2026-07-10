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
    - '[[common/test-policy|Test Change And Verification Policy]]'
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

Use the smallest reliable existing evidence in this precedence order:

1. exact acceptance criterion, failing command, reproduction, route, interaction, or existing regression test;
2. the order and commands recorded in `project/verification-profile.md` when present;
3. relevant existing test, lint, typecheck, build, or format-check commands required by the changed surface;
4. rendered visual QA when visual behavior is in scope;
5. manual source inspection only when executable verification is unavailable.

Do not impose a generic command order over a verified project profile. Run relevant existing tests when they cover changed behavior. Existing-test maintenance, new test authoring, and infrastructure changes follow `common/test-policy.md`.

Do not invent new scripts, package dependencies, testing frameworks, broad test suites, or CI jobs without explicit approval.

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
