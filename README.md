---
id: 'agents.readme'
title: 'WebDev Agent Kit README'
doc_type: 'readme'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/readme'
    - 'frontend'
    - 'developer-guide'
parent: []
related:
    - '[[AGENTS|Canonical Agent Policy]]'
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
depends_on: []
---

# WebDev Agent Kit

WebDev Agent Kit is a project-local skill pack for frontend coding agents.

It gives an agent a structured way to plan, implement, debug, refactor, review, visually verify, and maintain frontend work without turning every prompt into a broad rewrite. The kit is optimized for React and Next.js projects that use CSS Modules, Redux, TanStack, Axios, and TypeScript, while several planning, design, review, visual QA, onboarding, and toolchain workflows can still help in other frontend stacks.

The core idea is simple: put reusable agent behavior in `.agents/`, keep host-project facts in `.agents/project/**`, and make the agent load only the smallest set of rules needed for the current task.

## Quick Usage

Use this section first after the kit is installed in a project.

### 1. Adapt the kit to the current project

Ask the agent:

```text
адаптируйся
```

or in English:

```text
Adapt this .agents bundle to the current frontend project.
```

Expected result:

- the agent reads the host project shape;
- detects whether the project fits the target stack;
- creates or refreshes local-only `.agents/project/**` overlays when approved;
- records stack, architecture, styling, verification, MCP/tool, and path-index facts;
- does not create app source files, install packages, or change runtime code during onboarding.

### 2. Give the agent a task in product terms

Good prompts describe the desired outcome, surface, and constraints:

```text
Implement this approved Design Implementation Spec in the pricing page.
Reuse existing CSS Modules and do not install packages.
Verify desktop and 375px mobile layout.
```

```text
The dashboard route is blank on mobile.
Reproduce the symptom, fix the smallest cause, and run the relevant existing verification.
```

```text
Review this PR for frontend correctness, TypeScript safety, accessibility, performance, and verification gaps.
Do not apply fixes yet.
```

The agent should route the task through `AGENTS.md`, select the right workflow level, load only the matching skill package, and report evidence.

### 3. Use explicit skill names only when you need to force a workflow

Most of the time, let `AGENTS.md` route the task. If you need a specific workflow, call it directly:

```text
Use $frontend-quality-reviewer to review this implementation before merge.
```

```text
Use $loop-workflow-planner to define a bounded loop before repairing visual QA deviations.
```

```text
Use $mcp-toolchain-manager to check which MCP tools are missing for rendered visual QA.
```

### 4. Expect compact evidence, not process theater

Final reports should tell you what changed, why, how it was verified, what is blocked, and the next useful step when there is one.

For code-changing work, expect a report like:

```text
Changed: files or surfaces touched
Why: root cause or implementation rationale
Verified: exact command, rendered check, or blocked check
Risks: unresolved or out-of-scope issues
Next: one useful follow-up, only when needed
```

## Installation

Install the kit inside a host frontend repository as `.agents/`.

Recommended project shape:

```text
your-frontend-project/
├── AGENTS.md
├── .agents/
│   ├── AGENTS.md
│   ├── README.md
│   ├── bundle-manifest.json
│   ├── common/
│   ├── examples/
│   ├── skills/
│   ├── templates/
│   └── project/              # local-only overlays, created during onboarding
├── package.json
└── src/ or app/
```

### Option A: Copy the kit into a project

From the host project root:

```bash
mkdir -p .agents
cp -R /path/to/webdev-agent-kit/. .agents/
```

Then create a small root `AGENTS.md` pointer if the project does not already have one:

```md
# AGENTS.md

Use the project-local agent policy in `.agents/AGENTS.md`.
```

Keep the full policy inside `.agents/AGENTS.md`. The root pointer should not mirror the full bundled policy.

### Option B: Track it as a nested checkout or submodule

If you want to update the kit independently from the host app, keep it as a nested checkout or submodule under `.agents/`.

