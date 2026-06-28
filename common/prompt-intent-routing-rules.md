---
id: 'agents.common.prompt-intent-routing-rules'
title: 'Prompt Intent Routing Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/policy'
    - 'routing/task-scale'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[SUMMARY|Agent Documentation Summary]]'
    - '[[common/approved-patterns|Approved Patterns]]'
    - '[[common/anti-patterns|Common Anti-Patterns]]'
depends_on: []
---

# Prompt Intent Routing Rules

Purpose: choose the right workflow weight before selecting a skill chain.

## Core Rule

Do not apply the same workflow weight to every user prompt. Classify the prompt intent and task scale before invoking planning, checkpointing, project memory updates, MCP installation checks, deep project scans, or architecture workflows.

A narrow bugfix must stay lightweight. A large ambiguous request must be planned before implementation.

## Intent Classes

Classify every implementation-relevant prompt as one of:

- `micro-fix`
- `small-change`
- `standard-task`
- `large-task`
- `exploratory-plan`
- `deep-architecture`
- `maintenance-only`

## Workflow Levels

Use one of three workflow levels:

- `Lightweight Workflow`
- `Standard Workflow`
- `Deep Workflow`

## Lightweight Workflow

Use for:

- one small bug;
- one obvious typo or type error;
- one small styling adjustment;
- one isolated component change;
- one local refactor with clear boundaries;
- one direct request where the target file, route, component, or error context is obvious.

Behavior:

1. Restate the immediate task in one short sentence only when useful.
2. Inspect only the affected files, error context, supplied screenshot, or rendered surface.
3. Make the smallest safe change.
4. Run the smallest relevant verification available.
5. Report what changed and what was checked.

Do not create or update these files for a lightweight task unless the task escalates:

- `project/active-goals.md`
- `project/active-plan.md`
- `project/progress-log.md`
- `project/decision-log.md`

Do not invoke `goal-planner` or `execution-plan-manager` for a lightweight task unless targeted inspection proves that the task is larger than it first appeared.

## Standard Workflow

Use for:

- a feature touching multiple files;
- a UI implementation from a spec or screenshot;
- a bug with unclear root cause;
- a refactor that needs a behavior boundary;
- a task that needs more than one implementation slice;
- a task that changes project conventions or reusable patterns.

Behavior:

1. Create a compact goal and compact plan.
2. Use project overlays before broad scans.
3. Execute one slice at a time.
4. Verify each slice.
5. Compare the result with the compact plan before finishing.
6. Update checkpoint files only when the task is genuinely multi-step or resumable.

`goal-planner` and `execution-plan-manager` may run in compact mode for standard tasks.

## Deep Workflow

Use for:

- new project creation;
- architecture design;
- stack migration;
- onboarding an unknown project;
- broad visual redesign;
- repeated failures after lightweight or standard attempts;
- large tasks that require durable stop/resume state.

Behavior:

1. Create or update a Goal Contract.
2. Create or update an Execution Plan.
3. Define context budget and scan boundaries.
4. Check required MCP/tools only when they are needed for the current slice.
5. Execute small slices.
6. Update progress and decision logs.
7. Leave a precise stop/resume point.

## Escalation Rules

Escalate from Lightweight to Standard only when:

- the apparent fix touches multiple unrelated files;
- the root cause is unclear after targeted inspection;
- the change affects architecture, routing, data flow, state ownership, or shared styling;
- verification shows the first fix is insufficient;
- the user expands the scope.

Escalate from Standard to Deep only when:

- the task requires project-wide scanning;
- the work cannot be completed safely in one or two slices;
- the task needs long-lived decisions or stop/resume state;
- the task requires new tooling, package installation, framework migration, or architecture changes.

## De-Escalation Rules

De-escalate when a prompt sounds broad but the actionable surface is narrow.

Examples:

- `Fix the dashboard` -> inspect enough to identify the failing surface, then choose Lightweight or Standard.
- `Improve this page` with one screenshot and one target file -> Standard, not Deep.
- `Make the button color match the screenshot` -> Lightweight.
- `Fix this TypeScript error` -> Lightweight unless the error reveals broader type design issues.

## Skill Chain Examples

Small bug prompt:

```text
Lightweight Workflow
-> frontend-bugfix-debugger
-> minimal verification
-> no goal-planner
-> no execution-plan-manager
-> no persistent plan files
```

Large feature prompt:

```text
Standard Workflow
-> goal-planner compact mode
-> execution-plan-manager compact mode
-> relevant frontend skill
-> verification
```

Greenfield or architecture prompt:

```text
Deep Workflow
-> goal-planner
-> execution-plan-manager
-> mcp-toolchain-manager when needed
-> architecture or greenfield skill
```

## Validation Gates

Before selecting a heavy workflow, verify:

- the prompt is not a `micro-fix` or `small-change`;
- the user did not ask for one narrow bugfix or isolated change;
- persistent project memory files are actually needed;
- MCP installation checks are necessary for the current slice;
- broad scans are justified by the task scale.

Before finishing a lightweight task, verify:

- no unnecessary plan or checkpoint files were created;
- no unrelated source files were changed;
- the response reports the small verification that was run or honestly reports why it was not run.
