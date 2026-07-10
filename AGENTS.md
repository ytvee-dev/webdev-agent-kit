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
    - '[[common/policy-precedence|Policy Precedence]]'
    - '[[common/core/runtime-core-policy|Portable Runtime Core Policy]]'
    - '[[profiles/react-typescript/PROFILE|React TypeScript Profile]]'
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
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
    - '[[common/ui-ux-priority-checklist|UI UX Priority Checklist]]'
    - '[[common/css-modules-specificity-rules|CSS Modules Specificity Rules]]'
    - '[[common/form-feedback-rules|Form Feedback Rules]]'
    - '[[common/navigation-ux-rules|Navigation UX Rules]]'
    - '[[common/data-visualization-rules|Data Visualization Rules]]'
    - '[[common/icon-quality-rules|Icon Quality Rules]]'
    - '[[common/mobile-responsive-rules|Mobile Responsive Rules]]'
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/stop-criteria-rules|Stop Criteria Rules]]'
    - '[[common/bounded-retry-rules|Bounded Retry Rules]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
    - '[[common/windows-shell-sandbox-rules|Windows Shell Sandbox Rules]]'
    - '[[common/context-compaction-rules|Context Compaction Rules]]'
    - '[[common/independent-review-rules|Independent Review Rules]]'
    - '[[common/worktree-parallelism-rules|Worktree Parallelism Rules]]'
    - '[[common/agent-operating-model|Agent Operating Model]]'
    - '[[common/framework-adaptation-policy|Framework Adaptation Policy]]'
    - '[[common/typescript-discipline|TypeScript Discipline]]'
    - '[[skills/frontend-design-intelligence/SKILL|Frontend Design Intelligence]]'
    - '[[skills/loop-workflow-planner/SKILL|Loop Workflow Planner]]'
    - '[[skills/greenfield-project-builder/SKILL|Greenfield Project Builder]]'
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
depends_on: []
---

# AGENTS.md

This is the canonical runtime policy entrypoint for this `.agents` bundle. Paths are bundle-local paths rooted at `.agents` itself, such as `AGENTS.md`, `common/**`, `profiles/**`, `adapters/**`, `skills/**`, and `project/**`.

The host repository root `AGENTS.md` is managed only by `project-onboarding-adapter`. Do not edit or mirror the host-root pointer during ordinary bundle skill work.

## Runtime Policy Layers

Load only the layers needed for the current task:

1. `common/core/runtime-core-policy.md` for client-neutral authority, safety, evidence, execution, verification, and concise output.
2. The single matching file under `adapters/` for client discovery, native pointers, tool registry, sandbox, and configuration differences.
3. `profiles/react-typescript/PROFILE.md` only when repository evidence confirms that the target-stack defaults apply.
4. Local project conventions and verified `project/**` facts for the affected surface.
5. The smallest matching skill and only its required references.

This is context loading order, not instruction authority. Resolve conflicts through `common/policy-precedence.md`; do not duplicate its ordered contract inside skills. Generated targets ship only their matching adapter, and aliases reuse the canonical adapter.

## Target Stack

The default target stack is declared by `profiles/react-typescript/PROFILE.md`. Activate it from repository evidence, then load only the owning policies needed by the changed surface. Use `common/skill-applicability-policy.md` for framework-agnostic work outside that profile.

## Runtime Source Model

- `AGENTS.md` is the canonical publishable policy file for agent runtime.
- `common/core/**` contains the portable client-neutral runtime contract.
- `profiles/**` contains evidence-gated project and stack defaults.
- `adapters/**` contains only client discovery, entrypoint, tool, sandbox, and configuration differences.
- `skills/**` contains executable skill instructions.
- `common/**` contains reusable runtime rules.
- `templates/**` contains optional local artifact templates.
- `project/**` contains host-project facts and stays local-only.
- `README.md` is a human-facing repository description and usage guide only. It is not runtime context, not a routing source, not a policy source, not a skill inventory source, and not a validation source for agents.
- `dist/**` is generated distribution output and must not be used as source of truth.
- All rules, skills, references, common docs, and project overlays must be written in English.

## README Runtime Boundary

Agents must never read `README.md` under any circumstance.

- Do not open, search, summarize, cite, route from, validate from, or treat `README.md` as context.
- Do not use `README.md` for task classification, skill selection, onboarding, project context refresh, bundle maintenance, verification, source inventory, or generated-target validation.
- Use `AGENTS.md`, `bundle-manifest.json`, `common/core/**`, `profiles/**`, `adapters/**`, `skills/**`, `common/**`, `templates/**`, and local-only `project/**` overlays as the available source model instead.
- If a user asks about README content, ask the user to paste the relevant excerpt or desired replacement text. Do not inspect `README.md`.
- If a human-facing README change is needed, propose the text in the final response for a human maintainer to apply. Do not autonomously read or edit `README.md`.

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
- `design-intelligence`
- `design-direction`
- `frontend-layout`
- `frontend-architecture`
- `greenfield-project`
- `lint-verification`
- `visual-qa`
- `agent-loop`
- `loop-planning`
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

