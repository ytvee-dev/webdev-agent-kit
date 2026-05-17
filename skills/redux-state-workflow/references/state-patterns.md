---
id: 'agents.skills.redux-state-workflow.references.state-patterns'
title: 'State Patterns'
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

# State Patterns

## Deciding local vs shared state

- Keep transient UI state local when it is owned by one component or one small
  subtree.
- Move state to context or Redux only when multiple distant consumers need the
  same source of truth or coordinated updates.
- Do not introduce shared state just to avoid passing a few explicit props.

## Store responsibilities

- Use Redux for storing and mutating application state.
- Keep reducers focused on state transitions.
- Keep transport logic, server communication, and expensive processing in
  helpers, services, hooks, or providers outside the reducer layer.
- Keep store contracts explicit: state shape, action intent, selector ownership,
  and typed hooks should be easy to find.

## Shared-state review points

- Check whether the new state is serializable and minimal.
- Check whether derived reads can stay in selectors instead of duplicating data
  across the store.
- Check whether the same behavior is already available through an existing
  provider, context, selector, or hook before creating new state modules.
