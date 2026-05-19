---
id: 'agents.skills.react-state-workflow.references.state-patterns'
title: 'State Patterns'
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

# State Patterns

## Deciding local versus shared state

- Keep transient UI state local when it is owned by one component or one small
  subtree.
- Lift state only when sibling or distant consumers genuinely need coordinated
  updates.
- Use context or Redux only when a shared source of truth is clearer than
  explicit props.
- Do not introduce shared state just to avoid passing a few direct props.
- Check whether an existing hook, provider, selector, or helper already owns the
  behavior before creating another state layer.

## Shared-state responsibilities

- Keep shared state serializable, minimal, and focused on state transitions.
- Keep reducers and state containers free of transport logic, server
  communication, websocket handling, and expensive processing.
- Keep contracts easy to find: state shape, action intent, selector ownership,
  typed hooks, and provider boundaries.
- Keep boundary validation outside shared state; reducers and selectors should
  consume already-normalized data.

## Review points

- Check whether derived reads can stay in selectors or render-time derivation
  instead of duplicating data in state.
- Check whether the new state widens rerender scope for unrelated components.
- Check whether grouped state should be split so consumers can subscribe more
  narrowly.
