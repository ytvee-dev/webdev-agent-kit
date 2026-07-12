---
id: 'agents.common.agent-loop-policy'
title: 'Agent Loop Policy'
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
    - '[[common/stop-criteria-rules|Stop Criteria Rules]]'
    - '[[common/bounded-retry-rules|Bounded Retry Rules]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
    - '[[common/context-compaction-rules|Context Compaction Rules]]'
    - '[[common/independent-review-rules|Independent Review Rules]]'
    - '[[common/worktree-parallelism-rules|Worktree Parallelism Rules]]'
    - '[[skills/loop-workflow-planner/SKILL|Loop Workflow Planner]]'
depends_on: []
---

# Agent Loop Policy

Purpose: define platform-neutral bounded feedback loops for Codex, GPT-based coding agents, Claude Code, Claude Agent SDK, GitHub PR workflows, and generic coding agents.

A loop is a bounded cycle:

```text
discover -> plan -> execute -> verify -> iterate or stop
```

Use loops when a standard or deep workflow must repeat until measurable acceptance criteria pass, especially bugfixes, CI repair, lint repair, visual QA repair, multi-step refactors, and large UI implementation.

Do not use loops for Fast Lookup, tiny edits, one obvious typo, one isolated explanation, or small direct changes unless repeated failure or explicit user request justifies escalation.

## Loop Contract

Every loop must define:

```text
objective
allowed scope
acceptance criteria
goal, criterion, and target slice identifiers when present
verification source
maximum attempts or turns
retry strategy
stop conditions
escalation conditions
final evidence
```

## Host Mapping

Do not require host-specific commands in reusable rules.

- Claude Code may map the contract to `/goal`, `/loop`, subagents, or workflow primitives when available.
- Claude Agent SDK may map the contract to an agent loop with tool calls, max turns, and evaluators.
- Codex or GPT-based coding agents should execute the same contract manually through plan, edit, verify, retry, review, and final evidence.
- GitHub workflows should map the contract to branch scope, commits, PR evidence, CI output, and review.
- Generic agents should follow the contract without assuming special loop commands exist.

## Default Loop Types

### One-Pass Verification

Use for ordinary code changes that need a single verification pass.

### Bounded Retry

Use when verification can fail and the agent is allowed to fix related failures. Default maximum attempts: 3 unless a task-specific contract sets a different limit.

### Goal-Based Loop

Use when the user explicitly asks to continue until a measurable condition is true.

### Open Exploration

Use only for deep research, experiments, or broad discovery with explicit budget and stop rules. Closed loops are the default for web development work.

## Hard Rules

- Never run an unbounded loop.
- Never use vague quality as the only stop condition.
- Never repeat the same failed patch or hypothesis without new evidence.
- Reference the affected `AC-###` and `S-###` in every retry attempt when a
  durable plan exists.
- Never redefine active criteria or renumber slices inside a loop contract.
- Never expand scope, install packages, add tools, change build systems, or create testing workflows without explicit approval.
- Stop when acceptance criteria pass, the attempt limit is reached, scope changes are required, or required verification is blocked.

## Validation Gate

A loop is valid only when the agent can state what will be checked, how many attempts are allowed, what stops the loop, and what evidence will be reported.
