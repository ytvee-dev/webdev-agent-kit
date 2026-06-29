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

WebDev Assistant targets only React, Next.js, CSS Modules, Redux, TanStack, and Axios.

Do not present unrelated frontend frameworks, UI libraries, app generators, styling systems, or testing workflows as supported defaults. If a host project is outside the target stack, report the unsupported scope instead of adapting this bundle to it.

## Runtime Source Model

- `AGENTS.md` is the canonical publishable policy file for agent runtime.
- `skills/**` contains executable skill instructions.
- `common/**` contains reusable runtime rules.
- `templates/**` contains optional local artifact templates.
- `project/**` contains host-project facts and stays local-only.
- `README.md` is a human-facing repository description and usage guide only. Do not read it during normal agent runtime unless the user explicitly asks for README work.
- `dist/**` is generated distribution output. Do not use it as source-of-truth during ordinary source editing or runtime routing.
- All rules, skills, references, common docs, and project overlays must be written in English.

## Natural Language Commands

When the user says `адаптируйся`, `адаптируйся к проекту`, `адаптируй этот skill pack к проекту`, `инициализируй .agents`, or asks to initialize this bundle in the current repo, classify the task as `project-onboarding` and route to `project-onboarding-adapter`.

If the project already has `.agents/project/**` overlays and the user asks only to refresh stale paths, cached facts, commands, MCP state, or indexes, classify the task as `project-context-refresh` and route to `project-context-adapter`.

The adaptation command must not create app source files. It may create or update the host-root pointer and `.agents/project/**` overlays. Missing MCP installation must be reported with official sources and requires explicit approval before installation or config changes.

## Prompt Intake And Task Classification

The user may write a natural-language task without naming a skill. Before reading task-specific files, classify the task and choose the minimal context needed to solve it.

Classify every task as one or more of:

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

Before selecting the final skill chain, classify the prompt by workflow weight: `Lightweight Workflow`, `Standard Workflow`, or `Deep Workflow`.

Read `common/prompt-intent-routing-rules.md` when the prompt could be confused between a narrow task and a larger multi-step task.

Use `Lightweight Workflow` for one small bug, one obvious typo or type error, one small styling adjustment, one isolated component change, or one direct request where the affected file, component, route, or error context is obvious. Do not invoke `goal-planner`, `execution-plan-manager`, broad scans, MCP installation checks, or persistent project plan files for lightweight tasks unless targeted inspection proves the scope is larger than it first appeared.

Use `Standard Workflow` for multi-file features, screenshot/spec UI work, unclear bug root causes, refactors with behavior boundaries, or tasks that need more than one implementation slice. Standard tasks may use compact planning.

Use `Deep Workflow` only for new project creation, architecture design, stack migration, onboarding an unknown project, broad redesign, repeated failures, or large work that needs durable stop/resume state.

After task and scale classification:

1. Read this `AGENTS.md`.
2. Read `common/target-stack-policy.md` when stack scope matters.
3. Select relevant skills from the skill metadata and the skill map below. The user must not need to name a skill.
4. Read only selected `skills/**/SKILL.md` files.
5. Read only references named by the selected skill workflow and needed for the current task.
6. Read only relevant `common/**`, `project/**`, source files, configs, official docs, or external sources needed for the classified task.
7. If no repo-local skill matches, handle the task with base Codex behavior and read only relevant project context.

Do not read all skills, all references, all common docs, all overlays, `README.md`, or `dist/**` for routing. Progressive disclosure is required.

## Skill Map

- Standard or deep frontend work that needs a clear user goal, scope, constraints, and done criteria before implementation -> `goal-planner`.
- Standard or deep frontend work that needs task slices, context budget, checkpoint rules, or stop/resume state after the goal is defined -> `execution-plan-manager`.
- MCP/tool capability detection, missing-tool reporting, official install source verification, approval-gated installation planning, or `project/mcp-profile.md` updates -> `mcp-toolchain-manager`.
- Standard or deep UI work that needs visual direction, redesign, visual polish, design critique, anti-template checks, or design handoff before implementation -> `frontend-design-director`.
- Standard or deep React/Next.js work that needs architecture planning, ownership boundaries, routing/state/data/styling/form/build decisions, migration risk assessment, or implementation handoff -> `frontend-architecture-planner`.
- Deep React or Next.js work that starts a new project, plans an empty repository, or defines the first vertical slice from a product idea before any scaffold -> `greenfield-project-builder`.
- Code-changing frontend work that needs lint verification, or explicit user-requested lint setup -> `frontend-linter-manager`.
- Evidence-first frontend bugfixes, unclear UI/runtime errors, broken routes, styling regressions, hydration/client issues, and small defects that need reproduction before code changes -> `frontend-bugfix-debugger`.
- Behavior-preserving frontend refactors with clear boundaries, including component extraction, file reorganization, prop/interface cleanup, state simplification, and TypeScript tightening -> `frontend-refactor-surgeon`.
- Evidence-backed frontend quality review of code, UI implementation, architecture boundaries, TypeScript, security, performance, verification, and anti-slop concerns -> `frontend-quality-reviewer`.
- Screenshot or copied visual inspect material to implementation spec -> `design-screenshot-spec`.
- React/Next.js implementation from a `Design Implementation Spec`, Design Direction Contract, Frontend Architecture Plan, or Greenfield Project Plan -> `frontend-layout-implementer`.
- Rendered UI verification, browser screenshots, and visual diff review -> `frontend-visual-qa`.
- Project onboarding, root pointer creation, target-stack detection, docs/MCP selection, and `project/**` cache creation -> `project-onboarding-adapter`.
- Refresh factual project overlays and path indexes -> `project-context-adapter`.
- Skill authoring and bundle rule maintenance -> `agent-rules-skill-author`.

