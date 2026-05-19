---
id: 'agents.skills.figma-design-system-builder.references.component-library-rules'
title: 'Component Library Rules'
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
    - '[[skills/figma-canvas-editing/SKILL|Figma Canvas Editing]]'
depends_on:
    - '[[skills/figma-design-system-builder/SKILL|Figma Design System Builder]]'
---

# Component Library Rules

Use this reference when creating or updating Figma library entities.

## Section Map

- `Variable rules` for collections, scopes, and syntax.
- `Component rules` for families, variants, and bindings.
- `Documentation rules` for library pages and validation.

## Variable rules

- Create primitive and semantic layers deliberately instead of duplicating raw
  values.
- Set scopes explicitly on variables instead of leaving broad defaults.
- Keep code syntax aligned with the codebase token naming where the design
  system expects it.
- Import or reuse existing library variables when the target file already has
  the correct source of truth.

## Component rules

- Build one component family at a time.
- Prefer reusable component properties and instance-swap patterns over variant
  explosion.
- Bind fills, strokes, spacing, and radii to variables whenever those concepts
  exist in the library model.
- Validate structure and screenshots before continuing.

## Documentation rules

- Create dedicated foundations and component pages instead of leaving raw
  components scattered on the canvas.
- Keep page naming, variant naming, and component naming deterministic.
- Track created page and component IDs so later updates can mutate the existing
  library rather than duplicating it.
