---
name: screenshot-design-inspector
description: Use when design implementation starts from screenshots, or when Figma MCP access fails and the user can provide screenshots. Inspect desktop, tablet, and mobile screenshots to extract typography, color, spacing, and breakpoint intent without inventing missing design data.
id: 'agents.skills.screenshot-design-inspector.skill'
title: 'Screenshot Design Inspector'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'screenshot-design-inspector'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/screenshot-design-inspector/references/device-mapping|Device Mapping]]'
    - '[[skills/screenshot-design-inspector/references/extraction-checklist|Extraction Checklist]]'
    - '[[skills/screenshot-design-inspector/references/figma-ui-reading|Figma UI Reading]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Screenshot Design Inspector

## Purpose

Inspect screenshots as a design source when Figma is unavailable or insufficient.

## Required context

1. Read `AGENTS.md`.
2. Read `.agents/project/styling-profile.md`.
3. Read `.agents/project/figma-profile.md`.
4. Read the relevant framework path index for the target UI area.

## Workflow

1. Try Figma MCP first when the request started from a Figma URL or node.
2. If Figma access fails, ask the user to resend the task with screenshots.
3. Group screenshots by device class: desktop, tablet, and mobile.
4. Extract what is visible with confidence:
   - font size
   - font family or label
   - font weight
   - text color
   - spacing rhythm
   - breakpoint intent and layout shifts
5. Mark low-confidence observations explicitly.
6. Ask the user when a missing or ambiguous value is too uncertain to implement safely.

## Core rules

- Do not invent missing design data.
- Prefer existing project tokens and theme variables when translating screenshot
  observations into implementation.
- If a screenshot suggests a new global token, ask the user before adding it.
- Use screenshots to estimate values only when Figma or source code does not
  provide them.

## Reference map

- `references/extraction-checklist.md`
- `references/device-mapping.md`
- `references/figma-ui-reading.md`
