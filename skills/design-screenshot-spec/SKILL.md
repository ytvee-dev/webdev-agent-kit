---
name: design-screenshot-spec
description: Use when the user supplies Figma screenshots, copied visual inspect panels, exported assets, or design notes and needs a strict Design Implementation Spec for frontend implementation. Do not use Figma MCP or live Figma links; ask for screenshots or source artifacts when only a URL, file key, node id, Figma whiteboard reference is provided.
id: 'agents.skills.design-screenshot-spec.skill'
title: 'Design Screenshot Spec'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'design-screenshot-spec'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/spec'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/design-screenshot-spec/references/spec-extraction-checklist|Spec Extraction Checklist]]'
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Design Screenshot Spec

## Purpose

Convert user-supplied Figma screenshots, copied visual inspect panels, exported
assets, and design notes into a strict `Design Implementation Spec` for a
frontend implementer.

## When To Use

- The user sends screenshots of Figma frames, components, screens, or inspect
  panels.
- The user asks to analyze a visual design before implementation.
- The next step is frontend layout work and the implementer needs a structured
  spec.

## When Not To Use

- The user asks for live Figma inspection, canvas editing, file creation, Figma
  whiteboard workflows, design-system generation, or Code Connect.
- The user supplies only a Figma URL, file key, or node id without screenshots
  or copied design material.
- The user already provides a complete `Design Implementation Spec` and asks to
  implement it. Use `frontend-layout-implementer`.

## Required Context

1. Read `AGENTS.md`.
2. Confirm the classified task is `design-spec` or design intake for later
   frontend implementation.
3. Read `common/approved-patterns.md`.
4. Read `common/anti-patterns.md`.
5. Read `project/design-reference-profile.md` when present.
6. Read `references/spec-extraction-checklist.md`.

## Tool Contract

- Do not use Figma MCP.
- Use Visual Reference MCP when available for user-supplied image references.
- Use Design Spec MCP when available to store or read structured specs.
- If those MCP servers are unavailable, work from attached images, local image
  files, copied inspect text, and user-provided notes.
- Do not open live Figma links.

## Workflow

1. Inventory all supplied artifacts: screenshots, inspect panels, exported
   assets, dimensions, fonts, colors, states, notes, and target screens.
2. If only a Figma URL, file key, node id, Figma whiteboard reference is present,
   stop and ask for screenshots, exported assets, copied inspect values, or a
   written brief.
3. Group screenshots by screen, component, state, and viewport. For each
   screenshot, record the visible frame or viewport width, height, state,
   screen or component ownership, and confidence.
4. Treat each screenshot or design-frame size as a reference coordinate system,
   not as a production container cap. Record whether containment is explicitly
   visible and capture desktop edge anchors plus expected behavior beyond the
   reference viewport.
5. Extract visible layout, hierarchy, typography, color, spacing, sizing,
   radius, shadow, assets, states, and responsive behavior.
6. For typography, prefer copied inspect values or selected-text properties for
   `font-family`, `font-size`, `font-weight`, `line-height`, color, alignment,
   max width, and wrapping. When properties are unavailable, estimate from the
   screenshot and mark each estimate as `screenshot-inferred`.
7. For spacing, separate outside margins, section rhythm, inter-component gaps,
   container padding, and internal control padding instead of merging them into
   one generic gap value.
8. Mark each value as `source-provided`, `screenshot-inferred`, or `unknown`.
9. Resolve conflicts by preferring copied inspect values and exported values
   over screenshot estimates.
10. Ask the user about disputed or low-confidence values when the answer changes
   layout, responsive behavior, visual hierarchy, typography, or implementation
   acceptance.
11. Produce the `Design Implementation Spec` and stop unless the user also asks
    for implementation.
12. Route to `frontend-design-director` before implementation when the supplied
    material needs redesign, polish, distinctive visual direction, anti-template
    critique, interface-copy stance, motion stance, or visual acceptance
    criteria.

## Output Contract

Return a `Design Implementation Spec` with these sections:

- `Source Inventory`
- `Screen And Component Scope`
- `Layout Structure`
- `Typography`
- `Color And Effects`
- `Spacing And Sizing`
- `Assets`
- `States And Interactions`
- `Responsive Behavior`
- `Accessibility Notes`
- `Implementation Acceptance Criteria`
- `Confidence And Unknowns`

## Validation Gates

- Every concrete value must cite its source confidence.
- `Source Inventory` must record each screenshot's viewport or frame size when
  visible or provided.
- `Spacing And Sizing` must distinguish measured or estimated margins, section
  rhythm, inter-component gaps, container padding, and internal control padding
  with confidence labels.
- `Typography` must distinguish inspect-provided text properties from inferred
  font family, size, weight, line height, color, alignment, and wrapping.
- `Responsive Behavior` must include viewport-aware notes based on supplied
  screenshot widths, desktop edge anchors, and behavior beyond each reference
  viewport, and must mark inferred intermediate behavior explicitly.
- Screenshot or design-frame dimensions must not become runtime `max-width`,
  fixed container dimensions, or equivalent caps without source evidence of a
  centered container and an explicit responsive rationale.
- Missing states, assets, breakpoints, and token names must be explicit.
- Disputed values that materially affect implementation must be asked back to
  the user or listed as unresolved questions.
- The spec must be usable by `frontend-layout-implementer` without guessing the
  target layout intent.
- When visual judgment is needed, the handoff must name
  `frontend-design-director` before implementation.
- The response must not mention using Figma MCP or live Figma inspection.

## Trigger Evals

Should trigger:

- "Here are Figma screenshots with dimensions and colors; write the layout spec."
- "Read these frame screenshots and inspect panels before coding."
- "Create a frontend implementation spec from these design screenshots."

Should not trigger:

- "Implement this existing Design Implementation Spec."
- "Open this Figma node and inspect it."
- "Create a new Figma whiteboard."

## Reference Map

- `references/spec-extraction-checklist.md`
- `skills/frontend-design-director/SKILL.md`
