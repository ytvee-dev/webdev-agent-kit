---
id: 'agents.skills.agent-rules-skill-author.references.figma-derived-conventions'
title: 'Figma Derived Conventions'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'agent-rules-skill-author'
tags:
    - 'agents/skill-package'
    - 'agents/authoring'
    - 'frontend/figma'
    - 'agents/reference'
parent:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
related:
    - '[[skills/figma-design-reader/SKILL|Figma Design Reader]]'
    - '[[skills/figma-design-to-code/SKILL|Figma Design To Code]]'
depends_on:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
---

# Figma Derived Conventions

Use this reference when agent rules or skills need to encode reusable behavior
that was learned from Figma workflows.

## Section Map

- `Layer boundaries` for where Figma-derived rules belong.
- `Routing model` for mapping user intent to the correct Figma skill.
- `What not to encode` for avoiding repo leakage and skill overlap.

## Layer boundaries

- Put project-specific token names, breakpoint facts, and component locations in
  `.agents/project/figma-profile.md`, not in reusable skills.
- Put reusable read-only Figma workflow in `figma-design-reader`.
- Put reusable Figma-to-code workflow in `figma-design-to-code`.
- Put reusable Figma canvas mutation workflow in `figma-canvas-editing`.
- Put screenshot-only fallback rules in `screenshot-design-inspector`.

## Routing model

- Read or explain Figma -> `figma-design-reader`
- Implement repo code from Figma -> `figma-design-to-code`
- Edit existing Figma nodes, variables, or components -> `figma-canvas-editing`
- Build whole screens in Figma -> `figma-screen-generation`
- Build a Figma library or design system -> `figma-design-system-builder`
- Create Code Connect mappings -> `figma-code-connect`
- Create blank file -> `figma-create-file`
- No Figma access, screenshots only -> `screenshot-design-inspector`

## What not to encode

- Do not collapse all Figma work into `frontend-design-workflow`.
- Do not move Figma canvas rules into repo implementation skills.
- Do not encode screenshot-only fallback as if it were equivalent to Figma MCP
  reads.
- Do not copy vendor assets, licenses, or maintainers metadata into `.agents`
  unless the bundle truly needs them.
