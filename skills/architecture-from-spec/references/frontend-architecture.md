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
    - '[[skills/webapp-task-protocol/SKILL|Webapp Task Protocol]]'
    - '[[skills/nextjs-app-router/SKILL|Nextjs App Router]]'
    - '[[skills/react-component-workflow/SKILL|React Component Workflow]]'
    - '[[skills/react-state-workflow/SKILL|React State Workflow]]'
    - '[[skills/boundary-input-validation/SKILL|Boundary Input Validation]]'
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

## Output shape

- Architecture slices:
  describe route structure, feature boundaries, shared layers, and cross-cutting
  services at the level needed for safe implementation. Keep slices tied to
  behavior and ownership, not a generic folder template.
- Ownership boundaries:
  state which concerns belong to routes, features, shared UI, state layers,
  validation boundaries, and infrastructure helpers. Name the execution skill
  that should own each later implementation surface when the owner is not
  obvious.
- State, routing, data, security, and styling implications:
  explain only the decisions that materially affect implementation shape
- Verification surfaces:
  connect the proposed architecture to the checks and review steps that should
  exist later
- Deferred execution details:
  explicitly mark what should be implemented later by execution skills instead
  of pretending the architecture brief already made those edits

## Handoff boundaries

- Defer route files, layouts, metadata, server/client boundaries, and route UX
  states to `nextjs-app-router`.
- Defer component extraction, props, hooks, render logic, and strict TypeScript
  implementation to `react-component-workflow`.
- Defer context, Redux, selectors, providers, shared state shape, and
  subscription stability to `react-state-workflow`.
- Defer route params, search params, form input, external data, file content,
  and other untrusted input parsing to `boundary-input-validation`.
- Defer visual implementation, Figma translation, responsive polish, and
  design-system interpretation to `frontend-design-workflow`.
- Defer final implementation review, regression checks, and verification
  execution to `frontend-review-and-fix`.

## Output expectations

- Recommend one architecture path that fits the stated constraints.
- Provide alternatives only when they change meaningful tradeoffs.
- Mark unknowns that would change the plan instead of choosing silently.
- Keep file or folder suggestions behavior-level unless exact paths are needed
  to prevent ambiguity.
- Keep the deliverable as architecture guidance or an implementation-ready plan,
  not an implicit start of repo edits.
