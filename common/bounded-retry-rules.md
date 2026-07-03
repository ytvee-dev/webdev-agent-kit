---
id: 'agents.common.bounded-retry-rules'
title: 'Bounded Retry Rules'
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
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
depends_on: []
---

# Bounded Retry Rules

Purpose: allow useful repair loops without letting agents repeat failed strategies or drift into broad rewrites.

## Default Attempt Limit

Default maximum attempts for a bounded retry loop is 3.

Use a lower limit for risky refactors, destructive operations, or unclear root cause. Use a higher limit only when the user explicitly approves the budget or the loop contract defines it.

## After Each Failed Attempt

The agent must record:

```text
attempt number
what changed
verification command or check
failure evidence
likely cause
new strategy for next attempt
```

Before retrying, the agent must change the hypothesis or implementation strategy. Do not repeat the same patch, same command sequence, or same explanation without new evidence.

## Related Vs Unrelated Failures

When verification fails:

- fix related failures caused by the current change when safe and in scope;
- document unrelated pre-existing failures separately;
- do not expand the task to fix unrelated failures unless the user approves;
- do not weaken TypeScript, lint, security, accessibility, or architecture rules to make verification pass.

## Stop Conditions

Stop the loop when:

- acceptance criteria pass;
- attempt limit is reached;
- required context or tools are unavailable;
- the next fix requires unapproved package, script, config, architecture, or testing workflow changes;
- continuing would require a broader task than the user approved.

## Final Failure Report

When the loop stops without success, report:

```text
attempts made
latest evidence
what changed between attempts
why further retry is not justified
blocker or approval needed
safe next step
```

## Validation Gate

A retry is valid only if it uses new evidence, a changed hypothesis, or a narrower fix than the failed attempt.
