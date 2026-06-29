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
- Record each screenshot's visible or provided width, height, viewport or frame
  label, state, and screen or component ownership.
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

## Measurement Discipline

- Record measured or inferred spacing with element pair, axis, value, viewport,
  and confidence.
- Separate outside margins, section rhythm, inter-component gaps, container
  padding, and internal control padding.
- Measure spacing between actual neighboring components, not only between
  wrapper edges, when the screenshot makes both visible.
- Keep screenshot-derived pixel estimates local to the spec. Do not convert
  estimates into global spacing, typography, or breakpoint tokens.
- Ask the user when two plausible measurements would produce materially
  different layout or responsive behavior.

## Typography Extraction

- Prefer copied inspect panels, selected text properties, exported values, and
  explicit notes over screenshot estimates.
- For each important text style, record family, weight, size, line height,
  alignment, transform, color, max width, and wrapping behavior when visible or
  provided.
- When inspect values are unavailable, estimate visible font size, weight, line
  height, and likely family from the screenshot and mark each value as
  `screenshot-inferred`.
- Keep low-confidence font families, style names, and token names as
  `unknown` or `screenshot-inferred`; do not present them as source-provided
  facts.
- Ask the user when a typography ambiguity changes hierarchy, wrapping, or
  implementation acceptance.

## Viewport-Aware Responsive Analysis

- Use the actual supplied screenshot width before labeling a reference as
  desktop, tablet, or mobile.
- Create a viewport matrix that maps each supplied width to visible layout,
  density, typography scale, content order, hidden elements, and interaction
  state when those details are visible.
- Describe how the layout should stack, reflow, hide, resize, crop, or change
  density between supplied widths.
- When intermediate viewport sizes are not supplied, provide conservative
  adaptive guidance and label it `screenshot-inferred`.
- Ask for another screenshot or confirmation when the missing intermediate
  behavior would materially change implementation.

## Confidence Labels

- `source-provided`: copied inspect value, exported value, or explicit note.
- `screenshot-inferred`: estimated from a visible screenshot.
- `unknown`: not visible or not provided.

## Spec Quality Gate

- Do not invent hidden details.
- Do not convert screenshot estimates into global design tokens.
- Ask for missing artifacts when the uncertainty would materially change the
  implementation.
- The final spec must include measured or inferred spacing, typography, and
  viewport behavior with confidence labels rather than generic descriptions.

