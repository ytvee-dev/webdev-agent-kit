# Prompt Intent And Task Scale Routing

Status: draft architecture plan addendum.
Scope: prompt-level workflow selection for future WebDev Assistant routing.

## Purpose

The skill pack must not apply the same heavy workflow to every user prompt.

A small bugfix must not trigger persistent goal files, a multi-step execution plan, MCP installation checks, architecture decomposition, or project-wide scans. A large ambiguous project request must not jump straight into code.

This document defines the prompt intent and task scale gate that future routing rules must apply before selecting a skill chain.

## Core Rule

Before invoking goal planning, execution planning, project memory updates, MCP installation checks, or deep architecture workflows, the agent must classify the user's prompt by intent and task size.

The router must choose the workflow level before choosing the final skill chain.

## Intent Classes

```text
micro-fix
small-change
standard-task
large-task
exploratory-plan
deep-architecture
maintenance-only
```

## Workflow Levels

```text
Lightweight Workflow
Standard Workflow
Deep Workflow
```

## Lightweight Workflow

Use for:

```text
- one small bug;
- one obvious typo or type error;
- one small styling adjustment;
- one isolated component change;
- one local refactor with clear boundaries;
- one direct user request where the target file or surface is obvious.
```

Behavior:

```text
1. Restate the immediate task in one short sentence when useful.
2. Inspect only the affected files, error context, or rendered surface.
3. Make the smallest safe change.
4. Run the smallest relevant verification available.
5. Report what changed and what was checked.
```

Do not create or update:

```text
project/active-goals.md
project/active-plan.md
project/progress-log.md
project/decision-log.md
```

unless the small task reveals a larger hidden scope.

## Standard Workflow

Use for:

```text
- a feature touching multiple files;
- a UI implementation from a spec or screenshot;
- a bug with unclear root cause;
- a refactor that needs a behavior boundary;
- a task that needs more than one implementation slice;
- a task that changes project conventions or reusable patterns.
```

Behavior:

```text
1. Create a compact goal and plan.
2. Use project overlays before broad scans.
3. Execute one slice at a time.
4. Verify each slice.
5. Compare result with the plan before finishing.
6. Update checkpoint files only when the task is genuinely multi-step or resumable.
```

## Deep Workflow

Use for:

```text
- new project creation;
- architecture design;
- stack migration;
- onboarding an unknown project;
- broad visual redesign;
- repeated failures after lightweight or standard attempts;
- large tasks that require stop/resume state.
```

Behavior:

```text
1. Create or update Goal Contract.
2. Create or update Execution Plan.
3. Define context budget and scan boundaries.
4. Check required MCP/tools.
5. Execute small slices.
6. Update progress and decision logs.
7. Leave a precise stop/resume point.
```

## Escalation Rules

Escalate from Lightweight to Standard only when:

```text
- the apparent fix touches multiple unrelated files;
- the bug root cause is unclear after targeted inspection;
- the requested change affects architecture, routing, data flow, state ownership, or shared styling;
- verification shows the first fix is insufficient;
- the user expands the scope.
```

Escalate from Standard to Deep only when:

```text
- the task requires project-wide scanning;
- the work cannot be safely completed in one or two slices;
- the task needs long-lived decisions or stop/resume state;
- the task requires new tooling, package installation, framework migration, or architecture changes.
```

## De-Escalation Rules

De-escalate when the prompt looks large but the actionable scope is narrow.

Examples:

```text
"Fix the dashboard" -> inspect enough to identify the failing surface, then choose Lightweight or Standard.
"Improve this page" with one screenshot and one target file -> Standard, not Deep.
"Make the button color match the screenshot" -> Lightweight.
"Fix this TypeScript error" -> Lightweight unless the error reveals broader type design issues.
```

## Routing Examples

### Small Bug Prompt

```text
User asks for one small bugfix
-> Lightweight Workflow
-> frontend-bugfix-debugger only
-> minimal verification
-> no goal-planner
-> no execution-plan-manager
-> no persistent plan files
```

### Large Feature Prompt

```text
User asks for a multi-file feature
-> Standard Workflow
-> goal-planner compact mode
-> execution-plan-manager compact mode
-> relevant frontend skill
-> verification
```

### Greenfield Or Architecture Prompt

```text
User asks for a new project or architecture plan
-> Deep Workflow
-> goal-planner
-> execution-plan-manager
-> mcp-toolchain-manager when needed
-> architecture or greenfield skill
```

## Future Plan Integration

Future implementation phases must include:

```text
common/prompt-intent-routing-rules.md
```

The first implementation branch should add this policy before adding new system skills, because goal planning and execution planning must not be over-triggered.

## Validation

The future routing policy must prove that:

```text
- narrow prompts do not trigger heavy planning;
- vague or large prompts do not skip planning;
- goal-planner and execution-plan-manager can run in compact mode;
- project checkpoint files are created only when the task is multi-step or resumable;
- the agent can explain why a workflow level was chosen when asked.
```

## Relation To Existing Plan

This document extends `IMPLEMENTATION_PLAN.md`. It preserves the original architecture concept while adding a required first gate: choose task scale before choosing the skill chain.