Use `Fast Lookup` for narrow questions, file lookup, code explanation, locating related files, and inspecting how a small function, selector, route, style, or config works. Read `common/lightweight-routing-policy.md` for this path. Do not load task skills, references, planning skills, loop workflow planning, MCP profiles, visual QA, quality review, onboarding, or validation checklists unless targeted inspection proves escalation is required.

Use `Lightweight Workflow` for one small bug, obvious typo or type error, small styling adjustment, isolated component change, or direct request with obvious affected scope.

Use `Standard Workflow` for multi-file features, screenshot/spec UI work, unclear bug root causes, refactors with behavior boundaries, tasks that need more than one implementation slice, or tasks that require bounded retry against measurable verification.

Use `Deep Workflow` only for new project creation, architecture design, stack migration, onboarding an unknown project, broad redesign, repeated failures, parallel experiments, or large work that needs durable stop/resume state.

After task and scale classification:

1. Read this `AGENTS.md` and `common/core/runtime-core-policy.md`.
2. Read the matching generated adapter when client behavior affects the task.
3. If the task is `Fast Lookup`, read `common/lightweight-routing-policy.md`, search narrowly, inspect only the top relevant files or snippets, answer, and stop unless escalation is justified.
4. Read `profiles/react-typescript/PROFILE.md` only when target-stack evidence exists, then load only relevant owning policies.
5. Read `common/skill-applicability-policy.md` when the project is outside the target stack or the task can be solved by framework-agnostic workflows.
6. Select relevant skills from the skill metadata and the skill map below. The user must not need to name a skill.
7. Read only selected `skills/**/SKILL.md` files and required references.
8. If no repo-local skill matches, use the host agent's base behavior with relevant project context and the portable core.

Do not read all skills, all references, all common docs, all overlays, `README.md`, or `dist/**` for routing. Never read `README.md` for any non-routing task either.

## Skill Map

- Narrow lookup, code explanation, file location, and small inspection that do not need file changes -> `Fast Lookup` with `common/lightweight-routing-policy.md`, no task skill chain unless escalation is justified.
- Standard or deep frontend work that needs a clear user goal, scope, constraints, and done criteria before implementation -> `goal-planner`.
- Standard or deep frontend work that needs task slices, context budget, checkpoint rules, or stop/resume state after the goal is defined -> `execution-plan-manager`.
- Standard or deep work that must iterate until measurable acceptance criteria pass, repair verification failures, use bounded retry, preserve loop memory, or separate implementation from final judgment -> `loop-workflow-planner`.
- MCP/tool capability detection, missing-tool reporting, official install source verification, approval-gated installation planning, or `project/mcp-profile.md` updates -> `mcp-toolchain-manager`.
- Standard or deep UI work that needs product category, page pattern, design dials, domain UX risks, or product-specific anti-pattern grounding before visual direction -> `frontend-design-intelligence`.
- Standard or deep UI work that needs visual direction, redesign, visual polish, design critique, anti-template checks, or design handoff before implementation -> `frontend-design-director`.
- Standard or deep React/Next.js work that needs architecture planning, ownership boundaries, routing/state/data/styling/form/build decisions, migration risk assessment, or implementation handoff -> `frontend-architecture-planner`.
- Deep React or Next.js work that starts a new project, plans an empty repository, or defines the first vertical slice from a product idea before any scaffold -> `greenfield-project-builder`.
- Code-changing frontend work that needs lint verification, or explicit user-requested lint setup -> `frontend-linter-manager`.
- Evidence-first frontend bugfixes inside the target stack -> `frontend-bugfix-debugger`.
- Behavior-preserving frontend refactors inside the target stack -> `frontend-refactor-surgeon`.
- Evidence-backed frontend quality review of code, UI implementation, architecture boundaries, TypeScript, security, performance, UX gates, verification, and anti-slop concerns -> `frontend-quality-reviewer`.
- Screenshot or copied visual inspect material to implementation spec, including for non-target frontend projects -> `design-screenshot-spec`.
- React/Next.js implementation from a `Design Implementation Spec`, Design Direction Contract, Frontend Architecture Plan, or Greenfield Project Plan -> `frontend-layout-implementer`.
- Rendered UI verification, browser screenshots, and visual diff review, including for non-target frontend projects -> `frontend-visual-qa`.
- Project onboarding, root pointer creation, target-stack detection, limited non-target frontend applicability notes, docs/MCP selection, and `project/**` cache creation -> `project-onboarding-adapter`.
- Refresh factual project overlays and path indexes -> `project-context-adapter`.
- Skill authoring and bundle rule maintenance -> `agent-rules-skill-author`.

Use the target-stack screenshot pipeline in order:

```text
design-screenshot-spec
-> frontend-design-intelligence when product/page pattern or design dials need grounding
-> frontend-design-director when visual judgment is needed
-> frontend-architecture-planner when architecture boundaries matter
-> loop-workflow-planner when bounded retry or measurable iteration is required
-> frontend-layout-implementer
-> frontend-linter-manager when code changed and lint is available
-> frontend-visual-qa
-> frontend-quality-reviewer when quality review is requested or required by the loop contract
```

