---
id: 'agents.skills.redux-state-workflow.references.anti-patterns'
title: 'Anti-Patterns'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'redux-state-workflow'
tags:
    - 'agents/skill-package'
    - 'frontend/state'
    - 'agents/reference'
parent:
    - '[[skills/redux-state-workflow/SKILL|Redux State Workflow]]'
related:
    []
depends_on:
    - '[[skills/redux-state-workflow/SKILL|Redux State Workflow]]'
---

# Anti-Patterns

- Using Redux as a transport, fetch, websocket, or heavy business-processing layer
- Keeping local-only UI state in Redux without a verified shared-ownership need
- Selecting broad state objects and destructuring a small subset afterward
- Returning fresh objects or arrays from inline selectors without memoization or
  an explicit equality strategy
- Treating `shallowEqual` as the default answer instead of fixing selector shape
- Assuming destructuring from a store-like hook is safe without a stable
  contract
- Introducing new shared state before checking whether an existing hook,
  provider, selector, or helper already solves the same problem
