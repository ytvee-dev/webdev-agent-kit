---
name: frontend-architecture-planner
description: Use for standard or deep frontend work that needs architecture planning, ownership boundaries, routing/state/data/styling/form/build decisions, migration risk assessment, or implementation handoff. Do not use for micro-fixes, direct isolated edits, or purely visual design direction.
id: 'agents.skills.frontend-architecture-planner.skill'
title: 'Frontend Architecture Planner'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-architecture-planner'
tags:
    - 'agents/skill-package'
    - 'agents/architecture'
    - 'workflow/frontend-architecture'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[common/framework-adaptation-policy|Framework Adaptation Policy]]'
    - '[[common/state-ownership-rules|State Ownership Rules]]'
    - '[[common/routing-boundary-rules|Routing Boundary Rules]]'
    - '[[common/data-fetching-boundary-rules|Data Fetching Boundary Rules]]'
    - '[[common/form-boundary-rules|Form Boundary Rules]]'
    - '[[common/build-tool-boundary-rules|Build Tool Boundary Rules]]'
    - '[[common/frontend-integration-boundaries|Frontend Integration Boundaries]]'
    - '[[skills/goal-planner/SKILL|Goal Planner]]'
    - '[[skills/execution-plan-manager/SKILL|Execution Plan Manager]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Architecture Planner

## Purpose

Plan frontend architecture decisions before implementation when a task affects structure, ownership, routing, state, data flow, styling boundaries, form behavior, build/workspace shape, or long-lived conventions.

This skill creates an architecture decision and implementation handoff. It does not implement code by default.

## When To Use

Use this skill after prompt intent routing when the task is `Standard Workflow` or `Deep Workflow` and architecture decisions matter.

Use this skill when the user asks to:

- plan a new frontend feature that touches multiple modules;
- design a route, screen group, or application section;
- define component boundaries before implementation;
- decide where state should live;
- decide how data fetching should fit the existing project;
- plan routing changes;
- plan form ownership and validation boundaries;
- plan a frontend refactor before editing code;
- assess architecture risk before implementation;
- integrate a feature into an existing frontend stack;
- define a greenfield frontend architecture before scaffolding.

## When Not To Use

Do not use this skill for:

- one small bug;
- one obvious type error;
- one small styling adjustment;
- one direct file-scope edit;
- purely visual direction without architecture impact;
- rendered visual QA;
- UI component library selection;
- testing workflows;
- backend, database, ORM, migrations, or infrastructure work unless the user explicitly changes the scope.

Do not use this skill as a required step for every frontend implementation. Use it only when architecture choices affect the current task.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when workflow level is unclear.
3. Read the compact goal contract or `project/active-goals.md` when present.
4. Read the compact execution plan or `project/active-plan.md` when present.
5. Read common boundary rules relevant to the task:
   - `common/framework-adaptation-policy.md`;
   - `common/state-ownership-rules.md` for state ownership;
   - `common/routing-boundary-rules.md` for routing;
   - `common/data-fetching-boundary-rules.md` for data fetching;
   - `common/form-boundary-rules.md` for forms;
   - `common/build-tool-boundary-rules.md` for build or workspace concerns;
   - `common/frontend-integration-boundaries.md` for auth/data/provider integration.
6. Read only relevant project overlays:
   - `project/stack-profile.md`;
   - `project/architecture-map.md`;
   - `project/styling-profile.md`;
   - `project/verification-profile.md`;
   - `project/docs-profile.md` when present;
   - `project/build-profile.md` when present;
   - `project/workspace-profile.md` when present;
   - `project/state-management-profile.md` when present;
   - `project/data-fetching-profile.md` when present.
7. Read affected source files only when architectural boundaries cannot be planned from overlays.
8. Do not read `README.md` or `SUMMARY.md` during normal runtime.

## Tool Contract

- May use filesystem access to inspect relevant project overlays and affected source files.
- May use `context7` for official current framework and library documentation when architecture depends on framework behavior.
- May use MDN for platform constraints that affect architecture, such as forms, browser APIs, accessibility, and CSS behavior.
- May use `mcp-toolchain-manager` only when required tool capability affects the current architecture planning slice.
- Must not install packages, UI libraries, testing libraries, state libraries, data libraries, form libraries, or MCP servers.
- Must not change project source files, configs, package manager files, or build tooling.
- Must not create tests or testing workflows.
- Must not interact with production systems, secrets, or production data.

