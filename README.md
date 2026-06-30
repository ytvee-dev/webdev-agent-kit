# WebDev Assistant

WebDev Assistant is a focused frontend agent skill pack for React and Next.js projects that use CSS Modules, Redux, TanStack, and Axios.

It helps coding agents plan, implement, verify, debug, refactor, and review frontend work without turning the project into a generic framework playground.

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
-> frontend-design-director when visual judgment is needed
-> frontend-architecture-planner when architecture boundaries matter
-> frontend-layout-implementer
-> frontend-linter-manager when code changed and lint is available
-> frontend-visual-qa
-> frontend-quality-reviewer when quality review is requested or appropriate
```

## What It Does

- Turns supplied screenshots, inspect notes, assets, and briefs into implementation specs.
- Defines subject-grounded visual direction when UI judgment matters.
- Plans frontend architecture before code when routing, state, data, form, styling, build, or workspace boundaries matter.
- Implements scoped React and Next.js frontend changes using existing project conventions.
- Runs existing lint verification when code changes and a lint command exists.
- Runs rendered visual QA when a local app and browser tooling are available.
- Reviews implementation quality with evidence-backed findings.

## What It Will Not Do By Default

- It will not use Figma MCP or inspect live Figma files.
- It will not add packages, UI libraries, styling systems, framework migrations, or app generators without explicit approval.
- It will not turn Redux into server communication or domain processing.
- It will not create tests for components or functions.
- It will not treat README as agent runtime context.
- It will not adapt itself to unrelated frontend stacks as supported defaults.

## Runtime Source Of Truth

`AGENTS.md` and `skills/**` operate the agent.

`README.md` is only a human-facing repository overview and usage guide.

## Main Skills

- `goal-planner`
- `execution-plan-manager`
- `mcp-toolchain-manager`
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

## Distribution

Source files are the source of truth.

Generated distribution targets are produced from source during packaging or release and must not be used as runtime context or edited manually.

When generated output is needed, rebuild it from source instead of patching `dist/codex` or `dist/claude` directly.
