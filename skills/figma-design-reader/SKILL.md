---
name: figma-design-reader
description: Use when a task needs offline analysis of user-provided Figma-derived artifacts: screenshots, exports, copied inspect values, token/style notes, written specs, or design briefs. If the user provides only a Figma URL, node, or file key, ask for source material instead of opening Figma. Do not use for writing inside Figma or repo code implementation.
id: 'agents.skills.figma-design-reader.skill'
title: 'Figma Design Reader'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'figma-design-reader'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/figma'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/figma-design-reader/references/source-material-reading|Source Material Reading]]'
    - '[[skills/figma-design-to-code/SKILL|Figma Design To Code]]'
    - '[[skills/screenshot-design-inspector/SKILL|Screenshot Design Inspector]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Figma Design Reader

## Purpose

Use this skill for read-only Figma-derived source-material intake and analysis
before implementation, review, or design discussion.

This is a `.agents`-compatible Figma skill. It adapts the read-only parts of
the local design-reading workflow without taking ownership of repo code
generation or Figma canvas editing.

## When to use

- Analyze user-provided screenshots, exports, copied inspect values,
  variables/styles notes, design specs, or briefs derived from Figma.
- Explain structure, spacing, variables, typography, assets, responsive
  behavior, or component states from supplied source material.
- Identify missing artifacts when the user only provides a Figma URL, node, or
  file key.
- Prepare source-material findings for `figma-design-to-code`,
  `figma-canvas-editing`, or another downstream planning workflow.

## When not to use

- Screenshot-only tasks where the source is not Figma-derived. Use
  `screenshot-design-inspector`.
- Repo implementation from Figma. Use `figma-design-to-code`.
- Any write, create, edit, delete, variable, component, or auto-layout change
  inside Figma. Use the relevant offline planning skill.

## Required context

1. Read `AGENTS.md`.
2. Read `.agents/project/figma-profile.md`.
3. Read `references/source-material-reading.md` before analysis.
4. Add `frontend-design-workflow` when the read is in service of visual
   implementation.

## Core workflow

1. Confirm which source materials are present: screenshots, exports, copied
   inspect values, variables/styles notes, token tables, written specs, or repo
   code references.
2. If the prompt only provides a Figma URL, node, or file key, stop and ask for
   screenshots, exports, copied inspect values, token/spec notes, or a written
   brief. Do not try to open Figma.
3. Separate high-confidence copied/exported values from screenshot-inferred
   values.
4. Read variables, component structure, text hierarchy, asset references, and
   responsive behavior only from supplied material.
5. Mark missing states, breakpoints, assets, and token values explicitly.
6. If the task will continue into code, hand off to `figma-design-to-code`.

## Output expectations

Return a concise design reading that includes:

- file, node, frame, or artifact scope described by the user
- major sections or component structure
- important tokens, variables, typography, or asset notes
- unknowns, source confidence, and missing artifacts
- the correct next-skill handoff when more work is needed

## Trigger evals

Should trigger:

- "Analyze these screenshots and copied Figma inspect values before I implement it."
- "Read these exported frames and token notes and explain the layout."
- "This Figma node is described in this spec; tell me how the component is structured."

Should not trigger:

- "Implement this page from screenshots only."
- "Create variants and auto-layout in Figma."
- "Generate React code from this design."

## Reference map

- `references/source-material-reading.md`
