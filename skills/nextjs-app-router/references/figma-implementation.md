---
id: 'agents.skills.nextjs-app-router.references.figma-implementation'
title: 'Figma Implementation'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'nextjs-app-router'
tags:
    - 'agents/skill-package'
    - 'frontend/nextjs'
    - 'agents/reference'
parent:
    - '[[skills/nextjs-app-router/SKILL|Next.js App Router]]'
related:
    []
depends_on:
    - '[[skills/nextjs-app-router/SKILL|Next.js App Router]]'
---

# Figma Implementation

- Inspect the design in Figma before writing UI code.
- If Figma access fails, ask the user for screenshots and use
  `screenshot-design-inspector`.
- Reuse existing tokens, layout primitives, and component patterns first.
- Read typography deliberately: size, family, weight, line height, spacing, and
  color from Figma when available.
- With desktop, tablet, and mobile screenshots, compare typography and spacing
  per device class instead of reusing one size across breakpoints.
- If a value is only visible in screenshots, infer cautiously and ask the user
  when the value is not trustworthy enough to implement directly.
- Match the design's hierarchy and spacing, then adapt it to real breakpoints.
- Avoid pixel-perfect hardcoding that bypasses the project's styling system.
- If the design requires a new reusable token or abstraction, introduce it
  only with user approval instead of hiding it inside one component.
