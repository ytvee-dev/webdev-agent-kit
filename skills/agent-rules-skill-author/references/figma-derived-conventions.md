---
id: 'agents.skills.agent-rules-skill-author.references.figma-derived-conventions'
title: 'Screenshot Derived Conventions'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'agent-rules-skill-author'
tags:
    - 'agents/skill-package'
    - 'agents/authoring'
    - 'frontend/design'
    - 'agents/reference'
parent:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules Skill Author]]'
related:
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
depends_on:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules Skill Author]]'
---

# Screenshot Derived Conventions

Use this reference when agent rules or skills need to encode behavior learned
from screenshot-derived frontend workflows.

## Layer Boundaries

- Put reusable screenshot intake and spec rules in `design-screenshot-spec`.
- Put reusable implementation rules in `frontend-layout-implementer`.
- Put reusable rendered verification rules in `frontend-visual-qa`.
- Put project-specific tokens, breakpoints, component paths, and local examples
  in `project/**`.
- Put generic source-first or project-native implementation policy in
  `common/**`.

## Routing Model

- Supplied screenshots or visual inspect panels -> `design-screenshot-spec`.
- `Design Implementation Spec` to frontend code -> `frontend-layout-implementer`.
- Rendered UI comparison against spec or references -> `frontend-visual-qa`.
- Project overlay refresh -> `project-context-adapter`.
- Skill authoring or rule maintenance -> `agent-rules-skill-author`.

## Prohibited Encodings

- Do not encode live Figma access as part of this bundle.
- Do not add Figma MCP dependencies.
- Do not route Figma whiteboard, canvas editing, file creation,
  design-system generation, or Code Connect tasks.
- Do not treat screenshots as exact tokens unless the value is copied from an
  inspect panel or explicit note.
- Do not put host-project facts in reusable skills.
