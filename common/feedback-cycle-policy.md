---
id: 'agents.common.feedback-cycle-policy'
title: 'Feedback Cycle Policy'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/feedback'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/execution-loops|Execution Loops]]'
    - '[[skills/frontend-bugfix-debugger/SKILL|Frontend Bugfix Debugger]]'
    - '[[skills/frontend-refactor-surgeon/SKILL|Frontend Refactor Surgeon]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
depends_on: []
---

# Feedback Cycle Policy

Purpose: define where workflow feedback cycles are useful and prevent confusion with project-code iteration.

Workflow feedback cycles are allowed only as agent process control. They do not authorize iterative constructs in host project code.

## Relevant Skills

- `frontend-bugfix-debugger`: reproduce, form one hypothesis, patch, rerun the same check.
- `frontend-refactor-surgeon`: change one behavior boundary, verify, stop on behavior drift.
- `frontend-visual-qa`: capture rendered evidence, compare, report or fix scoped visual deviations.
- `frontend-quality-reviewer`: review evidence, classify findings, verify that required fixes are separate from optional improvements.
- `agent-rules-skill-author`: draft, run trigger and workflow evals, validate paths and metadata, then revise.
- `execution-plan-manager`: split work into small slices and record stop or resume state.

## Not Relevant

Do not use a workflow feedback cycle for one obvious edit, direct typo fixes, static value lookup, or tasks that need a single answer.

## Validation Gates

- Call them workflow feedback cycles, not code loops.
- Keep feedback cycles finite and evidence-based.
- Do not use feedback-cycle wording to justify iterative constructs in project code.
