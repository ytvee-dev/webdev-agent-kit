---
name: figma-canvas-editing
description: Use for create, edit, delete, or inspect-with-JavaScript actions inside a Figma file through use_figma: nodes, auto-layout, variables, components, variants, styles, bindings, or file-structure scripts. Pair with higher-level Figma skills for screens or libraries. Do not use for repository code generation or screenshot-only reading.
id: 'agents.skills.figma-canvas-editing.skill'
title: 'Figma Canvas Editing'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'figma-canvas-editing'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/figma'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/figma-canvas-editing/references/plugin-api-rules|Plugin Api Rules]]'
    - '[[skills/figma-canvas-editing/references/mutation-workflows|Mutation Workflows]]'
    - '[[skills/figma-screen-generation/SKILL|Figma Screen Generation]]'
    - '[[skills/figma-design-system-builder/SKILL|Figma Design System Builder]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Figma Canvas Editing

## Purpose

Use this skill for low-level Figma canvas mutation through `use_figma`.

It is the prerequisite skill for higher-level Figma write workflows, but it
does not own screen-building strategy, design-system phasing, or repo code
implementation.

## When to use

- Create, edit, or delete Figma nodes.
- Modify auto-layout, fills, strokes, text, variables, component properties,
  variants, bindings, or pages through Plugin API scripts.
- Run file-context JavaScript inspection that requires `use_figma`.

## When not to use

- Read-only design analysis without Plugin API execution. Use
  `figma-design-reader`.
- Repo implementation from Figma. Use `figma-design-to-code`.
- Screenshot-only analysis. Use `screenshot-design-inspector`.
- Full-screen composition or design-system building without the companion
  orchestration skill.

## Required context

1. Read `AGENTS.md`.
2. Read `references/plugin-api-rules.md` before any `use_figma` call.
3. Read `references/mutation-workflows.md` for multi-step mutations.
4. Add `figma-screen-generation` for screen-level composition work.
5. Add `figma-design-system-builder` for design-system or library work.

## Core rules

- Treat `use_figma` as the mutation boundary for Figma canvas edits.
- Work incrementally in small scripts. Do not batch a whole workflow into one
  large call.
- Return all created or mutated node IDs from every script.
- Re-read file state between mutation steps when the next action depends on it.
- Stop on `use_figma` errors, fix the script, then retry.
- Keep page context explicit across calls.

## Trigger evals

Should trigger:

- "Edit this auto-layout in Figma."
- "Create variants and variables in the Figma file."
- "Use Plugin API to inspect and mutate these nodes."

Should not trigger:

- "Read this Figma node and explain it."
- "Generate React code from this Figma component."
- "Implement this card from screenshots."

## Reference map

- `references/plugin-api-rules.md`
- `references/mutation-workflows.md`
