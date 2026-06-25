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

- Use `figma-design-to-code` for source-material-to-code intake when
  user-provided Figma-derived artifacts are available.
- If the user provides only a Figma URL, node, or file key, ask for screenshots,
  exports, copied inspect values, token/style notes, written specs, or a design
  brief before implementing.
- Keep `nextjs-app-router` focused on route composition, metadata, layouts,
  loading/error states, and server/client boundaries around that UI.
- Reuse existing route-level patterns, layout primitives, and styling tokens
  instead of hardcoded values.
- Use `screenshot-design-inspector` only when screenshots are the primary
  supplied source and no Figma-specific source context is available.
