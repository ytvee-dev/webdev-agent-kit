---
id: 'agents.skills.figma-design-reader.references.mcp-reading'
title: 'Mcp Reading'
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

# MCP Reading

Use this reference when reading Figma through MCP without mutating the canvas.

## Section Map

- `Required flow` for tool order.
- `Reading priorities` for what to extract from Figma.
- `Failure modes` for MCP troubleshooting and fallback.

## Required flow

1. Start with the exact node whenever the user provides a precise URL or node ID.
2. Run `get_design_context` first when the target node is already known and the
   expected payload is not too large.
3. If the response is truncated or the exact node is unclear, run `get_metadata`
   to map the scenegraph, then re-fetch only the required node or children with
   `get_design_context`.
4. Run `get_screenshot` for the same node before making visual fidelity claims.
5. Read asset URLs and variable references from MCP output rather than
   redrawing them from memory.

## Reading priorities

- Layout structure: frames, nesting, auto-layout direction, constraints,
  sizing behavior, and section boundaries.
- Typography: style hierarchy, weight, size, line height, alignment, and text
  grouping.
- Variables and tokens: color, spacing, radius, effect, and style references.
- Components and variants: whether the design uses reusable components or
  one-off composition.
- Assets: icon, image, SVG, or localhost asset references returned by Figma MCP.

## Failure modes

- If Figma MCP access fails, do not invent design data. Ask for screenshots and
  use `screenshot-design-inspector`.
- If `get_design_context` is too large, narrow the query instead of working from
  a partial response.
- If a link lacks the exact node variant, ask for the precise node or state
  rather than assuming a sibling variant is equivalent.
