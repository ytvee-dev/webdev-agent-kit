---
id: 'agents.skills.frontend-visual-qa.references.visual-qa-checklist'
title: 'Visual QA Checklist'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-visual-qa'
tags:
    - 'agents/skill-package'
    - 'frontend/verification'
    - 'agents/reference'
parent:
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
related:
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
depends_on:
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
---

# Visual QA Checklist

## Browser Checks

- Page or route loads without blocking runtime errors.
- Console has no unexpected errors or hydration/render failures.
- Primary content is visible above the fold at required viewports.
- Layout does not overflow horizontally.
- Text fits containers and wraps acceptably.
- Fixed headers, sidebars, modals, and toolbars do not occlude content.

## Viewport Checks

- Desktop: verify spacing, hierarchy, and multi-column layout.
- Tablet: verify reflow and intermediate widths when supplied by the spec.
- Mobile: verify stacking, tap targets, text wrapping, and viewport fit.

## Visual Comparison

- Compare layout structure, alignment, spacing rhythm, typography hierarchy,
  colors, borders, radii, shadows, assets, and states.
- Record each material mismatch with viewport and visible evidence.
- Distinguish approved project-native deviations from accidental mismatches.

## Interaction Checks

- Hover, focus, active, selected, disabled, loading, empty, and error states
  match the spec when supplied.
- Keyboard focus remains visible for interactive controls in scope.

