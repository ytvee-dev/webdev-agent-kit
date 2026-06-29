---
id: 'agents.common.motion-rules'
title: 'Motion Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/design'
    - 'quality/motion'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
    - '[[common/design-quality-rubric|Design Quality Rubric]]'
depends_on: []
---

# Motion Rules

Purpose: keep frontend motion meaningful, restrained, accessible, and implementable without dependency inflation.

## Core Rule

Use motion only when it clarifies:

- state;
- hierarchy;
- transition;
- user feedback;
- subject atmosphere.

Do not use motion to hide weak layout, generic copy, or missing product logic.

## Restraint

Prefer one orchestrated motion idea over scattered effects.

Avoid:

- animating every card;
- scroll reveal on every section;
- hover effects that compete with focus states;
- motion that delays the user's task;
- animation libraries for simple opacity or transform transitions.

## CSS-First Preference

Prefer CSS transitions and animations when they are sufficient.

Prefer lightweight properties:

```text
transform
opacity
```

Be cautious with layout-affecting properties such as width, height, top, left, and margin.

## Reduced Motion

Respect reduced motion preferences.

If motion is part of the design direction, define the reduced-motion behavior:

```text
remove animation
shorten animation
replace movement with opacity
keep state change instant
```

## Approval Gate

Do not add animation libraries without explicit user approval.

Do not add motion systems, global animation tokens, or timeline frameworks without an approved architecture plan.

## Verification

When motion is used, verify:

- the animation supports the user's task;
- hover and focus states remain clear;
- reduced-motion behavior exists or is documented as a gap;
- performance risk is low;
- no testing workflow is introduced.
