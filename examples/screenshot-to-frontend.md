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

Expected skill chain:

```text
design-screenshot-spec
-> frontend-design-director when visual judgment is needed
-> frontend-architecture-planner when route or ownership boundaries matter
-> frontend-layout-implementer
-> frontend-linter-manager when lint exists
-> frontend-visual-qa
-> frontend-quality-reviewer when review is requested or appropriate
```

Expected exclusions:

- no Figma MCP;
- no UI component library install;
- no testing workflow creation;
- no package installation without approval.