Use the screenshot-to-code pipeline in order:

```text
design-screenshot-spec
-> frontend-design-director when visual judgment is needed
-> frontend-architecture-planner when architecture boundaries matter
-> frontend-layout-implementer
-> frontend-linter-manager when code changed and lint is available
-> frontend-visual-qa
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

Use `mcp-toolchain-manager` before a selected skill only when tool capability affects the current slice or the user asks for MCP/tool setup, audit, or troubleshooting. Do not use it as a mandatory step for every task.

For code-changing tasks, run the smallest relevant existing lint command before final reporting. If no lint command exists, report that lint was not run. If the user asks for lint setup, use `frontend-linter-manager` and require explicit approval before dependency, script, or config changes.

For frontend bugfixes, start from `frontend-bugfix-debugger` unless the cause and file-scope fix are already obvious. For behavior-preserving refactors, use `frontend-refactor-surgeon` and preserve behavior unless the user explicitly approves a change. Use `frontend-quality-reviewer` for review requests and significant frontend implementation quality passes; review findings do not authorize broad rewrites by themselves.

Do not insert `goal-planner`, `execution-plan-manager`, `mcp-toolchain-manager`, `frontend-design-director`, `frontend-architecture-planner`, or `greenfield-project-builder` into lightweight workflows unless the task escalates or the user directly asks for that concern.

## Figma Boundary

- Do not use Figma MCP tools for this bundle's design intake or implementation flow.
- Do not open Figma URLs, inspect live Figma files, write Figma canvas nodes, create Figma files, use Figma whiteboard, create Figma design systems, or register Code Connect mappings.
- Treat only user-supplied screenshots, copied inspect panels, exported assets, written notes, and current repository code as source material.
- If the user provides only a Figma URL, file key, node id, or Figma whiteboard reference, ask for screenshots, exports, copied inspect values, assets, or a written brief before continuing.

## Tool Policy

- Prefer configured MCP tools over broad guessing when the needed server is available.
- Use Project Context, Design Spec, Visual Reference, and Visual Diff MCP servers when they are installed in the current session.
- Use `context7` for current React, Next.js, Redux, TanStack, Axios, TypeScript, or build-tool documentation when needed.
- Use `mdn` for current HTML, CSS, Web API, and browser compatibility facts.
- Use Browser or Playwright MCP for rendered UI verification.
- When Browser or Playwright MCP is already available in the session, use it for rendered UI verification without asking the user for extra confirmation. This does not override explicit approval requirements for installing missing MCP servers, starting commands that require approval, package installs, destructive actions, or production-system access.
- If a named MCP server required by the active skill is unavailable, report the missing capability before using a fallback. Use fallback only when the skill allows it or the user explicitly accepts it.
- During project onboarding, scan current `skills/*/agents/openai.yaml` files for declared MCP dependencies and cache required, available, missing, optional, approved, installed, skipped, or blocked capabilities in `project/mcp-profile.md`.
- Install missing MCP servers only after explicit user approval and only when the official install source has been verified.
- Never use Figma MCP as a fallback in this bundle.

## Frontend Implementation Rules

- Detect whether the task is within React, Next.js, CSS Modules, Redux, TanStack, or Axios before applying stack-specific rules.
- Reuse existing React components, Next.js routes, CSS Modules, Redux slices, TanStack conventions, Axios clients, tokens, layout patterns, and verification commands before introducing new ones.
- Do not add packages, styling systems, global tokens, generated scaffolds, architecture layers, UI libraries, or testing workflows without explicit user approval.
- During new or empty project onboarding, do not create app source files, framework configs, package manifests, routes, components, styles, tests, or build scripts. Create only the host-root pointer and local-only `project/**` overlays from inferred or user-provided intended stack facts.
- Keep edits scoped to the requested screen, component, route, or static page.
- Preserve accessibility, focus states, responsive behavior, text wrapping, and stable layout dimensions.
- Do not interact with production systems, production data, or live production environments.

## Documentation Rules

- Keep reusable instructions in `common/**` or `skills/**`.
- Keep host-project facts in `project/**`.
- Keep MCP and official documentation capability facts in `project/mcp-profile.md`.
- Keep screenshot, exported asset, copied inspect, and design-reference boundaries in `project/design-reference-profile.md`.
- Keep every Markdown file in this bundle graph-linkable with YAML frontmatter: `id`, `title`, `doc_type`, `layer`, `status`, `publishable`, `local_only`, `tags`, `parent`, `related`, and `depends_on`.
- In `SKILL.md`, keep `name` and `description` first, followed by graph metadata.
- Update `README.md` only for human-facing repository documentation changes, not for agent runtime routing or context. Agents may read or edit it only when the user explicitly asks for README work.
- Do not publish or copy `project/**` facts into reusable bundle docs.

## Verification

For skill and documentation changes:

1. Validate changed skills with `python skills/agent-rules-skill-author/scripts/validate_agent_skill.py skills/<skill-name>` when available.
2. Search for stale deleted skill names and prohibited Figma/Jam routing.
3. Search changed rules and overlays for non-English rule text.
4. Check that `README.md`, `plugin.json`, and actual `skills/**` directories agree only for human-facing documentation changes; do not use `README.md` as runtime context.
5. Run Markdown formatting checks when available.
