---
id: 'agents.skills.figma-design-system-builder.references.phase-plan'
title: 'Phase Plan'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'figma-design-system-builder'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/figma'
    - 'agents/reference'
parent:
    - '[[skills/figma-design-system-builder/SKILL|Figma Design System Builder]]'
related:
    - '[[skills/figma-design-system-builder/references/component-library-rules|Component Library Rules]]'
depends_on:
    - '[[skills/figma-design-system-builder/SKILL|Figma Design System Builder]]'
---

# Phase Plan

Use this reference for phased design-system work in Figma.

## Section Map

- `Phase order` for the required build sequence.
- `Checkpoints` for user confirmation and validation.
- `Anti-patterns` for workflow mistakes that break recoverability.

## Phase order

1. Discovery:
   inspect codebase tokens, component families, Figma file conventions, and
   existing libraries before writing anything.
2. Foundations:
   create collections, modes, primitives, semantic variables, text styles, and
   effect styles.
3. File structure:
   create cover, foundations, component, and utility pages.
4. Components:
   build component families one at a time with variable bindings and variant
   structure.
5. Final QA:
   run naming, unresolved-binding, and screenshot review passes.

## Checkpoints

- Get explicit approval after scope lock before creation.
- Validate token creation before moving to component work.
- Validate each component family before the next one.
- Rehydrate state from current file structure if the workflow spans multiple
  long turns.

## Anti-patterns

- Building components before foundations exist.
- Hardcoding visual values when reusable variables or styles should exist.
- Creating too many unrelated entities in one mutation call.
- Advancing to the next phase without visual or structural validation.
