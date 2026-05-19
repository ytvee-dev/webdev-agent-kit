---
id: 'agents.skills.figma-design-to-code.references.implementation-flow'
title: 'Implementation Flow'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'figma-design-to-code'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/figma'
    - 'agents/reference'
parent:
    - '[[skills/figma-design-to-code/SKILL|Figma Design To Code]]'
related:
    - '[[skills/figma-design-reader/SKILL|Figma Design Reader]]'
    - '[[skills/frontend-design-workflow/SKILL|Frontend Design Workflow]]'
depends_on:
    - '[[skills/figma-design-to-code/SKILL|Figma Design To Code]]'
---

# Implementation Flow

Use this reference when translating Figma designs into code in the repo.

## Section Map

- `Required flow` for Figma-to-code order.
- `Translation rules` for mapping design to repo conventions.
- `Validation` for visual signoff and fallback.

## Required flow

1. Parse the Figma URL or selected node.
2. Fetch `get_design_context`.
3. Fetch `get_screenshot` for the same node.
4. Download or reference required assets from the Figma MCP payload.
5. Read the touched code area and map the design onto existing repo patterns.
6. Implement with the repo's owned styling and component system.
7. Validate against the Figma screenshot before finishing.

## Translation rules

- Treat the MCP output as an explanation of layout and behavior, not as final
  code style.
- Replace any Tailwind-like output or generic Figma code with the repo's real
  tokens, CSS conventions, and framework primitives.
- Prefer extending an existing component over creating a parallel one.
- Use Figma variables and styles as intent, then bind them to the repo's design
  tokens or local equivalents.
- If the design and the repo's reusable token system conflict, prefer the repo's
  owned token model and document the visual adjustment.

## Validation

- Validate spacing, typography hierarchy, assets, and interaction states against
  the screenshot or node states fetched from Figma.
- If the design source is truncated or incomplete, say so and narrow the node
  read before continuing.
- If Figma becomes unavailable mid-task, explicitly switch to screenshot-based
  interpretation instead of silently guessing.
