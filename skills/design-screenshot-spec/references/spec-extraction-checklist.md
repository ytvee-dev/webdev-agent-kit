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

Sections cover source identity, selected-layer evidence, visual measurements,
typography, responsive analysis, and confidence. Apply the same component-level
ledger to MCP reads, browser inspection, and screenshot-only intake.

## Source Inventory

- List each link, successful MCP read, browser capture, supplied screenshot,
  exported asset, copied inspect panel, and written note with a source ID.
- Group artifacts by screen, component, viewport, and state.
- Record each screenshot's visible or provided width, height, viewport or frame
  label, state, and screen or component ownership.
- Record missing desktop, tablet, mobile, hover, focus, disabled, loading, empty,
  and error states.

## Selected Layer And Property Evidence

- First inspect the entire image: canvas, layer tree, selection outline,
  breadcrumb, right-side properties, and any prototype panel. Identify what is
  selected, not merely which component is visually prominent.
- For each component capture source ID, frame/parent/layer path, node ID when
  available, instance/variant/state, viewport, mode, and evidence location.
- Attribute panel values only to the confirmed selection. Parent-frame padding
  is not button padding; text fill is not a background; a selected icon's size
  is not the surrounding control size. Mixed or multi-selected values stay
  ambiguous until selection-specific evidence is available.
- Read every relevant visible panel section and text run: typography (including
  letter spacing), dimensions and sizing mode, padding/gap, constraints, fill
  color and alpha, border, radii, shadow/blur, component properties, and tokens.
  Record literal units and names rather than converting them from memory.
- Use original-resolution images and crops/zoom supported by the host to read
  small values. Preserve the image ID and crop location. Record device scale and
  canvas zoom when known; screen pixels do not automatically equal CSS pixels.
- Do not sample selection outlines, editor chrome, or anti-aliased text edges
  as design colors. Readable property values are exact for that selection;
  sampled colors and OCR remain estimates until visually confirmed.
- Inspect each unique component/state; link repeated instances to the verified
  base and record overrides. Do not extrapolate one selected component's values
  across an entire screen merely because controls look similar.
- When identity, units, or panel text cannot be read, mark the specific property
  unknown and request a focused capture with both selection and panel visible.
  Do not invent hidden layers, fonts, variants, token names, or exact hex values.

Use a compact ledger row per component/state:

`source | selection/parent | variant/state/mode | property/value/unit | evidence location | confidence | gap`

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

- Treat screenshot and design-frame dimensions as coordinate systems for
  measurement, not as production `max-width` or fixed container dimensions.
- Add a runtime container cap only when the source explicitly shows a centered
  container boundary; record that evidence and its responsive rationale.
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

- Prefer matching live properties, copied inspect panels, selected text properties, exported values, and
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
- For every desktop reference, record left, right, top, and bottom edge anchors
  for major content and media, including which anchors stay attached to the
  viewport and which belong to an explicitly evidenced container.
- Record evidenced behavior beyond the widest reference viewport: which
  regions remain edge-anchored, grow, cap, crop, or expose background.
- Describe observed stacking, reflow, hiding, resizing, cropping, and density
  differences between supplied widths; frame dimensions alone prove no breakpoint.
- When intermediate or wider behavior is not evidenced, label it `unknown` and
  propose adaptive behavior for user confirmation. Keep proposals out of the
  accepted implementation contract until answered.
- Ask for another screenshot or confirmation when the missing intermediate
  behavior would materially change implementation.

## Confidence Labels

- `source-provided`: successful MCP property read, legible property panel for
  the identified selection, copied inspect value, export, or explicit note.
- `screenshot-inferred`: estimated from a visible screenshot.
- `unknown`: not visible or not provided.

## Spec Quality Gate

- Do not invent hidden details.
- Do not convert screenshot estimates into global design tokens.
- Do not transfer screenshot or design-frame dimensions into runtime container
  caps without explicit source evidence and a responsive justification.
- Ask for missing artifacts when the uncertainty would materially change the
  implementation.
- The final spec must include measured or inferred spacing, typography, and
  viewport behavior with confidence labels rather than generic descriptions.
- Complete `product-behavior-review.md` after extraction; every unresolved
  product/design choice blocks its dependent implementation until answered.
