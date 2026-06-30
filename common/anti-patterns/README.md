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
related: []
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
- `no-component-loops.md` - do not use imperative loops inside React component bodies.
- `no-tests-for-components-or-functions.md` - do not create tests for components or functions.

## Use Rule

A skill should read `common/anti-patterns.md` first, then load only the concrete template that matches the current code risk.
