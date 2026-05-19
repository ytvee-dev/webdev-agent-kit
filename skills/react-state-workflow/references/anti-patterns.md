---
id: 'agents.skills.react-state-workflow.references.anti-patterns'
title: 'Anti-Patterns'
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

# Anti-Patterns

- Moving local-only UI state into context, Redux, or another store without a
  verified shared-ownership need.
- Adding Redux to a repo that does not already use it without explicit user
  approval.
- Using Redux or context as a transport, fetch, websocket, or heavy
  business-processing layer.
- Selecting broad state objects and destructuring a small subset afterward.
- Returning fresh objects or arrays from inline selectors without memoization or
  an explicit equality strategy.
- Treating `shallowEqual` as the default answer instead of fixing selector
  shape.
- Assuming destructuring from a store-like hook is safe without a stable
  contract.
- Introducing new shared state before checking whether an existing hook,
  provider, selector, or helper already solves the same problem.
