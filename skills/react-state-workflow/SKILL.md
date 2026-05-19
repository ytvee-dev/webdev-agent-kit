---
name: react-state-workflow
description: Use when React work touches shared client state, Context, Redux or Redux Toolkit, selectors, typed store hooks, provider wiring, or store-like reactive hooks. Do not use for trivial component-local useState that has no shared ownership or subscription-stability concerns.
id: 'agents.skills.react-state-workflow.skill'
title: 'React State Workflow'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'react-state-workflow'
tags:
    - 'agents/skill-package'
    - 'frontend/state'
    - 'frontend/react'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/react-state-workflow/references/anti-patterns|Anti-Patterns]]'
    - '[[skills/react-state-workflow/references/selector-rules|Selector Rules]]'
    - '[[skills/react-state-workflow/references/state-patterns|State Patterns]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# React State Workflow

## When to use

- Decide whether state belongs in component state, lifted state, context, Redux,
  or another store-like layer.
- Add or refactor context providers, Redux slices, selectors, typed hooks, or
  provider wiring.
- Review store subscriptions, selector stability, reactive hook identity, or
  shared client-state shape.
- Inspect components whose render path depends on shared reactive inputs.

## Required context

Before editing:

1. Read `AGENTS.md`.
2. Read `.agents/project/stack-profile.md` to confirm current state-management
   tools and whether Redux already exists.
3. Read `.agents/project/architecture-map.md` for current client-state and
   shared code boundaries.
4. Read `.agents/project/react/path-index.md` for state consumers and related
   components.
5. Read `.agents/common/approved-patterns.md`.
6. Read `.agents/project/approved-patterns.md`.
7. Read `.agents/common/anti-patterns.md`.
8. Read `.agents/project/anti-patterns.md`.
9. Read the affected state owner, provider, selector, hook, and consumer files.

## Core rules

- Prove shared ownership before moving state out of a component.
- Keep transient UI state local when one component or one small subtree owns it.
- Lift state only when multiple consumers genuinely need a shared source of
  truth or coordinated updates.
- Treat context, Redux, selectors, and custom store-like hooks as reactive
  inputs whose identity affects rendering.
- If the repo does not already use Redux, treat adding Redux as an architecture
  change that requires explicit user approval.
- Keep shared state serializable, minimal, and focused on state transitions.
- Keep transport logic, websocket handling, server communication, and heavy
  business processing outside reducers, slices, and state containers.
- Prefer reusable named selectors or narrow store hooks near the owning module.
- Prefer subscriptions that return one primitive or one already-stable reference
  at a time.
- If grouped derived data must be returned as an object or array, use a memoized
  selector or an explicit equality strategy for a justified case.
- Treat `shallowEqual` or another `equalityFn` as an exception, not as the
  default substitute for granular subscriptions.
- Re-check consuming components after shared-state changes so render
  dependencies remain explicit.

## Reference map

- `references/state-patterns.md`
- `references/selector-rules.md`
- `references/anti-patterns.md`
