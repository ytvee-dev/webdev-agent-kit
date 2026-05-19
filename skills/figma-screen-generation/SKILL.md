---
name: figma-screen-generation
description: Use when building or updating a full Figma screen, page, view, or multi-section layout from code or a written description. Reuse design-system components, variables, and styles, and pair with figma-canvas-editing for the actual use_figma mutations. Do not use for repository code generation or one-off low-level node edits by themselves.
id: 'agents.skills.figma-screen-generation.skill'
title: 'Figma Screen Generation'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'figma-screen-generation'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/figma'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/figma-canvas-editing/SKILL|Figma Canvas Editing]]'
    - '[[skills/figma-screen-generation/references/screen-build-workflow|Screen Build Workflow]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Figma Screen Generation

## Purpose

Use this skill when the deliverable is a screen in Figma rather than code in
the repo.

## When to use

- Build a new screen or page in Figma from code or a written spec.
- Update an existing Figma screen to match product code or a redesigned view.
- Assemble a multi-section layout from design-system instances.

## When not to use

- Repo code implementation from Figma. Use `figma-design-to-code`.
- Low-level one-off node edits without a screen-level deliverable. Use
  `figma-canvas-editing`.
- Design-system or component-library authoring. Use
  `figma-design-system-builder`.

## Required context

1. Read `AGENTS.md`.
2. Add `figma-canvas-editing`.
3. Read `references/screen-build-workflow.md`.
4. Read the relevant source code or written specification before mutating Figma.

## Core rules

- Discover the screen structure before building.
- Reuse published design-system components, variables, and styles instead of
  drawing with hardcoded values when reusable assets exist.
- Build incrementally, section by section.
- Validate visually after each major section.
- Treat screen updates and new screens as file-state-aware workflows rather than
  one-shot scripts.

## Trigger evals

Should trigger:

- "Build this landing page in Figma from the code."
- "Create a Figma screen for this app view."
- "Update the Figma screen to match the current implementation."

Should not trigger:

- "Generate React code from this Figma node."
- "Create a new variable collection in Figma."
- "Just tweak this one text layer with Plugin API."

## Reference map

- `references/screen-build-workflow.md`
