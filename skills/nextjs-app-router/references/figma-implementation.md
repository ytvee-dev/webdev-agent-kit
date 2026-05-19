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

- Use `figma-design-to-code` for the actual Figma-to-code intake and design
  reading flow.
- Keep `nextjs-app-router` focused on route composition, metadata, layouts,
  loading/error states, and server/client boundaries around that UI.
- Reuse existing route-level patterns, layout primitives, and styling tokens
  instead of hardcoded values.
- If Figma access fails, ask the user for screenshots and use
  `screenshot-design-inspector`.
