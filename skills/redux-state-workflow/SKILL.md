---
name: redux-state-workflow
description: Use when working on Redux, Redux Toolkit, React Redux selectors,
    typed store hooks, or other shared client-state changes that behave like a
    store layer.
---

# Redux State Workflow

## When to use

- Add or refactor Redux slices, selectors, typed hooks, or provider wiring
- Review store subscriptions, selector stability, or shared client-state shape
- Decide whether state belongs in local component state, context, or Redux
- Inspect store-like hooks whose reactive identity affects rendering

## Required context

Before editing:

1. Read `AGENTS.md`.
2. Read `.agents/project/stack-profile.md` — current framework and whether Redux
   already exists in the repo.
3. Read `.agents/project/architecture-map.md` — current client-state and shared
   code boundaries.
4. Read `.agents/project/react/path-index.md` — where shared-state consumers
   live today.
5. Read `.agents/common/approved-patterns.md`.
6. Read `.agents/project/approved-patterns.md`.
7. Read `.agents/common/anti-patterns.md`.
8. Read `.agents/project/anti-patterns.md`.
9. Read the affected store, selector, provider, hook, and component files.

## Core rules

- Confirm that the requested change belongs in shared state rather than local
  component state.
- Inspect the current store shape, slice layout, selectors, typed hooks, async
  flows, and provider wiring before changing shared state.
- If the inspected repo does not already use Redux, treat adding it as an
  architectural change and do not invent store infrastructure silently.
- Keep shared state serializable, minimal, and focused on state transitions.
- Keep server communication, transport logic, and heavy business processing
  outside Redux reducers and slices.
- Prefer reusable named selectors near the owning slice or store module.
- Prefer narrow subscriptions that return one primitive or one already-stable
  reference at a time.
- If grouped derived data must be returned as an object or array, use a
  memoized selector or an explicit equality strategy for a justified reason.
- Treat `shallowEqual` or another `equalityFn` as an exception, not as the
  default substitute for granular selectors.
- Re-check consuming components after shared-state changes so render
  dependencies remain explicit.

## Reference map

- `references/state-patterns.md`
- `references/selector-rules.md`
- `references/anti-patterns.md`
