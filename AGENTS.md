---
id: 'agents.agents'
title: 'AGENTS.md'
doc_type: 'policy'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/policy'
    - 'docs/entrypoint'
parent: []
related:
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[common/skill-applicability-policy|Skill Applicability Policy]]'
    - '[[common/rendered-visual-verification-policy|Rendered Visual Verification Policy]]'
    - '[[common/lightweight-routing-policy|Lightweight Routing Policy]]'
    - '[[common/documentation-maintenance|Documentation Maintenance]]'
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[common/approved-patterns|Approved Patterns]]'
    - '[[common/anti-patterns|Common Anti-Patterns]]'
    - '[[common/design-quality-rubric|Design Quality Rubric]]'
    - '[[common/anti-template-defaults|Anti-Template Defaults]]'
    - '[[common/interface-copy-rules|Interface Copy Rules]]'
    - '[[common/motion-rules|Motion Rules]]'
    - '[[common/agent-operating-model|Agent Operating Model]]'
    - '[[common/framework-adaptation-policy|Framework Adaptation Policy]]'
    - '[[common/typescript-discipline|TypeScript Discipline]]'
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
depends_on: []
---

# AGENTS.md

This is the canonical runtime policy entrypoint for this `.agents` bundle. Paths are bundle-local paths rooted at `.agents` itself, such as `AGENTS.md`, `skills/**`, `common/**`, and `project/**`.

The host repository root `AGENTS.md` is managed only by `project-onboarding-adapter`. Do not edit or mirror the host-root pointer during ordinary bundle skill work.

## Target Stack

WebDev Assistant targets React, Next.js, CSS Modules, Redux, TanStack, and Axios for stack-specific implementation, architecture, greenfield, state, data, and styling guidance.

Do not present unrelated frontend frameworks, UI libraries, app generators, styling systems, or testing workflows as supported defaults. If the host project is outside the target stack, distinguish unsupported stack-specific work from framework-agnostic bundle skills. Read `common/skill-applicability-policy.md` before deciding that no skill applies.

Non-target frontend projects may still use design intake, visual direction, rendered visual QA, frontend quality review, existing lint verification, planning, MCP, project context, onboarding, and skill-authoring workflows when their triggers match. Do not apply React, Next.js, CSS Modules, Redux, TanStack, or Axios implementation rules to those projects by default.

## Runtime Source Model

- `AGENTS.md` is the canonical publishable policy file for agent runtime.
- `skills/**` contains executable skill instructions.
- `common/**` contains reusable runtime rules.
- `templates/**` contains optional local artifact templates.
- `project/**` contains host-project facts and stays local-only.
- `README.md` is a human-facing repository description and usage guide only.
- `dist/**` is generated distribution output and must not be used as source of truth.
- All rules, skills, references, common docs, and project overlays must be written in English.

## Natural Language Commands

When the user says `адаптируйся`, `адаптируйся к проекту`, `адаптируй этот skill pack к проекту`, `инициализируй .agents`, or asks to initialize this bundle in the current repo, classify the task as `project-onboarding` and route to `project-onboarding-adapter`.

If the project already has `.agents/project/**` overlays and the user asks only to refresh stale paths, cached facts, commands, MCP state, or indexes, classify the task as `project-context-refresh` and route to `project-context-adapter`.

The adaptation command may create or update the host-root pointer and `.agents/project/**` overlays. It must not create app source files.

## Prompt Intake And Task Classification

Before reading task-specific files, classify the task and choose the minimal context needed to solve it.

Classify every task as one or more of:

- `lookup-only`
- `explanation-only`
- `bugfix`
- `refactor`
- `project-audit`
- `optimization`
- `feature/development`
- `documentation`
- `skill-documentation-refactor`
- `design-spec`
- `design-direction`
- `frontend-layout`
- `frontend-architecture`
- `greenfield-project`
- `lint-verification`
- `visual-qa`
- `project-onboarding`
- `project-context-refresh`
- `planning/architecture`
- `goal-planning`
- `execution-planning`
- `mcp-tooling`
- `brainstorm/conversation`
- `internet-research`
- `other`

## Prompt Intent And Task Scale Gate

Before selecting the final skill chain, classify the prompt by workflow weight: `Fast Lookup`, `Lightweight Workflow`, `Standard Workflow`, or `Deep Workflow`.

