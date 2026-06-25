---
id: 'agents.skills.frontend-layout-implementer.references.implementation-rules'
title: 'Implementation Rules'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-layout-implementer'
tags:
    - 'agents/skill-package'
    - 'frontend/implementation'
    - 'agents/reference'
parent:
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
related:
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
depends_on:
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
---

# Implementation Rules

## Stack Detection

- Inspect package manifests, configs, route trees, source entrypoints, and
  existing component/style files before editing.
- Use React/Next rules only when the project actually uses React or Next.
- For static HTML/CSS or another framework, follow the local file and style
  ownership already present.

## Layout Translation

- Prefer semantic structure over generated Figma-like wrapper depth.
- Use existing components and primitives before creating new ones.
- Keep one-off styles local to the changed surface.
- Use shared tokens only when they already exist or the user approves adding
  them.
- Keep fixed dimensions only where the spec requires fixed-format UI; otherwise
  use responsive constraints.

## Frontend Quality

- Ensure text wraps without overflow at supported viewports.
- Keep controls reachable by keyboard when the surrounding app supports
  keyboard interaction.
- Preserve labels, alt text, contrast intent, focus indication, loading states,
  and disabled states when in scope.
- Avoid unrelated refactors.

## Verification

- Run the relevant local checks from `project/verification-profile.md`.
- Use `frontend-visual-qa` for browser screenshots, viewport checks, and visual
  comparison.

