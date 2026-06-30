---
id: 'agents.common.anti-patterns.no-anonymous-functions'
title: 'No Anonymous Functions'
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

# No Anonymous Functions

## Rule

Use named components, handlers, callbacks, predicates, mappers, selectors, adapters, formatters, and helpers.

Do not export anonymous components. Do not hide meaningful behavior inside unnamed callbacks or inline handlers.

## Apply When

Name any behavior that affects rendering, state, data preparation, formatting, action selection, navigation, accessibility, or side effects.
