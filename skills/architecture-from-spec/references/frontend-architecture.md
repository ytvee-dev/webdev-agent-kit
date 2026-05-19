---
id: 'agents.skills.architecture-from-spec.references.frontend-architecture'
title: 'Frontend Architecture'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'architecture-from-spec'
tags:
    - 'agents/skill-package'
    - 'architecture/spec'
    - 'frontend/react'
    - 'agents/reference'
parent:
    - '[[skills/architecture-from-spec/SKILL|Architecture From Spec]]'
related:
    - '[[skills/react-component-workflow/SKILL|React Component Workflow]]'
    - '[[skills/react-state-workflow/SKILL|React State Workflow]]'
    - '[[skills/frontend-design-workflow/SKILL|Frontend Design Workflow]]'
depends_on:
    - '[[skills/architecture-from-spec/SKILL|Architecture From Spec]]'
---

# Frontend Architecture

Use this reference when turning a product spec, technical assignment, or large
refactor brief into a React/frontend implementation plan.

## Decision points

- Routing and rendering: identify which parts are route-level composition,
  server-rendered, client-only, or shared UI.
- Component boundaries: separate orchestration, presentation, reusable
  primitives, and feature-owned components only where the split improves
  readability or reuse.
- State ownership: decide local state, lifted state, context, Redux/store-like
  state, or server-owned state from real shared ownership needs.
- Data boundaries: validate route params, search params, form input, external
  data, file content, and public entry-point input near the boundary.
- Security surfaces: identify auth/session, secrets, redirects, unsafe
  rendering, browser storage, and client/server data exposure.
- Design system: reuse current tokens, styling conventions, components, and
  breakpoints before proposing new primitives.
- Verification: map the architecture to TypeScript, lint, format, build, test,
  browser, and manual checks that match the risk surface.

## Output expectations

- Recommend one architecture path that fits the stated constraints.
- Provide alternatives only when they change meaningful tradeoffs.
- Mark unknowns that would change the plan instead of choosing silently.
- Keep file or folder suggestions behavior-level unless exact paths are needed
  to prevent ambiguity.
