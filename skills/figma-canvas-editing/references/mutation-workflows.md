---
id: 'agents.skills.figma-canvas-editing.references.mutation-workflows'
title: 'Mutation Workflows'
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
    - '[[skills/figma-screen-generation/SKILL|Figma Screen Generation]]'
    - '[[skills/figma-design-system-builder/SKILL|Figma Design System Builder]]'
depends_on:
    - '[[skills/figma-canvas-editing/SKILL|Figma Canvas Editing]]'
---

# Mutation Workflows

Use this reference for multi-step Figma editing.

## Section Map

- `Default workflow` for safe sequential mutation.
- `Inspection before write` for convention discovery.
- `Companion skills` for screen and library orchestration.

## Default workflow

1. Inspect first with a read-only query or metadata call.
2. Make one logical change per `use_figma` call.
3. Return IDs and any other continuation data.
4. Validate structure or screenshot output before the next step.
5. Continue only from confirmed file state.

## Inspection before write

- Check pages, components, variables, naming, and existing layout patterns
  before creating new structures.
- Match existing conventions in the target file instead of imposing new names or
  token shapes.
- Use higher-level orchestration skills when the task is about a whole screen or
  a whole design system rather than a single mutation.

## Companion skills

- Use `figma-screen-generation` when the deliverable is a screen, page, or
  view assembled from multiple sections.
- Use `figma-design-system-builder` when the deliverable is a token system,
  component library, or design-system documentation surface.