The host app should still treat `.agents/AGENTS.md` as the canonical policy for agent behavior.

### After installation

Run onboarding through the agent:

```text
адаптируйся
```

Review the proposed `.agents/project/**` overlays before accepting durable project facts. The overlays are local-only and should not be published upstream with the reusable kit.

## What This Is

WebDev Agent Kit is not a UI library, component library, starter template, scaffolder, test framework, or framework generator.

It is a runtime instruction system for coding agents. It tells an agent:

- how to classify frontend tasks by size and risk;
- when to keep work lightweight;
- when to create a goal contract or execution plan;
- when to use bounded verification loops;
- how to extract implementation specs from screenshots;
- how to implement frontend layouts from approved specs;
- how to debug from evidence rather than guesses;
- how to refactor without changing behavior;
- how to review work with severity and evidence;
- how to run visual QA only when rendered evidence is actually needed;
- how to preserve project-local facts in `.agents/project/**`;
- how to avoid unapproved packages, tooling, testing workflows, Figma workflows, broad rewrites, and production access.

## What It Is Not

This kit does not:

- install packages automatically;
- install MCP servers automatically;
- create testing infrastructure by default;
- create app source files during onboarding;
- generate a full application from a vague idea without approval gates;
- migrate routers, state layers, styling systems, build tools, or frameworks by default;
- use live Figma inspection as part of the default screenshot-to-frontend workflow;
- access production systems, secrets, or production data;
- treat README content as runtime policy.

## Supported Frontend Scope

The primary target stack is:

```text
React
Next.js
CSS Modules
Redux
TanStack Query or TanStack Router
Axios
TypeScript
```

Stack-specific implementation and architecture skills are strict about that scope. They should not pretend to support unrelated frameworks.

Some workflows are framework-agnostic and can still apply to Astro, Vue, Svelte, static HTML/CSS, or another frontend stack when the task is about planning, design intake, visual QA, review, MCP/tool detection, documentation, or project-context adaptation.

## How The Kit Works

### Source model

The important layers are:

| Layer | Path | Purpose |
| --- | --- | --- |
| Runtime policy | `AGENTS.md` | Canonical routing, workflow levels, global rules, and source-of-truth model. |
| Skill packages | `skills/**` | Executable workflows selected by user intent. |
| Common rules | `common/**` | Reusable policies, boundaries, anti-patterns, verification rules, UX gates, and token economy rules. |
| Templates | `templates/**` | Optional durable artifacts such as goal contracts, execution plans, loop contracts, visual memory, and progress logs. |
| Examples | `examples/**` | Human-readable example prompts and expected skill chains. |
| Project overlays | `project/**` | Local-only host-project facts. These are ignored by the reusable bundle and should not be published. |
| Distribution output | `dist/**` | Generated release output. Do not patch it directly. |
| README | `README.md` | Human-facing guide. Not runtime policy. |

### Runtime flow

The agent should follow this loop:

```text
classify prompt
-> choose workflow level
-> read minimum authoritative context
-> select one or more skills
-> plan the smallest useful slice
-> execute only approved scope
-> verify with the smallest relevant existing check
-> report evidence and blockers
```

The kit intentionally avoids reading every rule for every task. It uses progressive disclosure: load `AGENTS.md`, then the selected skill, then only the common rules and references that skill needs.

### Workflow levels

| Level | Use for | Behavior |
| --- | --- | --- |
| Fast Lookup | locating a file, answering a narrow repo question, checking one rule | No heavy planning. Read only enough to answer. |
| Lightweight Workflow | one small bug, typo, styling tweak, obvious type error, direct local edit | Keep the task small. No durable plan unless it escalates. |
| Standard Workflow | multi-file feature, meaningful bugfix, refactor, UI implementation, review | Use selected skills, relevant overlays, and verification. |
| Deep Workflow | onboarding, greenfield planning, broad redesign, repeated failure, resumable work | Use goal contracts, execution plans, loop contracts, and local-only memory when useful. |

## Main Capabilities

