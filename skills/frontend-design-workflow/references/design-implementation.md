---
id: 'agents.skills.frontend-design-workflow.references.design-implementation'
title: 'Design Implementation'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-design-workflow'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'agents/reference'
parent:
    - '[[skills/frontend-design-workflow/SKILL|Frontend Design Workflow]]'
related:
    - '[[skills/screenshot-design-inspector/SKILL|Screenshot Design Inspector]]'
depends_on:
    - '[[skills/frontend-design-workflow/SKILL|Frontend Design Workflow]]'
---

# Design Implementation

Use this reference for Figma, screenshot, redesign, styling polish, and
responsive UI work.

## Design reading

- Identify purpose, audience, content density, and expected workflow before
  choosing layout or decoration.
- Extract hierarchy deliberately: heading scale, body text, metadata, controls,
  emphasis, and grouping.
- Read spacing as relationships between elements, not isolated pixel values.
- Compare desktop, tablet, and mobile behavior separately when multiple
  breakpoints are available.
- Mark low-confidence screenshot-derived values instead of treating them as
  exact design tokens.

## Implementation rules

- Use existing repo primitives and tokens before adding local values.
- Keep styles local to the component or route unless the repo already has a
  shared primitive for the pattern.
- Use semantic class names based on role rather than visual appearance.
- Keep UI elements stable across loading, hover, focus, and dynamic content.
- Ensure text fits its container at supported viewport widths.
- Prefer layout patterns that support scanning, comparison, and repeated use for
  operational tools; reserve expressive composition for public pages, editorial
  surfaces, games, or explicitly creative requests.
- Document design deviations only when they affect implementation or user
  expectations.

## Figma and screenshots

- Use configured Figma capabilities first when a Figma URL or node is provided.
- Use `figma-design-reader` for read-only Figma intake and
  `figma-design-to-code` when the deliverable is repo implementation from
  Figma.
- If Figma is unavailable, request screenshots and use
  `screenshot-design-inspector` before implementing from guesswork.
- Recreate responsive behavior and interaction states with existing repo
  patterns instead of copying one static viewport blindly.
- Ask before adding reusable tokens or design-system primitives that do not
  already exist.
