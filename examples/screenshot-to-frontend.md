---
id: 'agents.examples.screenshot-to-frontend'
title: 'Screenshot To Frontend Example'
doc_type: 'example'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/example'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
depends_on: []
---

# Screenshot To Frontend Example

User prompt:

```text
Use these screenshots and inspect notes to implement the pricing page in the
current app. Match desktop and mobile.
```

What to expect:

1. The agent describes visible layout, spacing, typography and states.
2. It checks the existing components and styles, then implements the page.
3. It runs relevant existing checks and compares the rendered page when a
   browser is available. It reports any visual checks it could not perform.

A screenshot cannot show every interaction. The agent should ask about missing
product behavior before implementing it. It should not install a UI library,
add tests or fetch a live design source merely because you supplied an image.

When a Figma link is supplied instead, the same intake skill tries available
MCP reads and then browser/computer use; it requests image fallback only after
available live paths cannot supply the needed evidence.