### Project onboarding and context caching

Use `project-onboarding-adapter` when adapting the kit to a project.

It detects project shape, target-stack fit, routing, styling, state, verification commands, docs/MCP choices, and path indexes. It writes only local project overlays when approved.

Useful prompt:

```text
адаптируйся
```

### Goal and execution planning

Use `goal-planner` and `execution-plan-manager` for standard or deep work that needs explicit goal, scope, constraints, done criteria, task slices, context budget, verification per slice, blockers, and stop/resume state.

Useful prompt:

```text
Define the goal and execution plan before implementing this dashboard redesign.
```

### Bounded agent loops

Use `loop-workflow-planner` when work must repeat until measurable acceptance criteria pass.

The loop contract defines objective, allowed scope, max attempts, retry strategy, verification, independent review, memory update, stop conditions, and escalation conditions.

Useful prompt:

```text
Create a bounded loop contract for fixing the visual QA mismatches.
Stop after three attempts or when the next step needs approval.
```

### Screenshot-to-frontend workflow

Use this chain when a user supplies screenshots, inspect notes, or exported assets:

```text
design-screenshot-spec
-> frontend-design-director when visual judgment is needed
-> frontend-architecture-planner when ownership boundaries matter
-> frontend-layout-implementer
-> frontend-linter-manager when lint exists
-> frontend-visual-qa when rendered evidence is required
-> frontend-quality-reviewer when review is requested or risk is high
```

This workflow is screenshot-first and source-first. It does not use live Figma links, Figma MCP, FigJam, Figma file creation, Figma canvas editing, design-system generation, or Code Connect.

### Design intelligence and design direction

Use `frontend-design-intelligence` to ground a UI task in product category, page pattern, design dials, UX risks, and product-specific anti-patterns.

Use `frontend-design-director` to create a Design Direction Contract with subject, audience, single job, lead thesis, visual position, typography roles, token stance, motion stance, interface copy voice, anti-template checks, implementation handoff, and visual acceptance criteria.

Useful prompt:

```text
Make this landing page direction less generic before implementation.
Ground it in the product category and define visual acceptance criteria.
```

### Architecture planning

Use `frontend-architecture-planner` before code changes when route ownership, component boundaries, React state, Redux state, TanStack remote state, Axios adapters, form behavior, CSS Modules, or build/workspace boundaries matter.

Useful prompt:

```text
Plan where this feature should live in the current Next.js project.
Decide route, state, data, and CSS Modules boundaries before implementation.
```

### Layout implementation

Use `frontend-layout-implementer` when an approved Design Implementation Spec or Design Direction Contract is ready.

The implementer should reuse existing project conventions, CSS Modules, components, tokens, Redux/TanStack/Axios boundaries, and verification commands. It must not add dependencies, UI libraries, global tokens, architecture layers, or new styling systems without explicit approval.

Useful prompt:

```text
Implement this Design Implementation Spec in the current React page.
Reuse existing components and CSS Modules. Do not install packages.
```

### Bugfix debugging

Use `frontend-bugfix-debugger` for UI/runtime errors, broken routes, hydration/client issues, styling regressions, responsive defects, TypeScript errors, or build defects that need evidence.

The bugfix workflow starts from symptom, reproduction path, evidence, and one hypothesis. It fixes the smallest cause and verifies with the same failing command, route, interaction, or symptom when possible.

Useful prompt:

```text
The settings page crashes after clicking Save.
Reproduce it, identify the smallest cause, fix it, and rerun the relevant check.
```

### Refactoring

Use `frontend-refactor-surgeon` for behavior-preserving frontend refactors: component extraction, file reorganization, prop/interface cleanup, state simplification, TypeScript tightening, and duplication removal within a clear boundary.

Useful prompt:

```text
Refactor this settings panel into smaller components without changing behavior.
Preserve rendered output and public props.
```

### Lint verification

Use `frontend-linter-manager` after code-changing frontend work when a lint command exists.

