# Task Routing

## Recommended chains

### Feature / refactor / bugfix

1. `webapp-task-protocol`
2. Domain skill(s):
    - `nextjs-app-router` — routing, layouts, file conventions, server/client boundaries
    - `react-component-workflow` — component architecture, props, state, hooks
    - `redux-state-workflow` — Redux, selectors, typed hooks, and shared client state
    - Use both when the task spans routing AND component concerns (see `classification-rules.md`)
    - Use `redux-state-workflow` alongside the React or Next skill when the task
      changes store shape, selectors, provider wiring, or store consumers
3. Add `frontend-typescript-rules` when typing or refactors matter
4. Add `boundary-input-validation` when boundary input is parsed or validated
5. Finish with `frontend-review-and-fix`

### Cross-domain feature

When a feature requires new routes AND new component architecture:

1. `webapp-task-protocol`
2. `nextjs-app-router` — establish route structure and boundaries
3. `react-component-workflow` — implement component internals
4. Add `redux-state-workflow` when shared client state is part of the feature
5. Add `frontend-typescript-rules` and `boundary-input-validation` as needed
6. `frontend-review-and-fix`

### Review request

1. `webapp-task-protocol`
2. `frontend-review-and-fix`

### SEO request

1. `technical-seo-app`

### Security request

1. `frontend-security-inspector`

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
