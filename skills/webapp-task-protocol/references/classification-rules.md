---
id: 'agents.skills.webapp-task-protocol.references.classification-rules'
title: 'Classification Rules'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'webapp-task-protocol'
tags:
    - 'agents/skill-package'
    - 'agents/routing'
    - 'agents/reference'
parent:
    - '[[skills/webapp-task-protocol/SKILL|Webapp Task Protocol]]'
related:
    []
depends_on:
    - '[[skills/webapp-task-protocol/SKILL|Webapp Task Protocol]]'
---

# Classification Rules

## Project type

Use `frontend-only` when the work is primarily:

- UI rendering
- styling and responsiveness
- client-side forms
- API consumption
- content rendering
- component architecture

Use `fullstack` when the work includes:

- auth or session handling
- persistence or database logic
- protected mutations
- Route Handlers or Server Actions
- backend validation or authorization

## Framework selection

Choose `nextjs-app-router` when the task touches:

- routes, layouts, metadata, dynamic segments
- loading, error, or empty states
- server/client boundaries in a Next.js app
- file conventions: `proxy.ts`, `template.tsx`, `global-error.tsx`, `default.tsx`

Choose `react-component-workflow` when the task is primarily:

- component decomposition
- props and state flow
- hooks discipline
- strict TypeScript for component contracts
- client-side rendering logic
- reusable UI behavior outside routing concerns

Choose `react-state-workflow` when the task touches:

- context providers or consumers
- Redux or Redux Toolkit
- selectors, typed store hooks, and provider wiring
- store-like reactive hooks and subscription stability
- deciding whether state should be local, lifted, context-owned, or store-owned

Choose `frontend-design-workflow` when the task is primarily:

- visual UI design, styling polish, typography, color, spacing, or motion
- Figma or screenshot implementation at the visual orchestration layer
- responsive design behavior
- canvas, generative, or web-art UI explicitly requested by the user

Choose `figma-design-reader` when the task is primarily:

- read-only Figma analysis
- node, frame, variable, asset, or screenshot inspection through Figma MCP
- understanding the design before deciding whether to implement code or edit
  Figma

Choose `figma-design-to-code` when the task is primarily:

- implementing repository code from a Figma design
- translating Figma context into the repo's components, tokens, and routes

Choose `figma-canvas-editing` when the task is primarily:

- create, edit, delete, or inspect-with-JavaScript work inside a Figma file
- auto-layout, variables, components, variants, or style mutation through
  `use_figma`

Choose `figma-screen-generation` when the task is primarily:

- building or updating a full screen, page, or multi-section layout inside
  Figma

Choose `figma-design-system-builder` when the task is primarily:

- building a Figma token system, component library, or design-system file

Choose `figma-code-connect` when the task is primarily:

- mapping published Figma components to code through Code Connect

Choose `figma-create-file` when the task is primarily:

- creating a new blank Figma design file or FigJam file

Choose `architecture-from-spec` when the task is primarily:

- turning a specification, technical assignment, or large refactor brief into
  React/frontend architecture guidance
- choosing a recommended architecture path before implementation starts
- producing an implementation-ready plan without editing the repository

Do not choose `architecture-from-spec` for ordinary feature, bugfix, or refactor
implementation requests. If the user asks to implement now, route through the
execution skills below and use architecture notes only as context.

## Overlapping domains

When a task spans both routing and component concerns, use both skills
sequentially — do not pick just one:

1. `nextjs-app-router` first — resolve route structure, file conventions,
   and server/client boundaries.
2. `react-component-workflow` second — component architecture, props flow,
   and hooks within those boundaries.

Add `frontend-design-workflow` when visual implementation or design fidelity is
part of the task. Add `figma-design-to-code` when Figma is the source of truth
for repo implementation. Add `react-state-workflow` when context, Redux,
selectors, or shared client state are part of the task. Add
`boundary-input-validation` whenever the task touches boundary validation or
untrusted input, regardless of which domain skill is active.
