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
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
    - '[[skills/loop-workflow-planner/SKILL|Loop Workflow Planner]]'
depends_on: []
---

# Independent Review Rules

Purpose: separate implementation from final judgment when a loop, standard workflow, or deep workflow needs confidence beyond self-review.

The implementer should not be the only judge of its own work when material risk exists.

## When Independent Review Is Required

Use an independent review pass when:

- the task is standard or deep and produced code changes;
- verification failed and was repaired during a loop;
- architecture, state ownership, data flow, security, or build behavior changed;
- the visual surface is significant;
- the user requested review, audit, pass/fail, or merge confidence;
- the loop contract requires a reviewer.

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
```

## Validation Gate

Independent review is valid only when it evaluates the acceptance criteria and evidence instead of merely restating the implementer's summary.