Read `common/prompt-intent-routing-rules.md` when the prompt could be confused between a narrow task and a larger multi-step task.

Use `Fast Lookup` for narrow questions, file lookup, code explanation, locating related files, and inspecting how a small function, selector, route, style, or config works. Read `common/lightweight-routing-policy.md` for this path. Do not load task skills, references, planning skills, MCP profiles, visual QA, quality review, onboarding, or validation checklists unless targeted inspection proves escalation is required.

Use `Lightweight Workflow` for one small bug, obvious typo or type error, small styling adjustment, isolated component change, or direct request with obvious affected scope.

Use `Standard Workflow` for multi-file features, screenshot/spec UI work, unclear bug root causes, refactors with behavior boundaries, or tasks that need more than one implementation slice.

Use `Deep Workflow` only for new project creation, architecture design, stack migration, onboarding an unknown project, broad redesign, repeated failures, or large work that needs durable stop/resume state.

After task and scale classification:

1. Read this `AGENTS.md`.
2. If the task is `Fast Lookup`, read `common/lightweight-routing-policy.md`, search narrowly, inspect only the top relevant files or snippets, answer, and stop unless escalation is justified.
3. Read `common/target-stack-policy.md` when stack scope matters.
4. Read `common/skill-applicability-policy.md` when the project is outside the target stack or the task can be solved by design, QA, review, lint, planning, MCP, onboarding, context, or skill-authoring without stack-specific implementation rules.
5. Select relevant skills from the skill metadata and the skill map below. The user must not need to name a skill.
6. Read only selected `skills/**/SKILL.md` files.
7. Read only references and project files needed for the classified task.
8. If no repo-local skill matches, handle the task with base Codex behavior and relevant project context.

Do not read all skills, all references, all common docs, all overlays, `README.md`, or `dist/**` for routing.

## Skill Map

- Narrow lookup, code explanation, file location, and small inspection that do not need file changes -> `Fast Lookup` with `common/lightweight-routing-policy.md`, no task skill chain unless escalation is justified.
- Standard or deep frontend work that needs a clear user goal, scope, constraints, and done criteria before implementation -> `goal-planner`.
- Standard or deep frontend work that needs task slices, context budget, checkpoint rules, or stop/resume state after the goal is defined -> `execution-plan-manager`.
- MCP/tool capability detection, missing-tool reporting, official install source verification, approval-gated installation planning, or `project/mcp-profile.md` updates -> `mcp-toolchain-manager`.
- Standard or deep UI work that needs visual direction, redesign, visual polish, design critique, anti-template checks, or design handoff before implementation -> `frontend-design-director`.
- Standard or deep React/Next.js work that needs architecture planning, ownership boundaries, routing/state/data/styling/form/build decisions, migration risk assessment, or implementation handoff -> `frontend-architecture-planner`.
- Deep React or Next.js work that starts a new project, plans an empty repository, or defines the first vertical slice from a product idea before any scaffold -> `greenfield-project-builder`.
- Code-changing frontend work that needs lint verification, or explicit user-requested lint setup -> `frontend-linter-manager`.
- Evidence-first frontend bugfixes inside the target stack -> `frontend-bugfix-debugger`.
- Behavior-preserving frontend refactors inside the target stack -> `frontend-refactor-surgeon`.
- Evidence-backed frontend quality review of code, UI implementation, architecture boundaries, TypeScript, security, performance, verification, and anti-slop concerns -> `frontend-quality-reviewer`.
- Screenshot or copied visual inspect material to implementation spec, including for non-target frontend projects -> `design-screenshot-spec`.
- React/Next.js implementation from a `Design Implementation Spec`, Design Direction Contract, Frontend Architecture Plan, or Greenfield Project Plan -> `frontend-layout-implementer`.
- Rendered UI verification, browser screenshots, and visual diff review, including for non-target frontend projects -> `frontend-visual-qa`.
- Project onboarding, root pointer creation, target-stack detection, limited non-target frontend applicability notes, docs/MCP selection, and `project/**` cache creation -> `project-onboarding-adapter`.
- Refresh factual project overlays and path indexes -> `project-context-adapter`.
- Skill authoring and bundle rule maintenance -> `agent-rules-skill-author`.

Use the target-stack screenshot pipeline in order:

