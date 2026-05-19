---
id: 'agents.skills.frontend-design-workflow.references.generative-ui'
title: 'Generative UI'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-design-workflow'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/canvas'
    - 'agents/reference'
parent:
    - '[[skills/frontend-design-workflow/SKILL|Frontend Design Workflow]]'
related:
    []
depends_on:
    - '[[skills/frontend-design-workflow/SKILL|Frontend Design Workflow]]'
---

# Generative UI

Use this reference only when the user explicitly asks for canvas, generative,
algorithmic, game-like, or web-art UI.

## Core rules

- Treat generative visuals as product UI only when they serve the requested
  experience.
- Keep the implementation inside the repo's existing framework and build system.
- Do not introduce p5.js, Three.js, custom bundlers, artifact scaffolds, or CDN
  dependencies without explicit user approval.
- Use seeded randomness only when reproducibility matters to the request.
- Keep parameters tied to meaningful user-facing controls rather than exposing a
  large debugging panel.
- Verify that the canvas or animated surface renders, resizes, and remains
  usable alongside surrounding React UI.

## Review points

- Check performance on the target viewport and expected device class.
- Check reduced-motion behavior for animation-heavy work.
- Check that controls, labels, and focus states remain accessible.
- Check that generated visuals do not obscure critical content.
