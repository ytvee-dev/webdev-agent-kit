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
- client-side rendering logic
- reusable UI behavior outside routing concerns

## Overlapping domains

When a task spans both routing and component concerns, use both skills
sequentially — do not pick just one:

1. `nextjs-app-router` first — resolve route structure, file conventions,
   and server/client boundaries.
2. `react-component-workflow` second — component architecture, props flow,
   and hooks within those boundaries.

Add `frontend-typescript-rules` whenever the task touches types. Add
`boundary-input-validation` whenever the task touches boundary validation or
untrusted input, regardless of which domain skill is active.