## Workflow

1. Confirm architecture scope.
   - If the prompt is lightweight and no architecture boundary is affected, stop and route to the direct skill.
   - If architecture is relevant, continue.

2. State the architectural question.
   Examples:
   - Where should this feature live?
   - Who owns this state?
   - How should the route be structured?
   - Which existing components or layers should be reused?
   - What should remain out of scope?

3. Inspect current conventions.
   Prefer local project facts over generic advice:
   - framework and router;
   - folder/module structure;
   - component ownership;
   - styling system;
   - state ownership;
   - data fetching layer;
   - form conventions;
   - build/workspace shape;
   - verification commands.

4. Define boundaries.
   Define only relevant boundaries:
   - route/page boundary;
   - feature/module boundary;
   - shared vs local component boundary;
   - local vs shared state boundary;
   - data fetching and transformation boundary;
   - form state and validation boundary;
   - styling/token boundary;
   - accessibility and responsive boundary;
   - build/workspace boundary;
   - verification boundary.

5. Choose the smallest architecture that satisfies the goal.
   Avoid new layers, shared abstractions, global stores, packages, and conventions unless the project already uses them or the user explicitly approves them.

6. Identify approval gates.
   Require explicit user approval for:
   - package installation;
   - framework migration;
   - package manager changes;
   - new state/data/form/styling libraries;
   - global architecture layers;
   - build tooling changes;
   - large refactors;
   - destructive file operations;
   - production access.

7. Create the architecture handoff.
   Include files or surfaces likely to change, but do not edit them from this skill.

8. Define verification strategy.
   Use existing project checks and rendered verification where relevant. Do not invent a testing workflow.

9. Hand off.
   Send implementation slices to `execution-plan-manager` or the relevant frontend skill.

## Output Contract

Return or write a Frontend Architecture Plan with:

```text
Goal
Workflow Level
Architecture Question
Current Project Conventions
Proposed Boundaries
Files Or Surfaces Likely To Change
State Ownership
Routing Boundary
Data Fetching Boundary
Form Boundary
Styling Boundary
Build Or Workspace Boundary
Approval Gates
Implementation Slices
Verification Strategy
Risks
Rejected Alternatives
Next Skill Or Next Step
```

Omit irrelevant sections rather than filling them with generic text.

## Validation Gates

Before finishing, verify:

- the task actually needed architecture planning;
- the plan follows current project conventions where known;
- every proposed new boundary has a reason;
- no package, UI library, testing library, or MCP install was proposed as default;
- approval gates are explicit;
- implementation slices are small enough to hand off;
- no source files, configs, package files, or tests were changed by this skill;
- verification strategy uses existing project capabilities or clearly marks gaps.

## Trigger Evals

Should trigger:

- "Plan the frontend architecture for this analytics section."
- "Where should this feature live in the current project?"
- "Design the route and state boundaries before implementation."
- "Plan a safe frontend refactor for this module."
- "Create the architecture plan for a greenfield frontend app, but do not scaffold yet."

Should not trigger:

- "Fix this TypeScript error."
- "Change this button color."
- "Make this page look less generic."
- "Run visual QA."
- "Install shadcn."
- "Create tests."

## Reference Map

- `AGENTS.md` - canonical policy, routing, tool rules, and documentation rules.
- `common/prompt-intent-routing-rules.md` - workflow weight selection and escalation rules.
- `common/framework-adaptation-policy.md` - framework adaptation boundaries.
- `common/state-ownership-rules.md` - state ownership defaults.
- `common/routing-boundary-rules.md` - route ownership and router boundaries.
- `common/data-fetching-boundary-rules.md` - frontend data-fetching boundaries.
- `common/form-boundary-rules.md` - form state and validation boundaries.
- `common/build-tool-boundary-rules.md` - build and workspace boundaries.
- `common/frontend-integration-boundaries.md` - auth/data/provider integration boundaries.
- `skills/goal-planner/SKILL.md` - goal contract for standard or deep work.
- `skills/execution-plan-manager/SKILL.md` - task slicing and stop/resume planning.
- `project/architecture-map.md` - local-only current architecture map.
- `project/stack-profile.md` - local-only framework and tooling facts.
- `project/styling-profile.md` - local-only styling conventions.
- `project/verification-profile.md` - local-only verification commands.
