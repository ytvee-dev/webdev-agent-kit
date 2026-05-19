---
name: figma-design-system-builder
description: Use when building or updating a Figma design system or component library from a codebase: variables, collections, modes, styles, components, documentation pages, and design-system structure. Pair with figma-canvas-editing for the actual use_figma mutations. Do not use for one-off screen edits or repository code generation.
id: 'agents.skills.figma-design-system-builder.skill'
title: 'Figma Design System Builder'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'figma-design-system-builder'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/figma'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/figma-canvas-editing/SKILL|Figma Canvas Editing]]'
    - '[[skills/figma-design-system-builder/references/phase-plan|Phase Plan]]'
    - '[[skills/figma-design-system-builder/references/component-library-rules|Component Library Rules]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Figma Design System Builder

## Purpose

Use this skill when the deliverable is a Figma design system or reusable
component library rather than product code or a one-off screen.

## When to use

- Create or update Figma variables, collections, modes, text styles, or effect
  styles from a codebase.
- Build component-library pages, variants, documentation surfaces, or token
  foundations in Figma.
- Reconcile code tokens and Figma design-system structure.

## When not to use

- One-off page or screen composition. Use `figma-screen-generation`.
- Repo implementation from Figma. Use `figma-design-to-code`.
- Single low-level mutations without a library-level deliverable. Use
  `figma-canvas-editing`.

## Required context

1. Read `AGENTS.md`.
2. Add `figma-canvas-editing`.
3. Read `references/phase-plan.md` before any write step.
4. Read `references/component-library-rules.md` when creating components,
   variants, variables, or documentation pages.
5. Read the codebase token and component structure before mutating Figma.

## Core rules

- Never treat a design-system build as a one-shot mutation.
- Lock scope before creation: tokens, pages, and component families.
- Build foundations before components.
- Validate after each phase and each component family.
- Keep code-token alignment explicit, including naming and code syntax.

## Trigger evals

Should trigger:

- "Build a Figma design system from this codebase."
- "Create variables, tokens, and component library pages in Figma."
- "Update the Figma library to match our design tokens."

Should not trigger:

- "Create one new screen in Figma."
- "Connect this component to Code Connect."
- "Implement this component in React."

## Reference map

- `references/phase-plan.md`
- `references/component-library-rules.md`
