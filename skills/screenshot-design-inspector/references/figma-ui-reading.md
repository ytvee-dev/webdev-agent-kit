---
id: 'agents.skills.screenshot-design-inspector.references.figma-ui-reading'
title: 'Figma UI Reading'
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

# Figma UI Reading

Use this reference when supplied screenshots, exports, or copied inspect panels
expose Figma-like UI labels.

## Text layers

- Read font family or displayed font label.
- Read style and weight.
- Read font size.
- Read line height.
- Read letter spacing.
- Read fill color.
- Read text box width and frame width when visible.

## Layout and spacing

- Read frame width for each supplied device class.
- Read visible gaps, padding, and alignment values.
- Compare desktop, tablet, and mobile values independently.

## Confidence

- Mark values from Figma Dev Mode or inspect panels as high confidence.
- Mark values inferred from screenshots as medium or low confidence.
- Ask the user when a low-confidence value affects implementation.
