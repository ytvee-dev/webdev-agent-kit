---
id: 'agents.skills.frontend-design-intelligence.references.design-dials'
title: 'Design Dials'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-design-intelligence'
tags:
    - 'agents/skill-package'
    - 'agents/reference'
    - 'workflow/design-intelligence'
parent:
    - '[[skills/frontend-design-intelligence/SKILL|Frontend Design Intelligence]]'
related:
    - '[[templates/design-direction-contract|Design Direction Contract Template]]'
    - '[[common/motion-rules|Motion Rules]]'
    - '[[common/design-quality-rubric|Design Quality Rubric]]'
depends_on:
    - '[[skills/frontend-design-intelligence/SKILL|Frontend Design Intelligence]]'
---

# Design Dials

Purpose: make visual intensity explicit without forcing a generic style catalog.

Use three 1-10 dials when a design task needs visual direction, redesign, landing structure, dashboard density, or motion stance.

## Visual Variance

How much the layout, palette, typography, and signature element depart from safe defaults.

```text
1-3: restrained, centered, quiet, convention-led
4-7: distinctive but stable, one memorable move
8-10: bold, asymmetric, high personality, higher execution risk
```

Rules:

- Low variance still needs precision.
- Mid variance should spend boldness in one place.
- High variance must be justified by audience, brand, content, or product context.

## Motion Intensity

How much motion contributes to state, hierarchy, transition, feedback, or atmosphere.

```text
1-3: minimal transitions and direct feedback
4-7: one coordinated motion idea or a few clear micro-interactions
8-10: choreographed motion, only when the product story needs it
```

Rules:

- Prefer CSS-first motion when sufficient.
- Motion must not hide weak layout or generic copy.
- Reduced-motion behavior must be defined when motion matters.
- Do not add animation libraries without explicit approval.

## Information Density

How much information appears per viewport and how quickly the user needs to scan.

```text
1-3: spacious, editorial, low decision pressure
4-7: balanced product UI or marketing page
8-10: dense dashboard, operations, analytics, or expert workflow
```

Rules:

- High density needs stronger hierarchy, grouping, and scan paths.
- Low density needs better typography and spacing discipline.
- Density should match the user's decision speed and context.

## Handoff Format

```text
visual variance: 1-10 + reason
motion intensity: 1-10 + reason + reduced-motion stance
information density: 1-10 + reason + responsive implication
```
