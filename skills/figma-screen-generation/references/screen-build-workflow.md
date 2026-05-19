---
id: 'agents.skills.figma-screen-generation.references.screen-build-workflow'
title: 'Screen Build Workflow'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'figma-screen-generation'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/figma'
    - 'agents/reference'
parent:
    - '[[skills/figma-screen-generation/SKILL|Figma Screen Generation]]'
related:
    - '[[skills/figma-canvas-editing/SKILL|Figma Canvas Editing]]'
depends_on:
    - '[[skills/figma-screen-generation/SKILL|Figma Screen Generation]]'
---

# Screen Build Workflow

Use this reference when building screens in Figma.

## Section Map

- `Preparation` for understanding the screen and file target.
- `Build flow` for section-by-section assembly.
- `Validation` for screen-level review.

## Preparation

- Read the source code or spec and identify the major sections first.
- Inspect the target file for existing pages, components, variables, and naming
  conventions before creating anything.
- Create or locate the wrapper frame before building nested sections.

## Build flow

1. Build one major section per mutation step.
2. Import or instantiate reusable design-system components when they exist.
3. Bind colors, spacing, radii, and styles to variables instead of hardcoding.
4. Return section and wrapper IDs after each step.
5. Re-read or validate before continuing to the next section.

## Validation

- Validate screenshots at the section level, not only the full page.
- Check placeholder text, spacing, clipping, and wrong variants before
  proceeding.
- When updating an existing screen, mutate or swap the existing structure
  rather than rebuilding the whole page unless replacement is explicitly safer.
