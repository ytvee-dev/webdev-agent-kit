---
id: 'agents.common.independent-review-rules'
title: 'Independent Review Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/review'
    - 'workflow/agent-loop'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/planning-rules|Planning Rules]]'
    - '[[common/convergence-rules|Convergence Rules]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
    - '[[skills/loop-workflow-planner/SKILL|Loop Workflow Planner]]'
depends_on: []
---

# Independent Review Rules

Purpose: separate implementation from final judgment when a loop, standard workflow, or deep workflow needs confidence beyond self-review.

The implementer should not be the only judge of its own work when material risk exists.

## When Independent Review Is Required

Use an independent review pass when:

- the user requested review, audit, pass/fail, or merge confidence;
- the loop contract requires a reviewer;
- a material verification failure was repaired and residual risk remains;
- architecture, state ownership, data flow, security, or build behavior changed materially;
- the changed visual surface is large or high-risk.

Standard or deep workflow classification alone does not require an independent review. Use the risk and acceptance criteria of the current task.

## Platform-Neutral Mapping

- Claude Code may use a fresh subagent, goal verifier, or review primitive when available.
- Claude Agent SDK may use a separate evaluator or reviewer agent.
- Codex or GPT-based coding agents should run `frontend-quality-reviewer` in a fresh session or isolated reviewer; otherwise label the pass self-review.
- GitHub workflows may use PR review, diff review, comments, and CI evidence.
- Generic agents without fresh-context support may perform self-review and report that independence is unavailable. A role switch does not create a fresh context.

## Reviewer Duties

The reviewer must:

```text
read acceptance criteria
read diff or changed files
read verification evidence
classify pass, pass with concerns, or fail
separate required fixes from optional improvements
cite concrete evidence for blocking or high findings
avoid broad rewrite
avoid implementing fixes unless explicitly requested
preserve existing goal, criterion, slice, and finding identifiers
report remaining work without adding or renumbering plan slices
```

The reviewer judges active `AC-###` criteria against coverage and verification
evidence. It does not create a second acceptance model or mutate the execution
plan. When review exposes remaining work, hand the evidence to
`execution-plan-manager` in `converge` mode; convergence alone may append new
slices under `common/convergence-rules.md`.

## Context Isolation

Use `fresh-context` only for a separate session or isolated reviewer that has
not inherited the implementation conversation. Switching skills in the same
conversation is `self-review`; describe missing independence when it affects
confidence. Do not spawn agents unless the active client and task authorize it.

Pass the diff, active criteria, relevant decision records and domain terms,
verification evidence, and paths needed to inspect surrounding code. Do not
forward the implementation transcript or use its conclusion as proof. Include
intentional tradeoffs from decisions so the reviewer can judge them fairly.

For material state, request, or navigation risk, seek a reproducible
counterexample such as duplicate submission, stale response, or lost edits.
A clean review is valid: never invent findings to satisfy a quota. Distinguish
correctness and scope defects from preferences. If a combined review-and-fix
request authorizes repairs, review the repaired diff in a fresh context before
claiming independent verification of those repairs.

## Validation Gate

Independent review is valid only when it evaluates the acceptance criteria and
evidence instead of merely restating the implementer's summary. Review findings
must not add, remove, reorder, renumber, or mark plan slices.

## Scoped Repair Review

For delegated durable review use `common/subagent-handoff-rules.md` and
`skills/frontend-quality-reviewer/references/review-handoffs.md`. The review
surface must include all task commits or the actual uncommitted snapshot, not
only the last commit. Re-review the open findings and repair-induced risk; widen
only for concrete dependent-interface, security, or outcome evidence. Unrelated
preferences never extend a repair loop. Preserve required failed criteria at
the attempt cap; completion is not manufactured by deferring mandatory work.
