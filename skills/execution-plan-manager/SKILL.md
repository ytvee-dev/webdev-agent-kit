---
name: execution-plan-manager
description: Use for standard or deep frontend work that needs an execution plan, task slices, checkpoint rules, loop handoff decisions, and stop/resume state after a goal is defined. Do not use for lightweight micro-fixes or isolated direct edits unless the task escalates.
id: 'agents.skills.execution-plan-manager.skill'
title: 'Execution Plan Manager'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'execution-plan-manager'
tags:
    - 'agents/skill-package'
    - 'agents/planning'
    - 'workflow/execution-plan'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/goal-planner/SKILL|Goal Planner]]'
    - '[[skills/loop-workflow-planner/SKILL|Loop Workflow Planner]]'
    - '[[common/planning-rules|Planning Rules]]'
    - '[[common/execution-loops|Execution Loops]]'
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/token-budget-rules|Token Budget Rules]]'
    - '[[common/checkpoint-rules|Checkpoint Rules]]'
    - '[[templates/execution-plan|Execution Plan Template]]'
    - '[[templates/loop-workflow-contract|Loop Workflow Contract Template]]'
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Execution Plan Manager

## Purpose

Create, maintain, and review execution plans for standard or deep frontend work after the goal is defined.

This skill prevents large tasks from becoming unbounded development sessions. It splits work into small verified slices, selects the minimum useful context budget, records stop/resume state when needed, and decides whether a slice needs a one-pass check, bounded retry loop, goal-based loop, independent review, or durable memory handoff.

## When To Use

Use this skill only after `AGENTS.md` and `common/prompt-intent-routing-rules.md` classify the task as `Standard Workflow` or `Deep Workflow`.

Use this skill when:

- a goal contract exists or the user goal is already explicit;
- the task needs more than one implementation slice;
- the task may need stop/resume state;
- the task has dependencies, blockers, or ordered phases;
- the task should be split before coding;
- the user asks to continue an existing large task;
- the agent needs to compare completed work with the plan;
- the task may require measurable iteration and should be handed to `loop-workflow-planner`.

## When Not To Use

Do not use this skill for `Lightweight Workflow` prompts, including one small bug, one obvious typo, one obvious type error, one small styling adjustment, one isolated component change, one direct file-scope edit, or one local refactor with clear boundaries.

Do not use this skill to implement code, install tools, scaffold projects, rewrite architecture, create tests, or perform visual QA.

If a lightweight task reveals hidden scope or repeated failure, escalate first using `common/prompt-intent-routing-rules.md`, then use this skill only if the escalated task is standard or deep.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when task scale is not obvious.
3. Read `common/planning-rules.md`.
4. Read `common/checkpoint-rules.md` when durable stop/resume state is needed.
5. Read `common/agent-loop-policy.md` when the plan may need measurable iteration.
6. Confirm the workflow level is `Standard Workflow` or `Deep Workflow`.
7. Read the current goal contract from the response, user request, or `project/active-goals.md` when present and relevant.
8. Read only project overlays needed to slice the task safely, such as `project/stack-profile.md`, `project/architecture-map.md`, `project/styling-profile.md`, or `project/verification-profile.md`.
9. Read affected source files only when slicing cannot be done safely without them.
10. Do not read human-facing documentation unless the task changes that documentation.

## Tool Contract

- Use filesystem access only when a durable execution plan, progress log, loop contract, or stop/resume state must be written or updated.
- Do not use MCP installation checks from this skill.
- Do not use Browser, Playwright, Visual Diff, Figma, or design-tool MCP from this skill.
- Do not install packages or tools.
- Do not change application source files.
- Do not create testing workflows or testing files.

## Workflow

1. Confirm task scale. If lightweight, stop and route back to the direct skill without creating an execution plan.
2. Confirm goal. Use an existing Goal Contract when available. If no goal exists and the task is ambiguous, route to `goal-planner` first.
3. Choose plan mode: compact response-only planning for standard tasks that can finish in one or two slices, durable planning for deep or resumable tasks.
4. Choose context budget: `Glance`, `Scoped`, or `Deep`.
5. Split into small independently verifiable slices.
6. Add verification per slice using the smallest relevant check already available in the project or active skill.
7. Decide whether a loop contract is needed. Use `loop-workflow-planner` when a slice must repeat until measurable acceptance criteria pass, when verification failure repair is in scope, when repeated failure already happened, when independent review should judge completion, or when loop memory is needed.
8. Add stop/resume state for durable plans, including current phase, last completed slice, next exact step, files to inspect next, checks to run next, loop contract or retry limit when relevant, blockers, and risks.
9. Hand off to the smallest relevant skill. Route measurable iteration to `loop-workflow-planner` before implementation.
10. When invoked after execution, compare plan and result, including completed scope, skipped scope, deviations, verification evidence, loop attempts, stop condition, and next step.

## Output Contract

Return or write an Execution Plan with:

```text
Goal
Done When
Workflow Level
Context Budget
Current Phase
Task Slices
Allowed Files Or Surfaces
Tools Allowed
Verification Per Slice
Loop Needed
Loop Handoff
Blockers
Risks
Stop Point
Next Skill Or Next Step
```

For durable plans, write or update:

```text
project/active-plan.md
project/progress-log.md
project/decision-log.md
project/loop-memory.md when loop memory is required
```

only when the task is genuinely multi-step, iterative, or resumable.

## Validation Gates

Before finishing, verify:

- the task was not a lightweight prompt;
- a goal exists or the task was routed to `goal-planner`;
- slices are small and independently verifiable;
- context budget is explicit;
- loop handoff is explicit when bounded retry or measurable iteration is required;
- persistent files were created only for durable standard or deep work;
- no source files were changed;
- no tools or packages were installed;
- no testing workflow was introduced;
- next step is precise enough for another agent run to resume.

## Trigger Evals

Should trigger:

- "Break this dashboard implementation into small steps."
- "Continue the previous big frontend task and tell me exactly where to resume."
- "Create an execution plan for this redesign after the goal is clear."
- "We need to implement this feature in slices without losing progress."
- "Plan the task and decide whether it needs a bounded loop."

Should not trigger:

- "Fix this TypeScript error."
- "Change this button color."
- "Fix the broken margin in this component."
- "Rename this prop in one file."
- "Define the goal first."
- "Run visual QA on this page."

## Reference Map

- `AGENTS.md` - canonical policy, routing, tool rules, and documentation rules.
- `common/prompt-intent-routing-rules.md` - workflow weight selection and escalation/de-escalation rules.
- `common/planning-rules.md` - context budget and task slice rules.
- `common/checkpoint-rules.md` - stop/resume state rules.
- `common/agent-loop-policy.md` - bounded loop policy.
- `templates/execution-plan.md` - durable execution plan template.
- `templates/loop-workflow-contract.md` - durable loop contract template.
- `skills/goal-planner/SKILL.md` - goal contract producer for standard or deep work.
- `skills/loop-workflow-planner/SKILL.md` - loop contract producer for measurable iteration.
- `project/active-plan.md` - optional local-only durable execution plan for deep or resumable work.
- `project/progress-log.md` - optional local-only progress log.
- `project/decision-log.md` - optional local-only decision log.
- `project/loop-memory.md` - optional local-only loop memory.
