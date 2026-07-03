---
id: 'agents.common.icon-quality-rules'
title: 'Icon Quality Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/icons'
    - 'quality/design'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/ui-ux-priority-checklist|UI UX Priority Checklist]]'
    - '[[common/anti-template-defaults|Anti-Template Defaults]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on: []
---

# Icon Quality Rules

Purpose: keep icons meaningful, consistent, accessible, and project-native without introducing new icon packages by default.

Use when a task adds, changes, reviews, or visually verifies icons, pictograms, glyphs, logos, status markers, navigation icons, action icons, or decorative symbols.

## Core Rules

- Use the project's existing icon system, asset folder, SVG pattern, or component primitive before introducing anything new.
- Do not add an icon library, SVG package, asset pipeline, or UI component package without explicit user approval.
- Do not use emojis as structural UI icons for navigation, settings, actions, system state, or status unless the product style explicitly requires it and accessibility is handled.
- Icons must have a job: action, status, category, affordance, brand, or illustration. Remove icons that only fill space.
- Keep icon family, stroke width, fill style, corner radius, optical size, and alignment consistent at the same hierarchy level.
- Do not mix filled and outline icons at the same semantic level unless the project convention uses that contrast to communicate state.
- Icons next to text must align optically with the text baseline and spacing rhythm.
- Functional icons must meet contrast expectations and remain distinguishable in supported themes.
- Official brand logos must not be redrawn, recolored, distorted, or guessed. Use official assets or report the asset gap.

## Accessibility Rules

- Icon-only buttons need accessible names.
- Decorative icons should not create noisy screen-reader output when the project has a pattern for hiding them.
- Status icons must not be the only status cue. Pair with text, shape, label, or another semantic signal when the state matters.
- Disabled, selected, active, expanded, and destructive icon states should be visually and semantically clear when relevant.

## Responsive And Interaction Rules

- Small visual icons may need a larger hit area for reliable touch interaction.
- Pressed, hover, focus, and disabled states must not shift layout bounds or cause jitter.
- Icons inside fixed or sticky UI must remain legible across viewport sizes and themes.

## Validation Gate

Before final reporting, verify that every added or changed icon is project-native, purposeful, consistent, accessible when interactive, and not a package-install shortcut.
