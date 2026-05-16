---
name: react-component-workflow
description: Use when working on React component structure, props and state
    flow, hooks discipline, rendering logic, and reusable UI behavior.
---

# React Component Workflow

## When to use

- Build or refactor components
- Improve props, state, or render flow
- Split orchestration and presentation concerns
- Implement Figma-derived UI that is not primarily a routing task

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
10. Read `.agents/project/figma-profile.md` — only when the work starts from design.

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
- Reuse the established styling system and component patterns of the repo.
- If the component task also changes Redux, selectors, or another store layer,
  add `redux-state-workflow` instead of handling shared-state design inside this
  skill alone.
- After component, helper, token, or client-boundary changes, verify whether
  `.agents/project/react/path-index.md` or related overlays need updates.

## Figma

When implementing from Figma:

1. Inspect the design first with the built-in Figma capabilities.
2. Recreate structure and responsive behavior with existing repo patterns.
3. Avoid hardcoded values when existing tokens or abstractions fit.
4. If Figma access fails, ask the user for screenshots and use
   `screenshot-design-inspector` before implementing UI.

## Reference map

- `references/component-patterns.md`
- `references/hooks-rules.md`
- `references/anti-patterns.md`
- `references/figma-implementation.md`
- `references/tooling-and-prompting.md`
