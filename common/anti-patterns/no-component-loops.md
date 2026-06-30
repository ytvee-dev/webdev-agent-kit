---
id: 'agents.common.anti-patterns.no-component-loops'
title: 'No Project Code Loops'
doc_type: 'anti-pattern-template'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'anti-patterns/readability'
parent:
    - '[[common/anti-patterns/README|Anti-Pattern Templates]]'
related:
    - '[[common/frontend-implementation-boundaries|Frontend Implementation Boundaries]]'
depends_on: []
---

# No Project Code Loops

## Rule

Do not introduce project-code loops.

This applies to components, routes, state slices, effects, render logic, business orchestration, adapters, selectors, and helpers.

## Exception

A loop is allowed only inside a small isolated utility when there is no practical alternative.

The exception must be named, local, small, outside render and orchestration code, and reported in the final response.

## Apply When

Use this whenever implementation, bugfix, refactor, or review touches collection handling, list rendering, transformations, adapters, selectors, or UI actions.
