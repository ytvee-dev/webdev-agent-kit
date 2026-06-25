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

Use this reference when translating user-provided Figma-derived source material
into code in the repo.

## Section Map

- `Required flow` for source-material-to-code order.
- `Translation rules` for mapping design to repo conventions.
- `Validation` for visual signoff and fallback.

## Required flow

1. Inventory supplied screenshots, exports, copied inspect values, token/style
   notes, written specs, briefs, and assets.
2. If only a Figma URL, node, or file key is provided, ask for source material
   before implementation.
3. Read the touched code area and map the design onto existing repo patterns.
4. Implement with the repo's owned styling and component system.
5. Validate against supplied screenshots, exports, specs, and intended states
   before finishing.

## Translation rules

- Treat supplied Figma-derived artifacts as an explanation of layout and
  behavior, not as final code style.
- Replace any Tailwind-like output or generic Figma code with the repo's real
  tokens, CSS conventions, and framework primitives.
- Prefer extending an existing component over creating a parallel one.
- Use copied variables, style values, and token notes as intent, then bind them
  to the repo's design tokens or local equivalents.
- If the design and the repo's reusable token system conflict, prefer the repo's
  owned token model and document the visual adjustment.

## Validation

- Validate spacing, typography hierarchy, assets, and interaction states against
  the supplied screenshots, exports, or specs.
- If the design source is incomplete, say so and ask for the missing artifact
  when it affects implementation.
- Do not silently guess missing Figma states, assets, tokens, or breakpoints.
