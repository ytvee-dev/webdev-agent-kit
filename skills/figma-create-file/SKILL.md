---
name: figma-create-file
description: Use when the user wants a new blank Figma design file or FigJam file, or when a Figma canvas workflow needs a fresh file before any use_figma calls. Resolve the target plan if needed, create the file, and hand off to the appropriate Figma skill. Do not use for existing-file editing or read-only design analysis.
id: 'agents.skills.figma-create-file.skill'
title: 'Figma Create File'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'figma-create-file'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/figma'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/figma-canvas-editing/SKILL|Figma Canvas Editing]]'
    - '[[skills/figma-screen-generation/SKILL|Figma Screen Generation]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Figma Create File

## Purpose

Create a new blank Figma design file or FigJam file and hand off cleanly to the
next Figma workflow.

## When to use

- The user wants a new Figma design file.
- The user wants a new FigJam file.
- A Figma editing workflow needs a fresh file before any canvas mutations.

## When not to use

- Existing-file editing. Use `figma-canvas-editing` or a higher-level Figma
  canvas skill.
- Read-only design analysis. Use `figma-design-reader`.

## Core workflow

1. Resolve the target plan or organization when required.
2. Create the file with the requested editor type:
   - `design`
   - `figjam`
3. Return the created file key and URL.
4. Hand off to `figma-canvas-editing` or `figma-screen-generation` when the user
   wants immediate follow-up work in the new file.

## Trigger evals

Should trigger:

- "Create a new Figma file for this flow."
- "Make a blank FigJam for brainstorming."
- "Start a fresh design file, then build the screen in it."

Should not trigger:

- "Update this existing frame in Figma."
- "Read this Figma component and explain it."
- "Implement this design in code."
