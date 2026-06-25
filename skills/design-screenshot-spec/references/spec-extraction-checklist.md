---
id: 'agents.skills.design-screenshot-spec.references.spec-extraction-checklist'
title: 'Spec Extraction Checklist'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'design-screenshot-spec'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'agents/reference'
parent:
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
related:
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
depends_on:
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
---

# Spec Extraction Checklist

## Source Inventory

- List each screenshot, exported asset, copied inspect panel, and written note.
- Group artifacts by screen, component, viewport, and state.
- Record missing desktop, tablet, mobile, hover, focus, disabled, loading, empty,
  and error states.

## Visual Extraction

- Layout: frame size, section order, containment, alignment, stack direction,
  columns, grids, fixed or fluid regions.
- Typography: family, weight, size, line height, alignment, transform, color,
  max width, wrapping behavior.
- Color: page background, surface, text, border, icon, accent, success, warning,
  error, disabled.
- Spacing: padding, gaps, margins, section rhythm, control density.
- Shape and effects: border width, radius, shadow, blur, opacity, overlays.
- Assets: images, icons, logos, illustrations, aspect ratios, crop behavior.
- Interactions: controls, hover, focus, selected, active, disabled, loading,
  validation, navigation.
- Responsive behavior: what stacks, hides, reorders, resizes, or changes density.

## Confidence Labels

- `source-provided`: copied inspect value, exported value, or explicit note.
- `screenshot-inferred`: estimated from a visible screenshot.
- `unknown`: not visible or not provided.

## Spec Quality Gate

- Do not invent hidden details.
- Do not convert screenshot estimates into global design tokens.
- Ask for missing artifacts when the uncertainty would materially change the
  implementation.

