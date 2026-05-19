---
id: 'agents.skills.figma-canvas-editing.references.plugin-api-rules'
title: 'Plugin Api Rules'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'figma-canvas-editing'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/figma'
    - 'agents/reference'
parent:
    - '[[skills/figma-canvas-editing/SKILL|Figma Canvas Editing]]'
related:
    - '[[skills/figma-canvas-editing/references/mutation-workflows|Mutation Workflows]]'
depends_on:
    - '[[skills/figma-canvas-editing/SKILL|Figma Canvas Editing]]'
---

# Plugin API Rules

Use this reference before any `use_figma` mutation.

## Section Map

- `Output rules` for returning data.
- `Mutation rules` for safe Plugin API usage.
- `Validation rules` for post-mutation checks.

## Output rules

- Use `return` as the output channel.
- Do not use `figma.closePlugin()`, `figma.notify()`, or `console.log()` as the
  result path.
- Return all created and mutated node IDs in structured data.

## Mutation rules

- Write plain JavaScript with top-level `await`.
- Load fonts before changing text.
- Use `await figma.setCurrentPageAsync(page)` instead of synchronous page
  switching.
- Reassign fills and strokes instead of mutating them in place.
- Set auto-layout sizing properties only when the node is in the correct parent
  context.
- Treat colors as `0-1` channel values.
- Tag or otherwise track created entities so the next call can reference them
  explicitly.

## Validation rules

- Stop on errors and read the error before retrying.
- Re-check structure with metadata or a follow-up read before stacking more
  mutations on top.
- When the result is visually important, capture a screenshot after the mutation
  milestone instead of assuming the structure implies correctness.
