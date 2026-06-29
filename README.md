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
- It will not treat README as agent runtime context.
- It will not adapt itself to unrelated frontend stacks as supported defaults.

## Runtime Source Of Truth

`AGENTS.md` and `skills/**` operate the agent.

`README.md` is only a human-facing repository overview and installation guide.

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

Source files are the source of truth. Generated targets live under `dist/codex` and `dist/claude`.

Update source files first, then rebuild distribution targets.
