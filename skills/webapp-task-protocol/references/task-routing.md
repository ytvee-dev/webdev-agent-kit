---
id: 'agents.skills.webapp-task-protocol.references.task-routing'
title: 'Task Routing'
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

# Task Routing

## Recommended chains

### Feature / refactor / bugfix

1. `webapp-task-protocol`
2. Domain skill(s):
    - `nextjs-app-router` — routing, layouts, file conventions, server/client boundaries
    - `react-component-workflow` — component architecture, props, state, hooks
    - `react-state-workflow` — context, Redux, selectors, typed hooks, and shared client state
    - `frontend-design-workflow` — visual design, Figma, screenshots, responsive polish
    - `figma-design-to-code` — implement repo code from Figma when Figma is the source of truth
    - Use both when the task spans routing AND component concerns (see `classification-rules.md`)
    - Use `react-state-workflow` alongside the React or Next skill when the task
      changes store shape, selectors, provider wiring, or store consumers
3. Add `boundary-input-validation` when boundary input is parsed or validated
4. Finish with `frontend-review-and-fix`

### Cross-domain feature

When a feature requires new routes AND new component architecture:

1. `webapp-task-protocol`
2. `nextjs-app-router` — establish route structure and boundaries
3. `react-component-workflow` — implement component internals
4. Add `react-state-workflow` when shared client state is part of the feature
5. Add `frontend-design-workflow` when visual design or responsive polish is part of the feature
6. Add `boundary-input-validation` as needed
7. `frontend-review-and-fix`

### Review request

1. `webapp-task-protocol`
2. `frontend-review-and-fix`

### SEO request

1. `technical-seo-app`

### Security request

1. `frontend-security-inspector`

### Design request

1. `frontend-design-workflow`
2. `figma-design-reader` for read-only Figma inspection when the request starts from Figma
3. `figma-design-to-code` when the deliverable is repo code from Figma
4. `react-component-workflow` or `nextjs-app-router` as needed for implementation
5. `screenshot-design-inspector` when Figma access is unavailable and screenshots are the source

### Figma canvas request

1. `figma-canvas-editing`
2. `figma-screen-generation` when the deliverable is a full screen or page
3. `figma-design-system-builder` when the deliverable is a library or token system

### Figma Code Connect request

1. `figma-code-connect`

### Figma file creation request

1. `figma-create-file`

### Repo refresh request

1. `project-context-adapter`

### Documentation or agent-rules request

1. `agent-rules-skill-author`

### Bundle sync or upstream publication request

1. `webdev-assistant-sync`
2. `agent-rules-skill-author` when the task also changes the bundle rules,
   routing, or documentation structure itself

### Architecture or spec request

1. `architecture-from-spec`

This chain ends in architecture guidance or an implementation-ready plan. It does
not implicitly continue into execution skills until the user asks for
implementation.

Do not append `nextjs-app-router`, `react-component-workflow`,
`react-state-workflow`, or `boundary-input-validation` as implementation steps
while the deliverable is still architecture guidance. Name those skills only as
later handoff owners unless the user explicitly changes the deliverable to code
execution.