It uses the smallest relevant existing lint command, classifies failures, repairs only related failures when safe, reruns the same command, and reports unresolved lint issues honestly.

It does not add lint packages, scripts, or configuration unless the user explicitly asks for setup and approves the plan.

### Visual QA

Use `frontend-visual-qa` only when rendered browser evidence is required: screenshot comparison, viewport checks, overflow, visible interaction states, visual regression evidence, or console/runtime issues that affect the rendered UI.

It must not open Browser or Playwright just to read font, spacing, color, or token values when source files or copied inspect values can answer the question.

Useful prompt:

```text
Verify the implemented page against these screenshots at desktop, tablet, and 375px mobile.
Report visual mismatches with viewport evidence.
```

### Quality review

Use `frontend-quality-reviewer` for pass/fail review of frontend work. It checks correctness, maintainability, decomposition, TypeScript, security, performance, architecture fit, UX gates, verification honesty, and independent loop acceptance when relevant.

It reports findings by severity and separates required fixes from optional improvements. It does not apply fixes unless the user asked for a combined review-and-fix task.

Useful prompt:

```text
Review this implementation before merge.
Give a pass, pass with concerns, or fail verdict with evidence.
```

### MCP and toolchain management

Use `mcp-toolchain-manager` when a task needs tool capability detection, missing-tool reporting, official install source verification, approval-gated installation planning, or `.agents/project/mcp-profile.md` updates.

It can reason about tools such as filesystem access, Playwright or Browser MCP, Context7, MDN, OpenAI developer docs, GitHub, visual diff, design references, or task management tools. It must not install tools or change configuration without explicit approval.

### Skill authoring and bundle maintenance

Use `agent-rules-skill-author` when changing this kit itself: `AGENTS.md`, `README.md`, `bundle-manifest.json`, `.codex-plugin/plugin.json`, `common/**`, `templates/**`, `project/**`, or `skills/**`.

It keeps native skill metadata, local graph metadata, OpenAI YAML, references, validators, manifests, and README aligned.

## Skill Map

| User need | Primary skill | Notes |
| --- | --- | --- |
| Adapt the kit to a project | `project-onboarding-adapter` | Creates or refreshes local-only project overlays when approved. |
| Refresh stale project context | `project-context-adapter` | Updates only affected `.agents/project/**` facts. |
| Define a goal before work | `goal-planner` | Standard/deep work only. Not for tiny fixes. |
| Split work into slices | `execution-plan-manager` | Adds context budget, verification per slice, stop/resume state. |
| Plan bounded iteration | `loop-workflow-planner` | Required for measurable retry loops and independent review contracts. |
| Convert screenshots into spec | `design-screenshot-spec` | Screenshot/inspect/assets only. No live Figma workflow. |
| Ground design choices | `frontend-design-intelligence` | Product category, page pattern, design dials, anti-patterns. |
| Define visual direction | `frontend-design-director` | Design Direction Contract before implementation. |
| Plan frontend architecture | `frontend-architecture-planner` | React/Next target-stack architecture decisions. |
| Implement approved UI spec | `frontend-layout-implementer` | React/Next implementation with existing project conventions. |
| Fix frontend defects | `frontend-bugfix-debugger` | Evidence-first, one hypothesis, smallest fix. |
| Refactor safely | `frontend-refactor-surgeon` | Behavior-preserving refactors only. |
| Run lint verification | `frontend-linter-manager` | Uses existing lint command; no setup without approval. |
| Verify rendered UI | `frontend-visual-qa` | Rendered evidence only when visual QA is in scope. |
| Review frontend quality | `frontend-quality-reviewer` | Evidence-backed verdict and severity labels. |
| Manage MCP/tool capability | `mcp-toolchain-manager` | Missing tools, official sources, approval gates. |
| Maintain the kit | `agent-rules-skill-author` | Skills, rules, manifests, README, validators. |
| Plan new frontend project | `greenfield-project-builder` | Deep workflow; approval gates before scaffolding. |

