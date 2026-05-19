---
name: figma-code-connect
description: Use for Figma Code Connect workflows: get suggestions, match published Figma components to code components, confirm mappings, and send mappings. Do not use for Figma canvas edits, screen generation, or repository code implementation from design.
id: 'agents.skills.figma-code-connect.skill'
title: 'Figma Code Connect'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'figma-code-connect'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/figma'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/figma-code-connect/references/mapping-workflow|Mapping Workflow]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Figma Code Connect

## Purpose

Use this skill for Code Connect mapping between published Figma components and
repository code components.

## When to use

- Get Code Connect suggestions from a Figma selection or URL.
- Match Figma components to code components in the repo.
- Send confirmed Code Connect mappings.

## When not to use

- Repo implementation from Figma. Use `figma-design-to-code`.
- Figma canvas mutation. Use `figma-canvas-editing`.
- Full-screen composition or design-system authoring in Figma.

## Required context

1. Read `AGENTS.md`.
2. Read `references/mapping-workflow.md`.
3. Read the candidate code components before sending mappings.

## Core rules

- Treat Code Connect as a mapping workflow, not a design implementation workflow.
- Require a published Figma component or component set before mapping.
- Search the codebase for real matches instead of asking the user for a path too
  early.
- Present matches clearly when user confirmation is needed.

## Trigger evals

Should trigger:

- "Connect this Figma component to code."
- "Set up Code Connect for these published components."
- "Find matching repo components for this Figma selection."

Should not trigger:

- "Implement this design in React."
- "Create a new component set in Figma."
- "Explain the spacing in this Figma frame."

## Reference map

- `references/mapping-workflow.md`
