---
id: 'agents.skills.react-state-workflow.references.selector-rules'
title: 'Selector Rules'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'react-state-workflow'
tags:
    - 'agents/skill-package'
    - 'frontend/state'
    - 'agents/reference'
parent:
    - '[[skills/react-state-workflow/SKILL|React State Workflow]]'
related:
    []
depends_on:
    - '[[skills/react-state-workflow/SKILL|React State Workflow]]'
---

# Selector Rules

## Subscription shape

- Subscribe to the smallest value a component renders or uses for control flow.
- Do not subscribe to root state, a broad slice object, or a broad context value
  and then destructure a few fields unless the full object is the dependency.
- Keep grouped derived reads in named selectors near the owning state module.
- Prefer typed selector hooks that expose stable, narrow contracts.

## Stability rules

- Memoize selectors that return objects or arrays so unchanged inputs keep the
  same output reference.
- Do not create fresh object or array references inside non-memoized inline
  selectors.
- Use an explicit `equalityFn` only when a granular selector would make the
  consuming code less clear or less correct.
- Distinguish stable service hooks from reactive state hooks. Destructuring is
  safe only when the hook contract explicitly guarantees stable callback
  references.
