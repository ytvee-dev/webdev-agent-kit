---
name: figma-design-to-code
description: Use when implementing repository UI code from user-provided Figma-derived screenshots, exports, copied inspect values, token/style notes, written specs, or briefs. If the user provides only a Figma URL, node, or file key, ask for source material first. Do not use for writing inside Figma or generic screenshot tasks.
id: 'agents.skills.figma-design-to-code.skill'
title: 'Figma Design To Code'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'figma-design-to-code'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/figma'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/figma-design-reader/SKILL|Figma Design Reader]]'
    - '[[skills/frontend-design-workflow/SKILL|Frontend Design Workflow]]'
    - '[[skills/react-component-workflow/SKILL|React Component Workflow]]'
    - '[[skills/nextjs-app-router/SKILL|Nextjs App Router]]'
    - '[[skills/figma-design-to-code/references/implementation-flow|Implementation Flow]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Figma Design To Code

## Purpose

Translate user-provided Figma-derived source material into production
repository code with explicit confidence notes and repo-convention reuse.

This skill narrows the design-to-code path out of the generic
`frontend-design-workflow` so Figma work no longer lives only inside a broad
visual skill.

## When to use

- Implement a page, section, or component from supplied Figma-derived
  screenshots, exports, copied inspect values, token/style notes, or specs.
- Generate or refine production UI code from Figma-derived source material.
- Continue from `figma-design-reader` into actual repo implementation.

## When not to use

- Any write or edit inside Figma. Use the relevant offline planning skill.
- Screenshot-only implementation that is not Figma-derived. Use
  `screenshot-design-inspector` plus `frontend-design-workflow`.
- Generic styling polish without Figma as the source of truth. Use
  `frontend-design-workflow`.

## Required context

1. Read `AGENTS.md`.
2. Read `.agents/project/figma-profile.md`.
3. Read `.agents/project/styling-profile.md`.
4. Add `frontend-design-workflow`.
5. Add `react-component-workflow` or `nextjs-app-router` based on the touched
   code surface.
6. Read `references/implementation-flow.md` before implementation starts.

## Core workflow

1. Confirm that source artifacts are available before touching code.
2. If the prompt only includes a Figma URL, node, or file key, ask for
   screenshots, exports, copied inspect values, token/style notes, or a written
   spec instead of opening Figma.
3. Map the design to existing repo tokens, components, layout primitives, and
   route boundaries.
4. Treat copied/exported source material as design intent, not final code style.
5. Reuse existing components before creating new ones.
6. Translate supplied assets and variables into the repo's owned patterns.
7. Validate the implemented UI against supplied screenshots, exports, specs, and
   intended states.

## Output expectations

The implementation summary should state:

- which Figma-derived artifacts or described node/frame were implemented
- which repo primitives or tokens were reused
- any necessary deviation from the design
- what was visually verified against supplied materials

## Trigger evals

Should trigger:

- "Implement this React page from these Figma exports and inspect values."
- "Generate code from this Figma component spec and screenshots."
- "Build the Next.js section to match this Figma-derived brief."

Should not trigger:

- "Create a new Figma file for this concept."
- "Edit the auto-layout and variables inside Figma."
- "Analyze generic screenshots that are not Figma-derived."

## Reference map

- `references/implementation-flow.md`
