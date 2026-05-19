---
name: figma-design-to-code
description: Use when implementing repository code from a Figma design, URL, or node. Fetch design context, screenshot, assets, and variables first, then translate the design into the repo's existing components, tokens, and framework conventions. Do not use for writing inside Figma or screenshot-only fallback tasks.
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

Translate Figma designs into production repository code with explicit design
context, screenshot validation, and repo-convention reuse.

This skill narrows the design-to-code path out of the generic
`frontend-design-workflow` so Figma work no longer lives only inside a broad
visual skill.

## When to use

- Implement a page, section, or component from a Figma URL or node.
- Generate or refine production UI code from Figma design context.
- Continue from `figma-design-reader` into actual repo implementation.

## When not to use

- Any write or edit inside Figma. Use `figma-canvas-editing`,
  `figma-screen-generation`, or `figma-design-system-builder`.
- Screenshot-only implementation when Figma is unavailable. Use
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

1. Get Figma design context and screenshot before touching code.
2. Map the design to existing repo tokens, components, layout primitives, and
   route boundaries.
3. Treat MCP output as design representation, not final code style.
4. Reuse existing components before creating new ones.
5. Translate Figma assets and variables into the repo's owned patterns.
6. Validate the implemented UI against the Figma screenshot and intended states.
7. If Figma access fails, switch to `screenshot-design-inspector` and state the
   drop in source confidence.

## Output expectations

The implementation summary should state:

- which Figma node or frame was implemented
- which repo primitives or tokens were reused
- any necessary deviation from the design
- what was visually verified against Figma

## Trigger evals

Should trigger:

- "Implement this React page from Figma."
- "Generate code from this Figma component."
- "Build the Next.js section to match this Figma node."

Should not trigger:

- "Create a new Figma file for this concept."
- "Edit the auto-layout and variables inside Figma."
- "Analyze these screenshots without Figma access."

## Reference map

- `references/implementation-flow.md`
