---
id: 'agents.summary'
title: 'Agent Documentation Summary'
doc_type: 'summary'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/summary'
    - 'docs/navigation'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[README|WebDev Assistant README]]'
depends_on: []
---

# Agent Documentation Summary

Purpose: provide a manual catalog of the focused WebDev Assistant `.agents` bundle for humans.

This file is not part of normal agent runtime. Agents must not use this file for prompt routing or required context unless the user explicitly asks to edit, audit, or summarize `SUMMARY.md`.

## Target Stack

WebDev Assistant targets only React, Next.js, CSS Modules, Redux, TanStack, and Axios.

Other frontend frameworks, UI libraries, app generators, and styling systems are not supported defaults. Generated `dist/**` targets must not be treated as source-of-truth during normal source editing.

## Common Docs

- `common/target-stack-policy.md` - supported stack, source priority, and unsupported scope policy.
- `common/approved-patterns.md` - project-native implementation patterns for the target stack.
- `common/anti-patterns.md` - prohibited workflow and implementation directions.
- `common/documentation-maintenance.md` - rules for changing bundle docs and skill packages.
- `common/prompt-intent-routing-rules.md` - task scale routing rules.
- `common/design-quality-rubric.md` - design review dimensions and verdicts.
- `common/anti-template-defaults.md` - suspicious generic AI design defaults.
- `common/interface-copy-rules.md` - interface copy rules.
- `common/motion-rules.md` - restrained frontend motion rules.
- `common/lint-verification-rules.md` - lint verification and approval-gated lint setup rules.
- `common/agent-operating-model.md` - inspect, plan, execute, verify, and report operating loop.
- `common/goal-contract.md` - reusable goal contract fields and rules.
- `common/planning-rules.md` - task slice, context budget, and planning rules.
- `common/execution-loops.md` - standard, debug, and refactor loops.
- `common/token-budget-rules.md` - targeted context gathering and escalation rules.
- `common/checkpoint-rules.md` - durable stop/resume state rules.
- `common/framework-adaptation-policy.md` - target-stack adaptation policy.
- `common/framework-source-map.md` - official source order for target-stack guidance.
- `common/state-ownership-rules.md` - React local state, Redux object state, and TanStack remote state ownership rules.
- `common/routing-boundary-rules.md` - route ownership and router boundary rules.
- `common/data-fetching-boundary-rules.md` - TanStack and Axios data boundary rules.
- `common/form-boundary-rules.md` - form state, validation, and accessibility boundaries.
- `common/build-tool-boundary-rules.md` - build, package, and workspace tooling boundaries for supported projects.
- `common/frontend-integration-boundaries.md` - React, Next.js, Redux, TanStack, and Axios integration limits.
- `common/typescript-discipline.md` - TypeScript safety rules.
- `common/debugging-evidence-rules.md` - symptom, reproduction, and evidence rules.
- `common/refactor-safety-rules.md` - behavior-preserving refactor rules.
- `common/review-severity-model.md` - review verdicts and severity labels.
- `common/security-review-rules.md` - frontend security review rules.
- `common/performance-review-rules.md` - evidence-backed frontend performance review rules.
- `common/cross-agent-compatibility-rules.md` - Codex and Claude target packaging policy.
- `common/portable-skill-core-contract.md` - portable `SKILL.md` core contract.

## Project Overlays

`project/**` is local-only and must not be copied into publishable reusable skills or common docs.

Expected overlays include stack, architecture, styling, verification, MCP, docs, build, workspace, state, data-fetching, design-reference, and visual-memory profiles when relevant.

## Skills

- `skills/goal-planner` - define user goal, scope, constraints, and done criteria.
- `skills/execution-plan-manager` - split work into small verified slices.
- `skills/mcp-toolchain-manager` - detect MCP/tool capabilities and approval-gated setup.
- `skills/frontend-design-director` - define subject-grounded visual direction.
- `skills/frontend-architecture-planner` - plan React/Next.js architecture, routing, state, data, styling, forms, build/workspace concerns, approval gates, and handoff.
- `skills/greenfield-project-builder` - plan new React or Next.js projects before scaffold or package installation.
- `skills/frontend-linter-manager` - run existing lint verification or plan approved lint setup.
- `skills/frontend-bugfix-debugger` - reproduce frontend symptoms, gather evidence, fix the smallest cause, and verify against the original bug.
- `skills/frontend-refactor-surgeon` - perform behavior-preserving refactors with explicit boundaries and verification.
- `skills/frontend-quality-reviewer` - review frontend work with evidence, severity labels, and no broad rewrite by default.
- `skills/design-screenshot-spec` - convert supplied screenshots, inspect panels, assets, and notes into a `Design Implementation Spec`.
- `skills/frontend-layout-implementer` - implement specs in React/Next.js projects using existing CSS Modules, Redux, TanStack, and Axios conventions.
- `skills/frontend-visual-qa` - verify rendered UI against the design spec and visual references.
- `skills/project-onboarding-adapter` - target-stack onboarding, host-root pointer handling, docs/MCP selection, and local-only overlays.
- `skills/project-context-adapter` - refresh factual project overlays and frontend path indexes.
- `skills/agent-rules-skill-author` - create, edit, evaluate, and validate `.agents` skill packages and bundle rules.

## Main Pipeline

```text
design-screenshot-spec
-> frontend-design-director when visual judgment is needed
-> frontend-architecture-planner when architecture boundaries matter
-> frontend-layout-implementer
-> frontend-linter-manager when code changed and lint is available
-> frontend-visual-qa
-> frontend-quality-reviewer when quality review is requested or appropriate
```

For new or empty React/Next.js projects:

```text
goal-planner
-> execution-plan-manager
-> greenfield-project-builder
-> frontend-architecture-planner when architecture boundaries need deeper planning
-> project-onboarding-adapter for pointer and local-only overlays
```

## Navigation Rules

- Use Project Context MCP when available for project facts; otherwise read `project/**` and affected source files directly.
- Use Design Spec MCP when available; otherwise keep the spec in the response or a user-approved local artifact.
- Use Visual Reference MCP when available; otherwise rely on attached images and local files supplied by the user.
- Use Visual Diff MCP when available; otherwise use the manual visual-diff checklist.
- Use `context7` for React, Next.js, Redux, TanStack, Axios, TypeScript, or build-tool docs when needed.
- Use `mdn` for HTML, CSS, Web APIs, and browser compatibility.
- Use Browser or Playwright MCP for rendered frontend verification.
- Install missing MCP servers only after explicit user approval and verified official source.
- Never use Figma MCP or Figma whiteboard tooling in this bundle.
