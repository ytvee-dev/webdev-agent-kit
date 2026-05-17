---
id: 'agents.skills.screenshot-design-inspector.references.device-mapping'
title: 'Device Mapping'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'screenshot-design-inspector'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'agents/reference'
parent:
    - '[[skills/screenshot-design-inspector/SKILL|Screenshot Design Inspector]]'
related:
    []
depends_on:
    - '[[skills/screenshot-design-inspector/SKILL|Screenshot Design Inspector]]'
---

# Device Mapping

- Treat a single wide screenshot as desktop unless the user says otherwise.
- Treat a narrow portrait screenshot as mobile unless the user says otherwise.
- Treat intermediate-width screenshots as tablet when the layout clearly sits
  between desktop and mobile.
- If multiple screenshots are present, compare typography and spacing deltas
  instead of assuming they stay constant across breakpoints.
