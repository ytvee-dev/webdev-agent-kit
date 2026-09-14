---
id: 'agents.skills.agent-rules-skill-author.references.figma-derived-conventions'
title: 'Design Evidence Conventions'
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

# Design Evidence Conventions

Use this reference when agent rules or skills need to encode behavior learned
from live design inspection and screenshot-derived frontend workflows.

## Layer Boundaries

- Put reusable MCP/browser/image intake and spec rules in `design-screenshot-spec`.
- Put reusable implementation rules in `frontend-layout-implementer`.
- Put reusable rendered verification rules in `frontend-visual-qa`.
- Put project-specific tokens, breakpoints, component paths, and local examples
  in `project/**`.
- Put generic source-first or project-native implementation policy in
  `common/**`.

## Routing Model

- Supplied Figma links, screenshots, or inspect panels -> `design-screenshot-spec`.
- `Design Implementation Spec` to frontend code -> `frontend-layout-implementer`.
- Rendered UI comparison against spec or references -> `frontend-visual-qa`.
- Project overlay refresh -> `project-context-adapter`.
- Skill authoring or rule maintenance -> `agent-rules-skill-author`.

## Prohibited Encodings

- Do not block available read-only Figma MCP or browser fallback during intake.
- Do not add hard Figma MCP dependencies or auto-install missing tooling.
- Do not route Figma whiteboard, canvas editing, file creation,
  design-system generation, or Code Connect tasks.
- Do not treat image estimates as exact tokens or attach inspected properties
  to the wrong selected node/state. Require component evidence and user decisions
  for unresolved product behavior before implementation.
- Do not put host-project facts in reusable skills.
