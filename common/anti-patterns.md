---
id: 'agents.common.anti-patterns'
title: 'Common Anti-Patterns'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/policy'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[SUMMARY|Agent Documentation Summary]]'
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
depends_on:
    []
---

# Common Anti-Patterns

Purpose: define bundle-wide pitfalls that should not be published as local
project context and should not be reintroduced across host projects.

Use `.agents/project/anti-patterns.md` only for host-repo-specific additions or
explicit local exceptions.

- Installing packages before checking whether the package and required version
  already exist
- Installing packages or changing shared tokens without explicit user approval
- Using a dev server as a substitute for the documented verification flow
- Interacting with production systems, production data, or live production
  environments
- Waiting for the user to explicitly request project-context verification or
  documentation sync after the affected area is already known
- Inventing missing requirements, API contracts, architecture, or behavior
  instead of narrowing the search and asking the user
- Refactoring unrelated code the user did not ask to change
- Duplicating existing code instead of reusing or carefully extending the
  current implementation
- Adding helpers, services, selectors, hooks, or modules before checking
  whether the host repo already solves the same problem
- Using `any`, `@ts-ignore`, or similarly broad unsafe typing
- Using `{} as const` or similar empty assertions to bypass typing
- Creating meaningless pass-through aliases or variables that only rename an
  existing symbol without adding domain meaning
- Re-validating already guaranteed values inside internal helpers when the
  contract is already established
- Choosing terse or clever syntax over straightforward control flow when
  readability drops
- Hardcoding reusable text, links, or configuration inside render trees when a
  clear config owner exists
- Leaving magic numbers unnamed when a shared token, shared constant, or clear
  local constant should carry the meaning
- Adding code comments without an explicit user request or a real safety need
- Using `useCallback` by default
- Using `void someFunc()`
- Building JSX in `renderSomething` variables instead of extracting a component
- Using `let isCancelled = false` cancellation guards instead of
  `AbortController`
- Hiding route or component metadata inside component bodies instead of keeping
  it adjacent to the owner
- Reusing component names for different components in the same repository
- Using imperative loops inside components to assemble render structures when a
  clearer component or data-flow decomposition would avoid them
- Keeping local-only UI state in Redux or another broad shared store without a
  real shared-ownership need
- Using Redux or another shared client store as a transport layer, fetch layer,
  or heavy business-processing layer
- Subscribing to broad store or context objects and then destructuring a few
  fields when a narrower selector or hook contract would be clearer
- Returning fresh objects or arrays from non-memoized selectors or store-like
  hooks without a stability strategy
- Assuming destructuring from a store-like hook is safe by default when the hook
  contract does not explicitly guarantee stable references
- Writing new feature tests without an explicit user request
- Publishing `.agents/project/**`, `upstream/**`, or other host-project context
  into the shared `webdev-assistant` repository
