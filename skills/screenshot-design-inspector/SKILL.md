---
name: screenshot-design-inspector
description: Use when design implementation starts from user-provided screenshots or copied visual inspect panels. Inspect desktop, tablet, and mobile screenshots to extract typography, color, spacing, and breakpoint intent without inventing missing design data. Do not treat this as a remote file reader.
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

Inspect screenshots and copied visual inspect panels as design sources.
This is a first-class offline source-material skill, not a remote file reader.

## Required context

1. Read `AGENTS.md`.
2. Read `.agents/project/styling-profile.md`.
3. Read `.agents/project/figma-profile.md`.
4. Read the relevant framework path index for the target UI area.

## Workflow

1. Confirm screenshots or copied visual inspect panels are present.
2. If the request provides only a Figma URL, node, or file key, ask the user for
   screenshots, exports, copied inspect values, token/style notes, or a written
   brief.
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
- Do not use this skill as a substitute for `figma-design-reader` when the user
  supplies Figma-derived specs, exports, or copied inspect values that need
  structured analysis.
- Prefer existing project tokens and theme variables when translating screenshot
  observations into implementation.
- If a screenshot suggests a new global token, ask the user before adding it.
- Use screenshots to estimate values only when source material or source code
  does not provide them.

## Reference map

- `references/extraction-checklist.md`
- `references/device-mapping.md`
- `references/figma-ui-reading.md`
