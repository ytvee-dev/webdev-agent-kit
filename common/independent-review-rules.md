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
- Codex or GPT-based coding agents should run a separate `frontend-quality-reviewer` pass or equivalent fresh review pass.
- GitHub workflows may use PR review, diff review, comments, and CI evidence.
- Generic agents should switch to review mode and avoid further implementation unless fixes are explicitly requested.

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

## Validation Gate

Independent review is valid only when it evaluates the acceptance criteria and
evidence instead of merely restating the implementer's summary. Review findings
must not add, remove, reorder, renumber, or mark plan slices.
