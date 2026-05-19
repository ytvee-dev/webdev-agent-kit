---
name: figma-design-reader
description: Use when a task needs read-only Figma analysis: inspect a Figma URL, node, or file; fetch design context, metadata, screenshots, variables, or assets; explain how a design is structured; or troubleshoot Figma MCP access before code or canvas edits. Do not use for screenshot-only analysis or writing inside Figma.
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
    - '[[skills/figma-design-reader/references/mcp-reading|Mcp Reading]]'
    - '[[skills/figma-design-to-code/SKILL|Figma Design To Code]]'
    - '[[skills/screenshot-design-inspector/SKILL|Screenshot Design Inspector]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Figma Design Reader

## Purpose

Use this skill for read-only Figma intake and analysis before implementation,
review, or design discussion.

This is a `.agents`-compatible Figma skill. It adapts the read-only parts of
the local `codex-skills/skills/figma/figma` workflow without taking ownership
of repo code generation or Figma canvas mutation.

## When to use

- Analyze a Figma URL, node, frame, or component before writing code.
- Explain structure, spacing, variables, typography, assets, or responsive
  behavior from Figma.
- Fetch `get_design_context`, `get_metadata`, `get_screenshot`, or asset
  references as source material for another skill.
- Troubleshoot Figma MCP access, oversized responses, or missing node context.

## When not to use

- Screenshot-only tasks where Figma access is unavailable or irrelevant.
  Use `screenshot-design-inspector`.
- Repo implementation from Figma. Use `figma-design-to-code`.
- Any write, create, edit, delete, variable, component, or auto-layout change
  inside Figma. Use `figma-canvas-editing` or a higher-level Figma canvas skill.

## Required context

1. Read `AGENTS.md`.
2. Read `.agents/project/figma-profile.md`.
3. Read `references/mcp-reading.md` before calling Figma read tools.
4. Add `frontend-design-workflow` when the read is in service of visual
   implementation.

## Core workflow

1. Confirm whether the prompt provides a Figma URL, node, file key, or an
   already selected Figma desktop node.
2. Fetch structured context first:
   - `get_design_context` for the exact node when the response size is tractable
   - `get_metadata` first when the node tree is large or the exact child node is
     still unclear
3. Fetch `get_screenshot` for the same node before making visual claims.
4. Read variables, component structure, text hierarchy, and asset references
   from the MCP output instead of inferring from the screenshot alone.
5. If the task will continue into code, hand off to `figma-design-to-code`.
6. If Figma access fails, ask for screenshots and hand off to
   `screenshot-design-inspector`.

## Output expectations

Return a concise design reading that includes:

- file or node scope analyzed
- major sections or component structure
- important tokens, variables, typography, or asset notes
- unknowns, truncation risk, or MCP limitations
- the correct next-skill handoff when more work is needed

## Trigger evals

Should trigger:

- "Read this Figma node and explain the layout before I implement it."
- "Analyze the variables and spacing in this Figma frame."
- "Inspect this Figma URL and tell me how the component is structured."

Should not trigger:

- "Implement this page from screenshots only."
- "Create variants and auto-layout in Figma."
- "Generate React code from this design."

## Reference map

- `references/mcp-reading.md`
