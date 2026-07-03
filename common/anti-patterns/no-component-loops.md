---
id: 'agents.common.anti-patterns.no-component-loops'
title: 'No Unclear Render Orchestration Loops'
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

# No Unclear Render Orchestration Loops

## Rule

Do not use imperative loops for render-side mutation, hidden component-body preparation, or orchestration that becomes harder to understand than named transformations.

Use a normal local loop when it is the clearest correct solution, especially for early exit, indexed traversal, bounded accumulation, or performance-sensitive work. Keep it named or isolated when the body contains meaningful behavior.

## Exception

Inside React render paths, prefer immutable named helpers and readable collection transformations. Move side effects and multi-step orchestration to the existing owner rather than hiding them in render preparation.

## Apply When

Use this whenever implementation, bugfix, refactor, or review touches collection handling, list rendering, transformations, adapters, selectors, or UI actions. Judge clarity and behavior instead of banning syntax globally.
