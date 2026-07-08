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
    - '[[common/windows-shell-sandbox-rules|Windows Shell Sandbox Rules]]'
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

## Shell And Sandbox Retry Limit

A shell or sandbox blocker is not evidence that the project code is broken.

When a verification command fails because PowerShell blocks a `.ps1` shim, the only default retry is the equivalent `.cmd` command when available.

When build, dev-server, browser, Vite, esbuild, SWC, Next.js, or Playwright startup fails because the sandbox cannot access files, binaries, caches, parent directories, temporary directories, or child processes, the only default retry is one approved out-of-sandbox attempt when the host supports it.

If the same shell or sandbox class failure repeats after the allowed fallback, stop. Do not repeat the same command, start another dev server, start browser QA, or change project code to bypass an environment blocker.

## Related Vs Unrelated Failures

When verification fails:

- fix related failures caused by the current change when safe and in scope;
- document unrelated pre-existing failures separately;
- document shell or sandbox blockers separately from code failures;
- do not expand the task to fix unrelated failures unless the user approves;
- do not weaken TypeScript, lint, security, accessibility, or architecture rules to make verification pass.

## Stop Conditions

Stop the loop when:

- acceptance criteria pass;
- attempt limit is reached;
- required context or tools are unavailable;
- shell or sandbox verification is blocked after the allowed fallback;
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

A retry is valid only if it uses new evidence, a changed hypothesis, a narrower fix than the failed attempt, or an approved execution-boundary change for a documented shell or sandbox blocker.
