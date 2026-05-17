---
id: 'agents.skills.react-component-workflow.references.figma-implementation'
title: 'Figma Implementation'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'react-component-workflow'
tags:
    - 'agents/skill-package'
    - 'frontend/react'
    - 'agents/reference'
parent:
    - '[[skills/react-component-workflow/SKILL|React Component Workflow]]'
related:
    []
depends_on:
    - '[[skills/react-component-workflow/SKILL|React Component Workflow]]'
---

# Figma Implementation

- Start by inspecting the design in Figma.
- If Figma access fails, ask the user for screenshots and use
  `screenshot-design-inspector`.
- Reuse existing tokens and component primitives before inventing new ones.
- Read typography deliberately: size, family, weight, line height, spacing, and
  color from Figma when available.
- With desktop, tablet, and mobile screenshots, compare typography and spacing
  per device class instead of reusing one size across breakpoints.
- If a value is only visible in screenshots, infer cautiously and ask the user
  when the value is not trustworthy enough to implement directly.
- Match hierarchy, spacing, typography, and interaction states faithfully.
- Adapt width, stacking, and overflow behavior to real breakpoints.
- Document any design deviation that is required by the target codebase.
