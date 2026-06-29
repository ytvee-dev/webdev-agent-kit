---
id: 'agents.common.checkpoint-rules'
title: 'Checkpoint Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/checkpoints'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[templates/progress-log|Progress Log Template]]'
    - '[[templates/decision-log|Decision Log Template]]'
depends_on: []
---

# Checkpoint Rules

Purpose: make deep or resumable frontend work safe to stop and resume.

## When To Checkpoint

Use checkpoint files only for deep or genuinely resumable standard work.

Checkpoint after:

- a completed implementation slice;
- a user-approved architecture decision;
- a verification result that changes the plan;
- a blocker that another run must understand.

## Required Stop State

Every stop state must include:

- current phase;
- last completed slice;
- next exact step;
- files or overlays to inspect next;
- checks to run next;
- blockers, risks, and approval gates.

Keep checkpoint files in local-only `project/**`.

