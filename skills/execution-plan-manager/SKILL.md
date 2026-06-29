---
name: execution-plan-manager
description: Use for standard or deep frontend work that needs an execution plan, task slices, checkpoint rules, and stop/resume state after a goal is defined. Do not use for lightweight micro-fixes or isolated direct edits unless the task escalates.
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
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/goal-planner/SKILL|Goal Planner]]'
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Execution Plan Manager

## Purpose

Create, maintain, and review execution plans for standard or deep frontend work after the goal is defined.

This skill prevents large tasks from becoming unbounded development sessions. It splits work into small verified slices, selects the minimum useful context budget, records stop/resume state when needed, and compares completed work against the plan before handoff or final reporting.

## When To Use

Use this skill only after `AGENTS.md` and `common/prompt-intent-routing-rules.md` classify the task as `Standard Workflow` or `Deep Workflow`.

Use this skill when:

- a goal contract exists or the user goal is already explicit;
- the task needs more than one implementation slice;
- the task may need stop/resume state;
- the task has dependencies, blockers, or ordered phases;
- the task should be split before coding;
- the user asks to continue an existing large task;
- the agent needs to compare completed work with the plan.

## When Not To Use

Do not use this skill for `Lightweight Workflow` prompts, including:

- one small bug;
- one obvious typo;
- one obvious type error;
- one small styling adjustment;
- one isolated component change;
- one direct file-scope edit;
- one local refactor with clear boundaries.

Do not use this skill to implement code, install tools, scaffold projects, rewrite architecture, create tests, or perform visual QA.

If a lightweight task reveals hidden scope, escalate first using `common/prompt-intent-routing-rules.md`, then use this skill only if the escalated task is standard or deep.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when task scale is not obvious.
3. Confirm the workflow level is `Standard Workflow` or `Deep Workflow`.
4. Read the current goal contract from the response, user request, or `project/active-goals.md` when present and relevant.
5. Read only project overlays needed to slice the task safely, such as `project/stack-profile.md`, `project/architecture-map.md`, `project/styling-profile.md`, or `project/verification-profile.md`.
6. Read affected source files only when slicing cannot be done safely without them.
7. Do not read `SUMMARY.md` unless the task explicitly edits, audits, or summarizes it.

## Tool Contract

- Use filesystem access only when a durable execution plan, progress log, or stop/resume state must be written or updated.
- Do not use MCP installation checks from this skill.
- Do not use Browser, Playwright, Visual Diff, Figma, or design-tool MCP from this skill.
- Do not install packages or tools.
- Do not change application source files.
- Do not create testing workflows or testing files.

## Workflow

1. Confirm task scale.
   - If the task is lightweight, stop and route back to the direct skill without creating an execution plan.
   - If the task is standard or deep, continue.

2. Confirm goal.
   - Use an existing Goal Contract when available.
   - If no goal exists and the task is ambiguous, route to `goal-planner` first.
   - Do not invent missing user goals.

3. Choose plan mode.
   - Use compact response-only planning for standard tasks that can finish in one or two slices.
   - Use durable planning for deep tasks or work that may need stop/resume state.

4. Choose context budget.
   - `Glance`: routing, planning, or shallow explanation.
   - `Scoped`: most implementation planning with affected files and relevant overlays only.
   - `Deep`: onboarding, architecture, broad redesign, unclear root cause, migration, or repeated failure.

5. Split into slices.
   A good slice is:
   - one component;
   - one route integration;
   - one screen section;
   - one bug hypothesis;
   - one design/spec handoff;
   - one visual QA pass;
   - one refactor boundary;
   - one project overlay refresh.

6. Add verification per slice.
   Verification must use the smallest relevant check already available in the project or active skill. Do not invent new testing workflows.

7. Add stop/resume state.
   For durable plans, include:
   - current phase;
   - last completed slice;
   - next exact step;
   - files to inspect next;
   - checks to run next;
   - blockers and risks.

8. Hand off.
   - Route the next slice to the smallest relevant skill.
   - Do not continue into implementation from this skill.

9. Compare plan and result when invoked after execution.
   - Record completed scope.
   - Record skipped scope.
   - Record deviations.
   - Record verification evidence or missing verification honestly.
   - Record next step.

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
```

only when the task is genuinely multi-step or resumable.

## Validation Gates

Before finishing, verify:

- the task was not a lightweight prompt;
- a goal exists or the task was routed to `goal-planner`;
- slices are small and independently verifiable;
- context budget is explicit;
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
- `skills/goal-planner/SKILL.md` - goal contract producer for standard or deep work.
- `project/active-plan.md` - optional local-only durable execution plan for deep or resumable work.
- `project/progress-log.md` - optional local-only progress log.
- `project/decision-log.md` - optional local-only decision log.
