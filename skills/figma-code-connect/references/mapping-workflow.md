---
id: 'agents.skills.figma-code-connect.references.mapping-workflow'
title: 'Mapping Workflow'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'figma-code-connect'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/figma'
    - 'agents/reference'
parent:
    - '[[skills/figma-code-connect/SKILL|Figma Code Connect]]'
related:
    - '[[skills/figma-design-to-code/SKILL|Figma Design To Code]]'
depends_on:
    - '[[skills/figma-code-connect/SKILL|Figma Code Connect]]'
---

# Mapping Workflow

Use this reference for Code Connect operations.

## Section Map

- `Required flow` for suggestions, search, and mapping.
- `Matching rules` for codebase selection.
- `Failure modes` for published component and permission issues.

## Required flow

1. Normalize the Figma selection or URL node reference.
2. Run suggestions first so the workflow starts from actual unmapped published
   components.
3. Search the repo for matching code components and inspect their prop surface.
4. Present the best match or the top candidates when ambiguity remains.
5. Send mappings only for confirmed or clearly accepted targets.

## Matching rules

- Prefer structural and prop-interface matches over name similarity alone.
- Use the real relative source path from the repo.
- Choose the correct framework label for the mapping payload.
- Stop and explain when no trustworthy match exists.

## Failure modes

- If the component is not published, explain that Code Connect cannot proceed on
  unpublished components.
- If the mapping already exists, report that instead of forcing a duplicate
  workflow.
- If plan or permission limitations block mapping, surface that exact blocker.
