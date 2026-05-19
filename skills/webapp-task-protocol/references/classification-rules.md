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
- Figma or screenshot implementation
- responsive design behavior
- canvas, generative, or web-art UI explicitly requested by the user

## Overlapping domains

When a task spans both routing and component concerns, use both skills
sequentially — do not pick just one:

1. `nextjs-app-router` first — resolve route structure, file conventions,
   and server/client boundaries.
2. `react-component-workflow` second — component architecture, props flow,
   and hooks within those boundaries.

Add `frontend-design-workflow` when visual implementation or design fidelity is
part of the task. Add `react-state-workflow` when context, Redux, selectors, or
shared client state are part of the task. Add `boundary-input-validation`
whenever the task touches boundary validation or untrusted input, regardless of
which domain skill is active.
