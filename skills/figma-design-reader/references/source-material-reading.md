---
id: 'agents.skills.figma-design-reader.references.source-material-reading'
title: 'Source Material Reading'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'figma-design-reader'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/figma'
    - 'agents/reference'
parent:
    - '[[skills/figma-design-reader/SKILL|Figma Design Reader]]'
related:
    - '[[skills/figma-design-to-code/SKILL|Figma Design To Code]]'
depends_on:
    - '[[skills/figma-design-reader/SKILL|Figma Design Reader]]'
---

# Source Material Reading

Use this reference when analyzing user-provided Figma-derived artifacts without
opening Figma or changing the canvas.

## Section Map

- `Required flow` for source-material intake.
- `Reading priorities` for what to extract from supplied artifacts.
- `Missing material` for URL-only prompts and incomplete specs.

## Required flow

1. Inventory the supplied artifacts before analysis:
   screenshots, exports, copied inspect values, variables/styles notes, token
   tables, written specs, briefs, or repo references.
2. If the user supplies only a Figma URL, node, or file key, ask for source
   material and stop the Figma-specific workflow until it is provided.
3. Treat copied inspect values, exported assets, and written token/spec notes as
   higher confidence than pixel estimates from screenshots.
4. Compare every visual claim against the supplied artifact that supports it.
5. Record missing states, breakpoints, component variants, and assets instead of
   inventing them.

## Reading priorities

- Layout structure: frames, nesting, auto-layout direction, constraints,
  sizing behavior, and section boundaries.
- Typography: style hierarchy, weight, size, line height, alignment, and text
  grouping.
- Variables and tokens: color, spacing, radius, effect, and style references.
- Components and variants: whether the design uses reusable components or
  one-off composition.
- Assets: icons, images, SVGs, exported files, or asset notes supplied by the
  user.

## Missing material

- If a Figma link lacks artifacts, ask for screenshots, exports, copied inspect
  values, token/spec notes, or a written brief.
- If a screenshot omits responsive states, state transitions, hover/focus
  variants, or assets, mark those gaps explicitly.
- If source materials conflict, prefer copied/exported values over inferred
  screenshot estimates and call out the conflict.
