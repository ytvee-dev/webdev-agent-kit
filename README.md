---
id: 'agents.readme'
title: 'WebDev Assistant README'
doc_type: 'readme'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/readme'
    - 'docs/human'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[examples/screenshot-to-frontend|Screenshot To Frontend Example]]'
    - '[[examples/bugfix-refactor-review|Bugfix Refactor Review Example]]'
    - '[[skills/greenfield-project-builder/SKILL|Greenfield Project Builder]]'
depends_on: []
---

# WebDev Assistant

WebDev Assistant is a focused frontend agent skill pack for React and Next.js projects that use CSS Modules, Redux, TanStack, and Axios.

It helps coding agents plan, implement, verify, debug, refactor, review, and iterate on frontend work without turning the project into a generic framework playground.

## Target Stack

Supported target stack:

- React
- Next.js
- CSS Modules
- Redux
- TanStack
- Axios

Other frontend frameworks, styling systems, UI libraries, app generators, and backend tooling are not supported defaults.

## Usage

1. Copy this package into your project as `.agents/`.
2. Add a host-root `AGENTS.md` pointer to `.agents/AGENTS.md`.
3. Ask the agent: `адаптируйся`.
4. The agent will inspect the project, detect the target stack, create or update `.agents/project/**`, scan MCP needs, cache paths and verification commands, and report missing tools.
5. Missing MCP installation requires explicit approval after the agent reports the official source and exact install or config action.
6. For screenshot-to-code work, provide screenshots, exported assets, copied inspect values, or a written brief.

Recommended first prompt:

```text
адаптируйся к проекту: проверь стек, пути, команды проверки, доступные MCP, недостающие MCP, создай локальный кеш проекта в .agents/project/**, но не меняй исходный код приложения.
```

## Core Flow

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

## What It Does

- Turns supplied screenshots, inspect notes, assets, and briefs into implementation specs.
- Grounds product category, page pattern, design dials, domain UX risks, and product-specific anti-patterns before visual direction when needed.
- Defines subject-grounded visual direction when UI judgment matters.
- Plans frontend architecture before code when routing, state, data, form, styling, build, or workspace boundaries matter.
- Creates platform-neutral loop contracts when work must iterate until measurable acceptance criteria pass.
- Implements scoped React and Next.js frontend changes using existing project conventions.
- Applies conditional UX gates for forms, navigation, data visualization, icons, CSS Modules specificity, and responsive behavior when those surfaces are touched.
- Runs existing lint verification when code changes and a lint command exists.
- Runs rendered visual QA when a local app and browser tooling are available.
- Reviews implementation quality with evidence-backed findings.

## Agent Loop Support

WebDev Assistant supports bounded agent loops without requiring Claude-only commands.

A loop contract defines:

- objective;
- allowed scope;
- acceptance criteria;
- verification source;
- maximum attempts or turns;
- retry strategy;
- independent review;
- memory update;
- stop conditions;
- final evidence.

Claude hosts may map this to `/goal`, `/loop`, subagents, or evaluator workflows when available. Codex, GPT-based coding agents, GitHub PR workflows, and generic agents can execute the same contract manually through plan, edit, verify, retry, review, and final evidence.

## What It Will Not Do By Default

- It will not use Figma MCP or inspect live Figma files.
- It will not add packages, UI libraries, styling systems, framework migrations, app generators, design generators, icon packages, animation libraries, loop automation, or testing workflows without explicit approval.
- It will not run unbounded autonomous loops.
- It will not treat vague goals such as "make it better" as sufficient stop criteria for iterative work.
- It will not turn Redux into server communication or domain processing.
- It will use scoped existing or regression tests when the task and project conventions require them, but it will not add test infrastructure without explicit approval.
- It will not treat README as agent runtime context.
- It will not adapt itself to unrelated frontend stacks as supported defaults.

## Runtime Source Of Truth

`AGENTS.md` and `skills/**` operate the agent.

`README.md` is only a human-facing repository overview and usage guide.

## Main Skills

- `goal-planner`
- `execution-plan-manager`
- `loop-workflow-planner`
- `mcp-toolchain-manager`
- `frontend-design-intelligence`
- `frontend-design-director`
- `frontend-architecture-planner`
- `greenfield-project-builder`
- `frontend-bugfix-debugger`
- `frontend-refactor-surgeon`
- `frontend-quality-reviewer`
- `frontend-linter-manager`
- `design-screenshot-spec`
- `frontend-layout-implementer`
- `frontend-visual-qa`
- `project-onboarding-adapter`
- `project-context-adapter`
- `agent-rules-skill-author`

## Main Common Rule Additions

- `ui-ux-priority-checklist`
- `css-modules-specificity-rules`
- `form-feedback-rules`
- `navigation-ux-rules`
- `data-visualization-rules`
- `icon-quality-rules`
- `mobile-responsive-rules`

## Main Loop Rules

- `agent-loop-policy`
- `stop-criteria-rules`
- `bounded-retry-rules`
- `verification-loop-rules`
- `context-compaction-rules`
- `independent-review-rules`
- `worktree-parallelism-rules`

## Distribution

Source files are the source of truth.

- `bundle-manifest.json` is the internal source and target inventory.
- `.codex-plugin/plugin.json` is the native Codex plugin entrypoint.
- Claude distribution uses portable skill packages and does not include Codex-only metadata.

Generated distribution targets are produced from source during packaging or release and must not be used as runtime context or edited manually.

When generated output is needed, rebuild it from source instead of patching `dist/codex` or `dist/claude` directly.