Use the framework-agnostic screenshot pipeline in non-target frontend projects:

```text
design-screenshot-spec
-> frontend-design-intelligence when product/page pattern or design dials need grounding
-> frontend-design-director when visual judgment is needed
-> loop-workflow-planner when bounded retry or measurable iteration is required
-> base agent implementation using inspected local project conventions
-> frontend-linter-manager when code changed and an existing lint command is available
-> frontend-visual-qa when a local app and browser tooling are available
-> frontend-quality-reviewer when quality review is requested or required by the loop contract
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

For iterative tasks, use `common/agent-loop-policy.md`. A loop must have measurable acceptance criteria, an attempt limit, stop conditions, and final evidence. Do not require Claude-only commands such as `/goal`, `/loop`, or `/schedule`; map the same Loop Workflow Contract to the host platform when available.

Do not insert planning, MCP, design direction, architecture, design intelligence, loop workflow planning, or greenfield skills into lightweight workflows unless the task escalates, repeated failure appears, measurable iteration is explicitly requested, or the user directly asks for that concern.

## Figma Boundary

- Do not use Figma MCP tools for this bundle's design intake or implementation flow.
- Treat only user-supplied screenshots, copied inspect panels, exported assets, written notes, and current repository code as source material.
- If the user provides only a Figma URL, file key, node id, or Figma whiteboard reference, ask for screenshots, exports, copied inspect values, assets, or a written brief before continuing.

## Tool Policy

- Prefer configured MCP tools over broad guessing when the needed server is available.
- Use `context7` for current React, Next.js, Redux, TanStack, Axios, TypeScript, or build-tool documentation when needed.
- Use `mdn` for current HTML, CSS, Web API, and browser compatibility facts.
- Use Browser or Playwright MCP only for rendered visual QA tasks allowed by `common/rendered-visual-verification-policy.md`.
- Read `common/windows-shell-sandbox-rules.md` before retrying npm, build, dev-server, browser, Vite, esbuild, SWC, or Playwright commands that fail with Windows shell policy or sandbox access errors.
- Do not use Browser or Playwright MCP for font, token, color, spacing, or CSS-variable lookup when source files, copied inspect values, or specs can answer the question.
- A running local app or installed Playwright dependency does not mean Browser or Playwright MCP is available.
- Install missing MCP servers only after explicit user approval and only when the official install source has been verified.
- Never use Figma MCP as a fallback in this bundle.

## Frontend Implementation Rules

- Detect whether the task is within React, Next.js, CSS Modules, Redux, TanStack, or Axios before applying stack-specific rules.
- When the project is outside the target stack, do not suppress framework-agnostic skills that match the user request; use the host agent's base behavior for source edits and apply only local project conventions plus browser-platform rules.
- Reuse existing project components, routes, styles, data boundaries, tokens, layout patterns, and verification commands before introducing new ones.
- Apply component decomposition rules regardless of framework, router, state layer, data layer, or styling system.
- Apply CSS Modules specificity rules when CSS Modules are changed.
- Apply conditional UX gates for forms, navigation, data visualization, icons, and mobile responsive behavior when those surfaces are touched.
- Use bounded verification loops only when acceptance criteria, retry limit, and stop conditions are defined.
- Do not add packages, styling systems, global tokens, generated scaffolds, architecture layers, UI libraries, or testing workflows without explicit user approval.
- Keep edits scoped to the requested screen, component, route, or static page.
- Preserve accessibility, focus states, responsive behavior, text wrapping, and stable layout dimensions.

## Documentation Rules

- Keep portable behavior in `common/core/**`, project defaults in `profiles/**`, client differences in `adapters/**`, and reusable procedures in `common/**` or `skills/**`.
- Keep host-project facts in `project/**`.
- Keep loop memory and verified loop learnings in local-only `project/**` files.
- Keep MCP and official documentation capability facts in `project/mcp-profile.md`.
- Keep screenshot, exported asset, copied inspect, and design-reference boundaries in `project/design-reference-profile.md`.
- Keep every runtime Markdown file in this bundle graph-linkable with YAML frontmatter. `README.md` is excluded because it is human-only.
- In `SKILL.md`, keep `name` and `description` first, followed by graph metadata.
- Do not read or autonomously update `README.md`. Propose human-facing README text to the user instead.
- Do not publish or copy `project/**` facts into reusable bundle docs.

## Verification

For skill and documentation changes:

1. Validate changed skills with `python skills/agent-rules-skill-author/scripts/validate_agent_skill.py skills/<skill-name>` when available.
2. Search for stale deleted skill names and prohibited Figma/Jam routing.
3. Search changed rules and overlays for non-English rule text.
4. Check that human-facing docs and actual `skills/**` directories agree only when those docs changed, without reading `README.md`.
5. Run Markdown formatting checks when available.
