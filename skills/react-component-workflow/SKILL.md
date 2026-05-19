---
name: react-component-workflow
description: Use as the primary React implementation workflow for component structure, props and state flow, hooks discipline, rendering logic, strict TypeScript, reusable UI behavior, and client UI changes. Do not use for security audits, SEO-only work, or shared store design that needs the react-state-workflow skill.
id: 'agents.skills.react-component-workflow.skill'
title: 'React Component Workflow'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'react-component-workflow'
tags:
    - 'agents/skill-package'
    - 'frontend/react'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/react-component-workflow/references/anti-patterns|Anti-Patterns]]'
    - '[[skills/react-component-workflow/references/component-patterns|Component Patterns]]'
    - '[[skills/react-component-workflow/references/hooks-rules|Hooks Rules]]'
    - '[[skills/react-component-workflow/references/typescript-rules|TypeScript Rules]]'
    - '[[skills/react-state-workflow/SKILL|React State Workflow]]'
    - '[[skills/frontend-design-workflow/SKILL|Frontend Design Workflow]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# React Component Workflow

## When to use

- Build or refactor components
- Improve props, state, or render flow
- Split orchestration and presentation concerns
- Implement client UI that is not primarily a routing task
- Touch component props, exported helpers, or TypeScript-heavy UI refactors

## Required context

Before editing:

1. Read `AGENTS.md`.
2. Read `.agents/project/stack-profile.md` — React version and project type.
3. Read `.agents/project/react/path-index.md` — targeted lookup for component work.
4. Read `.agents/project/architecture-map.md` — component locations and shared patterns.
5. Read `.agents/common/approved-patterns.md` — bundle-wide approved implementation patterns.
6. Read `.agents/project/approved-patterns.md` — host-project-specific additions and examples.
7. Read `.agents/common/anti-patterns.md` — bundle-wide patterns to avoid.
8. Read `.agents/project/anti-patterns.md` — host-project-specific additions and exceptions.
9. Read `.agents/project/styling-profile.md` — token system and styling conventions.
10. Add `frontend-design-workflow` when the work starts from Figma,
    screenshots, visual redesign, or styling polish.

## Core rules

- Prefer MCP tools and project indexes before broad repo scanning.
- Use this lookup fallback order: `.agents/project/react/path-index.md` ->
  targeted repo search -> user clarification.
- Prefer small, focused components with one clear responsibility.
- Keep data flow explicit through props and clear ownership.
- Derive state when possible instead of duplicating it.
- Use effects only for true side effects, not for routine render logic.
- Treat store, context, and custom store-like hook results as reactive inputs
  whose identity affects rendering.
- Prefer narrow subscriptions over pulling broad reactive objects into a render
  path when the component only needs a small subset of values.
- Destructure service-hook results only when the inspected hook contract
  explicitly guarantees stable callback references.
- Preserve strict TypeScript. Do not use `any`, `@ts-ignore`, unsafe double
  casts, broad object types, or copied parallel types when a real source type
  exists.
- Use type-only imports, discriminated unions, explicit exported API types, and
  proper runtime narrowing where they clarify the component contract.
- Reuse the established styling system and component patterns of the repo.
- If the component task also changes context, Redux, selectors, provider
  wiring, or another shared store layer, add `react-state-workflow` instead of
  handling shared-state design inside this skill alone.
- If the task is primarily visual direction, Figma translation, responsive
  polish, canvas/generative UI, or design-system interpretation, add
  `frontend-design-workflow` and let this skill handle the React composition
  layer.
- After component, helper, token, or client-boundary changes, verify whether
  `.agents/project/react/path-index.md` or related overlays need updates.

## Reference map

- `references/component-patterns.md`
- `references/hooks-rules.md`
- `references/anti-patterns.md`
- `references/typescript-rules.md`
