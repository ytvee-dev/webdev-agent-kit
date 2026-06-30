---
id: 'agents.common.skill-applicability-policy'
title: 'Skill Applicability Policy'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'agents/routing'
    - 'frontend/stack'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[common/framework-adaptation-policy|Framework Adaptation Policy]]'
    - '[[common/framework-source-map|Framework Source Map]]'
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
    - '[[skills/frontend-linter-manager/SKILL|Frontend Linter Manager]]'
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
depends_on: []
---

# Skill Applicability Policy

Purpose: prevent the bundle from disabling useful framework-agnostic skills when the host project is not React or Next.js.

The target stack remains React, Next.js, CSS Modules, Redux, TanStack, and Axios for stack-specific implementation, architecture, and greenfield recommendations. Non-target frontend projects may still use skills whose evidence model is screenshots, browser rendering, HTML, CSS, accessibility, TypeScript, project scripts, or `.agents` documentation rather than React or Next.js conventions.

## Applicability Layers

### Target-stack skills

Use these only when the changed surface is inside React, Next.js, CSS Modules, Redux, TanStack, Axios, or an explicitly approved extension of the bundle scope:

- `frontend-layout-implementer`
- `frontend-architecture-planner`
- `greenfield-project-builder`
- stack-specific parts of `frontend-bugfix-debugger`
- stack-specific parts of `frontend-refactor-surgeon`

Do not apply their React, Next.js, CSS Modules, Redux, TanStack, or Axios recommendations to Astro, Vue, Svelte, static HTML, server-rendered templates, or another unrelated framework by default.

### Framework-agnostic frontend skills

These skills may be used in non-target frontend projects when their normal trigger matches:

- `design-screenshot-spec` for screenshots, copied inspect values, exported assets, and written visual notes.
- `frontend-design-director` for visual direction, redesign, design critique, anti-template checks, interface copy stance, motion stance, and visual acceptance criteria.
- `frontend-visual-qa` for rendered browser verification, desktop/mobile screenshots, console checks, overflow checks, and manual or tool-assisted visual comparison.
- `frontend-quality-reviewer` for evidence-backed review of frontend quality, decomposition, accessibility, visual fidelity, TypeScript, security, performance, and verification honesty. Ignore React-only checks when the project is not React.
- `frontend-linter-manager` for existing lint or verification commands after code changes. Do not add lint dependencies, scripts, or configs without explicit approval.
- `goal-planner` and `execution-plan-manager` for standard or deep frontend work that needs goal, scope, slicing, checkpoints, or stop/resume state.
- `mcp-toolchain-manager` for tool capability detection, missing-tool reporting, and approval-gated MCP planning.
- `project-onboarding-adapter` and `project-context-adapter` for limited project overlays, verification facts, MCP facts, design-reference boundaries, and skill applicability notes.
- `agent-rules-skill-author` for reusable bundle rule and skill maintenance.

### Base-agent fallback

When a non-target project needs source edits, use base agent behavior plus local project conventions, MDN/browser-platform rules, existing project scripts, and the framework-agnostic skill outputs. Do not pretend that the React/Next implementation skill is responsible for the code change.

Example non-target screenshot flow:

```text
design-screenshot-spec
-> frontend-design-director when visual judgment is needed
-> base agent implementation using inspected local Astro/Vue/Svelte/static conventions
-> frontend-linter-manager when code changed and an existing command is available
-> frontend-visual-qa when a local app and browser tooling are available
-> frontend-quality-reviewer when quality review is requested or appropriate
```

## Non-Target Project Rule

If the detected host project is Astro, Vue, Svelte, static HTML, server-rendered templates, or another non-target frontend stack:

1. State that stack-specific React/Next implementation guidance is unsupported.
2. Do not stop routing entirely when a framework-agnostic skill matches the user request.
3. Select the smallest applicable framework-agnostic skill before falling back to base agent behavior.
4. Keep any non-target framework facts in local-only `project/**` overlays.
5. Do not add official non-target framework documentation as reusable bundle policy unless the user explicitly approves extending the supported stack.
6. Do not install packages, add UI libraries, add styling systems, or create migrations without explicit approval.

## Validation Gates

- A non-target stack must not suppress `design-screenshot-spec`, `frontend-design-director`, `frontend-visual-qa`, `frontend-quality-reviewer`, `frontend-linter-manager`, planning, MCP, onboarding, context, or skill-authoring skills when their triggers match.
- A framework-agnostic skill must not import React, Next.js, CSS Modules, Redux, TanStack, or Axios rules into a non-target project unless the project actually uses that surface.
- A non-target implementation must be reported as base-agent implementation with local project conventions, not as target-stack implementation.
- Project-specific non-target facts must remain in `project/**` and must not be copied into publishable bundle rules.