## Common Rules Worth Knowing

The agent does not normally read every common rule. These are loaded only when relevant.

| Rule file | Purpose |
| --- | --- |
| `common/prompt-intent-routing-rules.md` | Choose Fast Lookup, Lightweight, Standard, or Deep workflow before loading skills. |
| `common/lightweight-routing-policy.md` | Keep small tasks small and prevent unnecessary planning. |
| `common/token-budget-rules.md` | Spend context on correctness instead of broad reading. |
| `common/token-economy-rules.md` | Reduce context, thinking, and output waste without reducing quality. |
| `common/context-compaction-rules.md` | Preserve only durable facts when work must stop and resume. |
| `common/target-stack-policy.md` | Define target stack and unsupported stack boundaries. |
| `common/framework-adaptation-policy.md` | Keep framework-agnostic skills usable without pretending all stacks are supported. |
| `common/approved-patterns.md` | Source-first design intake, project-native implementation, decomposition, verification. |
| `common/anti-patterns.md` | Bundle-wide prohibited defaults and anti-pattern categories. |
| `common/ui-ux-priority-checklist.md` | Review UI risks in order: accessibility, states, layout, navigation/forms, performance, data, polish. |
| `common/verification-loop-rules.md` | Use existing verification, classify failures, rerun honestly. |
| `common/bounded-retry-rules.md` | Prevent repeated failed strategies and unbounded retries. |
| `common/agent-loop-policy.md` | Platform-neutral loop contract for repeatable agent work. |
| `common/documentation-maintenance.md` | Keep README, manifests, skills, graph links, and references consistent. |

## Project Overlays

`.agents/project/**` is for host-project facts only. These files are local-only and should not be published with the reusable kit.

Typical overlays:

```text
project/stack-profile.md
project/architecture-map.md
project/styling-profile.md
project/verification-profile.md
project/design-reference-profile.md
project/mcp-profile.md
project/approved-patterns.md
project/anti-patterns.md
project/react/path-index.md
project/next/path-index.md
project/active-goals.md
project/active-plan.md
project/progress-log.md
project/decision-log.md
project/loop-memory.md
project/visual-memory.md
```

The purpose of overlays is token and quality control: the agent can read factual project summaries and path indexes instead of scanning the whole repository every time.

## Guardrails

These rules are intentionally strict because the kit is meant to control coding agents, not merely advise them.

### Approval required

The agent must ask for approval before:

- installing packages;
- adding UI libraries;
- adding state, data, form, styling, animation, chart, icon, testing, or build tooling;
- changing package manager, scripts, bundler, monorepo tooling, or framework;
- creating testing infrastructure;
- changing auth persistence, session behavior, or data mutation flow;
- scaffolding a new app;
- touching production systems, secrets, or production data;
- broad rewrites outside the requested scope.

### Frontend state and data boundaries

Default ownership:

- local UI state stays in React components or local hooks;
- Redux stores and mutates application objects only;
- Redux must not own server communication, data processing, or domain workflow layers;
- TanStack-owned remote data should not be duplicated into Redux unless the existing project convention requires it;
- Axios clients and API adapters should be reused rather than replaced.

### Code quality boundaries

The agent should avoid:

- variables created by appending `as const` to values instead of using explicit types;
- anonymous exported components and unnamed behavior-bearing functions;
- `useCallback` by default;
- JSX-returning `renderXxx` helpers inside components;
- unreadable nested array pipelines inside components;
- unclear imperative loops for render-side orchestration;
- unapproved test infrastructure;
- comments added as a substitute for clear naming and structure.

### Design and visual boundaries

The agent should avoid:

- generic SaaS heroes with gradient blobs;
- fake metrics and decorative dashboards;
- badges, grids, numbers, labels, and dividers that do not encode meaning;
- motion used to hide weak layout;
- animation libraries for simple transitions;
- new icon packages when the project already has an icon system;
- screenshots treated as exact design tokens unless values are copied from inspect panels or explicit notes.