```text
design-screenshot-spec
-> frontend-design-director when visual judgment is needed
-> frontend-architecture-planner when architecture boundaries matter
-> frontend-layout-implementer
-> frontend-linter-manager when code changed and lint is available
-> frontend-visual-qa
-> frontend-quality-reviewer when quality review is requested or appropriate
```

Use the framework-agnostic screenshot pipeline in non-target frontend projects:

```text
design-screenshot-spec
-> frontend-design-director when visual judgment is needed
-> base Codex implementation using inspected local project conventions
-> frontend-linter-manager when code changed and an existing lint command is available
-> frontend-visual-qa when a local app and browser tooling are available
-> frontend-quality-reviewer when quality review is requested or appropriate
```

For new or empty React/Next.js projects, use the greenfield flow before any scaffold:

```text
goal-planner
-> execution-plan-manager
-> greenfield-project-builder
-> frontend-architecture-planner when architecture boundaries need deeper planning
-> project-onboarding-adapter for pointer and local-only overlays
```

For code-changing tasks, run the smallest relevant existing lint command before final reporting. If no lint command exists, report that lint was not run. If the user asks for lint setup, use `frontend-linter-manager` and require explicit approval before dependency, script, or config changes.

Do not insert planning, MCP, design direction, architecture, or greenfield skills into lightweight workflows unless the task escalates or the user directly asks for that concern.

## Figma Boundary

- Do not use Figma MCP tools for this bundle's design intake or implementation flow.
- Treat only user-supplied screenshots, copied inspect panels, exported assets, written notes, and current repository code as source material.
- If the user provides only a Figma URL, file key, node id, or Figma whiteboard reference, ask for screenshots, exports, copied inspect values, assets, or a written brief before continuing.

## Tool Policy

- Prefer configured MCP tools over broad guessing when the needed server is available.
- Use `context7` for current React, Next.js, Redux, TanStack, Axios, TypeScript, or build-tool documentation when needed.
- Use `mdn` for current HTML, CSS, Web API, and browser compatibility facts.
- Use Browser or Playwright MCP only for rendered visual QA tasks allowed by `common/rendered-visual-verification-policy.md`.
- Do not use Browser or Playwright MCP for font, token, color, spacing, or CSS-variable lookup when source files, copied inspect values, or specs can answer the question.
- A running local app or installed Playwright dependency does not mean Browser or Playwright MCP is available.
- Install missing MCP servers only after explicit user approval and only when the official install source has been verified.
- Never use Figma MCP as a fallback in this bundle.

## Frontend Implementation Rules

- Detect whether the task is within React, Next.js, CSS Modules, Redux, TanStack, or Axios before applying stack-specific rules.
- When the project is outside the target stack, do not suppress framework-agnostic skills that match the user request; use base Codex behavior for source edits and apply only local project conventions plus browser-platform rules.
- Reuse existing project components, routes, styles, data boundaries, tokens, layout patterns, and verification commands before introducing new ones.
- Apply component decomposition rules regardless of framework, router, state layer, data layer, or styling system.
- Do not add packages, styling systems, global tokens, generated scaffolds, architecture layers, UI libraries, or testing workflows without explicit user approval.
- Keep edits scoped to the requested screen, component, route, or static page.
- Preserve accessibility, focus states, responsive behavior, text wrapping, and stable layout dimensions.

## Documentation Rules

- Keep reusable instructions in `common/**` or `skills/**`.
- Keep host-project facts in `project/**`.
- Keep MCP and official documentation capability facts in `project/mcp-profile.md`.
- Keep screenshot, exported asset, copied inspect, and design-reference boundaries in `project/design-reference-profile.md`.
- Keep every Markdown file in this bundle graph-linkable with YAML frontmatter.
- In `SKILL.md`, keep `name` and `description` first, followed by graph metadata.
- Update `README.md` only for human-facing repository documentation changes.
- Do not publish or copy `project/**` facts into reusable bundle docs.

## Verification

For skill and documentation changes:

1. Validate changed skills with `python skills/agent-rules-skill-author/scripts/validate_agent_skill.py skills/<skill-name>` when available.
2. Search for stale deleted skill names and prohibited Figma/Jam routing.
3. Search changed rules and overlays for non-English rule text.
4. Check that human-facing docs and actual `skills/**` directories agree only when those docs changed.
5. Run Markdown formatting checks when available.
