---
id: 'agents.common.anti-patterns.index'
title: 'Anti-Pattern Templates'
doc_type: 'common-rule-index'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'anti-patterns'
parent:
    - '[[common/anti-patterns|Common Anti-Patterns]]'
related:
    - '[[common/anti-patterns/no-as-const-variables|No As Const Variables]]'
    - '[[common/anti-patterns/no-anonymous-functions|No Anonymous Functions]]'
    - '[[common/anti-patterns/no-use-callback-by-default|No UseCallback By Default]]'
    - '[[common/anti-patterns/no-render-functions|No Render Functions]]'
    - '[[common/anti-patterns/no-nested-array-pipelines|No Nested Array Pipelines]]'
    - '[[common/anti-patterns/no-component-loops|No Component Loops]]'
    - '[[common/anti-patterns/no-unapproved-test-infrastructure|No Unapproved Test Infrastructure]]'
depends_on: []
---

# Anti-Pattern Templates

Purpose: provide small, loadable anti-pattern files with code examples. Load only the files relevant to the current task.

## Templates

- `no-as-const-variables.md` - do not create variables by casting values with `as const`.
- `no-anonymous-functions.md` - use named components, handlers, and helpers.
- `no-use-callback-by-default.md` - do not use `useCallback` unless the local code proves it is needed.
- `no-render-functions.md` - do not create JSX-returning helpers named `renderXxx`, `xxxRender`, or similar.
- `no-nested-array-pipelines.md` - avoid unreadable nested maps, filters, reduces, and inline transformations.
- `no-component-loops.md` - avoid imperative render preparation and unclear orchestration; allow clear local iteration.
- `no-unapproved-test-infrastructure.md` - use relevant project tests without introducing unapproved test tooling or broad suites.

## Use Rule

A skill should read `common/anti-patterns.md` first, then load only the concrete template that matches the current code risk.