### Figma boundary

The default workflow is screenshot-derived. The kit must not use Figma MCP, live Figma inspection, FigJam, Figma whiteboard, canvas editing, Figma file creation, design-system generation, or Code Connect.

When the user supplies only a Figma URL, file key, or node ID, the agent should ask for screenshots, exported assets, copied inspect values, or a written brief.

## Verification Model

The kit prefers the smallest reliable existing evidence.

Verification source order:

1. exact acceptance criterion, failing command, reproduction, route, interaction, or existing regression test;
2. commands recorded in `.agents/project/verification-profile.md` when present;
3. existing lint, typecheck, build, test, or format-check commands relevant to the changed surface;
4. rendered visual QA when visual behavior is in scope;
5. manual source inspection only when executable verification is unavailable.

For code-changing frontend work, lint should run when an existing lint command is available. If no lint command exists, the agent should say that lint was not run and explain the confidence impact.

If verification fails, the agent must classify the failure:

```text
passed
failed: related to current change
failed: likely pre-existing
failed: unrelated environment/tool issue
blocked: required command or tool unavailable
unknown: evidence insufficient
```

It must not switch to an easier command just to claim success.

## Token Economy

The kit includes token economy rules, but the goal is not to make the agent "think less".

The goal is to reduce waste:

- no broad repo scans before targeted search;
- no all-skill reads for narrow tasks;
- no heavy planning for micro-fixes;
- no repeated conclusions;
- no long process narration;
- no full logs when one decisive line is enough.

The agent must preserve:

- acceptance criteria;
- user constraints;
- code semantics;
- exact commands;
- exact paths;
- exact errors;
- API names;
- security warnings;
- irreversible-action confirmations;
- verification evidence;
- known unknowns and blockers.

Correctness wins over compactness.

## MCP And Tooling

MCP tools are optional capabilities, not automatic requirements for every task.

Common capabilities referenced by skills include:

```text
filesystem_server
playwright
context7
mdn
openaiDeveloperDocs
github
browser/devtools
visual-diff
design-reference
```

Rules:

- Use only tools required by the current workflow slice.
- Report missing tools before falling back to lower-confidence checks.
- Verify official install sources before proposing installation.
- Ask for explicit approval before installing MCP servers or changing configuration.
- Do not claim rendered browser QA if Browser or Playwright MCP is unavailable.
- Do not use Figma MCP in this screenshot-derived bundle workflow.

## Example Workflows

### Screenshot to implementation

```text
Use these screenshots and inspect notes to implement the pricing page in the current app.
Match desktop and mobile. Do not use Figma MCP or install packages.
```

Expected route:

```text
design-screenshot-spec
-> frontend-design-director when visual judgment matters
-> frontend-architecture-planner when route/state/data ownership matters
-> frontend-layout-implementer
-> frontend-linter-manager
-> frontend-visual-qa
-> frontend-quality-reviewer when review is requested or risk is high
```

### Bugfix

```text
The dashboard route renders blank on mobile.
Reproduce it and fix the smallest cause.
```

Expected route:

```text
frontend-bugfix-debugger
-> frontend-linter-manager when lint exists
-> frontend-visual-qa when rendered UI changed or the bug is visual
-> frontend-quality-reviewer when review is requested or risk is high
```

### Refactor

```text
Refactor this settings panel into smaller components without changing behavior.
Preserve public props and rendered output.
```

Expected route:

```text
frontend-refactor-surgeon
-> frontend-linter-manager
-> frontend-visual-qa when rendered output risk exists
-> frontend-quality-reviewer when the refactor is broad or requested
```

### Review

```text
Review this frontend change before merge.
Check correctness, TypeScript, accessibility, performance, architecture, and verification honesty.
Do not apply fixes.
```

Expected route:

```text
frontend-quality-reviewer
```

### Greenfield planning

```text
Plan the first version of a new Next.js app for this product idea.
Do not scaffold yet.
```

Expected route:

```text
goal-planner
-> greenfield-project-builder
-> frontend-architecture-planner when boundaries matter
-> execution-plan-manager after approval
-> project-onboarding-adapter for local overlays
```

## Troubleshooting

### The agent ignores the kit

Check that the host project has a root `AGENTS.md` pointer to `.agents/AGENTS.md`, and that the agent environment actually reads repository `AGENTS.md` files.

### The agent reads too much

Ask it to follow Fast Lookup or Lightweight Workflow. The routing rules tell it not to read all skills, all references, all common docs, README, generated `dist/**`, or broad source trees unless the task requires it.

### The agent wants to install a package

Ask for the approval gate. The agent must name the package or tool, reason, official source, exact action, expected validation, and risk before installation.

### The agent asks for a Figma URL or tries live Figma inspection

This kit is screenshot-derived by default. Provide screenshots, exported assets, copied inspect values, or written notes. Do not use Figma MCP unless you intentionally leave this bundle's default workflow.

### Visual QA is blocked

Rendered visual QA requires Browser or Playwright MCP availability in the current agent session. A local server or installed Playwright dependency alone is not enough to claim MCP-backed visual QA.

### The project is not React or Next.js

Use framework-agnostic skills where applicable: onboarding boundary detection, design screenshot spec, design intelligence, design direction, visual QA from browser evidence, quality review, lint manager, planning, loop contracts, MCP toolchain management, and skill authoring.

Do not use React/Next-specific architecture or implementation guidance for unrelated stacks unless the supported scope is explicitly changed.

## Distribution And Maintenance

Source files are the source of truth:

```text
AGENTS.md
README.md
bundle-manifest.json
.codex-plugin/plugin.json
common/**
examples/**
skills/**
templates/**
```

Generated or local-only paths are excluded:

```text
project/**
dist/**
docs/**
.obsidian/**
node_modules/**
```

Do not patch generated `dist/**` output directly. Update source files, then regenerate distribution output through the repository's release process when one is available.

When adding, renaming, or deleting skills:

- update `skills/<skill>/SKILL.md`;
- update `skills/<skill>/agents/openai.yaml`;
- update references under `skills/<skill>/references/**` when needed;
- update `bundle-manifest.json`;
- update `.codex-plugin/plugin.json` when native plugin metadata changes;
- update this README when user-facing workflow, installation, or skill lists change;
- run the local skill validator for changed skill packages when available;
- check for stale skill names, stale paths, and prohibited Figma routing.

## Repository Inventory

The current source bundle contains:

- one canonical runtime policy: `AGENTS.md`;
- one human-facing guide: `README.md`;
- one internal inventory: `bundle-manifest.json`;
- one Codex plugin manifest: `.codex-plugin/plugin.json`;
- reusable rules in `common/**`;
- example workflows in `examples/**`;
- 18 skill packages under `skills/**`;
- templates under `templates/**`;
- generated distribution output excluded from source editing;
- local-only project overlays excluded from publication.

## Developer Checklist

Before using the kit on a real project:

```text
[ ] `.agents/` exists in the host project.
[ ] root `AGENTS.md` points to `.agents/AGENTS.md`.
[ ] `адаптируйся` has been run or onboarding has been planned.
[ ] `.agents/project/**` overlays reflect actual project facts.
[ ] missing MCP/tool capabilities are known and accepted.
[ ] package installation and tooling changes require explicit approval.
[ ] verification commands are known or marked as unavailable.
[ ] the current task has the right workflow level.
```

Before merging kit changes:

```text
[ ] README matches `AGENTS.md`, `bundle-manifest.json`, and `.codex-plugin/plugin.json`.
[ ] Skill list matches actual `skills/**` directories.
[ ] Skill references point to existing files.
[ ] `agents/openai.yaml` matches skill triggers and tool dependencies.
[ ] No host-project facts leaked into publishable docs.
[ ] No Figma MCP dependency became part of the default workflow.
[ ] Markdown and skill validation were run when available.
```
