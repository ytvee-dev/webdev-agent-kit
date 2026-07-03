---
id: 'agents.common.stop-criteria-rules'
title: 'Stop Criteria Rules'
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
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
    - '[[templates/loop-workflow-contract|Loop Workflow Contract Template]]'
depends_on: []
---

# Stop Criteria Rules

Purpose: make completion measurable before an agent starts iterative work.

A stop criterion says exactly how the agent knows the loop is done.

## Good Stop Criteria

Good criteria are observable, scoped, and tied to the task:

```text
lint passes
related typecheck passes
related build command passes
affected route loads without blocking runtime errors
no new console error appears during visual QA
small-phone viewport has no horizontal overflow
specified form error state is visible and actionable
visual deviations are fixed or documented
PR summary lists changed files and verification evidence
```

## Bad Stop Criteria

Bad criteria are vague, subjective, or unbounded:

```text
make it better
improve the code
make it beautiful
polish the UI
optimize performance
clean everything up
keep going until it feels right
```

Convert vague criteria into measurable checks before starting a standard or deep loop. If the user goal remains ambiguous and the answer would materially affect implementation, route to `goal-planner` or ask for clarification.

## Required Fields

Every loop stop definition must include:

```text
success condition
verification source
failure condition
attempt limit
blocked condition
```

## Frontend Examples

### Bugfix

```text
success: reported symptom no longer reproduces and lint passes
verification: reproduction steps plus existing lint command
failure: symptom still reproduces after patch
attempt limit: 3
blocked: reproduction path or required credentials unavailable
```

### Visual QA Repair

```text
success: material visual deviations are resolved or explicitly documented
verification: rendered screenshot comparison at required viewports
failure: same deviation remains after scoped fix
attempt limit: 3
blocked: Browser or Playwright MCP unavailable for required rendered check
```

### Refactor

```text
success: public behavior is preserved and related verification passes
verification: existing lint/typecheck/build plus optional rendered check
failure: public contract changes without approval
attempt limit: 2
blocked: required ownership boundary cannot be determined
```

## Validation Gate

Do not begin a goal-based loop unless the stop criteria are measurable enough for another reviewer to evaluate independently.
