---
id: 'agents.common.diff-impact-verification-rules'
title: 'Diff Impact Verification Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/verification'
parent:
    - '[[common/lightweight-routing-policy|Lightweight Routing Policy]]'
related:
    - '[[common/smart-verification-budget|Smart Verification Budget]]'
    - '[[common/rendered-visual-verification-policy|Rendered Visual Verification Policy]]'
depends_on: []
---

# Diff Impact Verification Rules

Purpose: verify only the surfaces that the diff can affect.

## Direct Impact Rule

Map verification to changed files and changed ownership. Do not discover and test unrelated routes merely because they exist.

Verify directly affected routes, components, styles, states, and commands. If the diff touches a shared owner, verify representative surfaces that actually depend on that owner.

## CSS Impact Classes

Classify CSS-only changes before choosing verification.

### Low-risk visual-only CSS

Examples:

- background color;
- decorative background image or mask;
- border color;
- text color when contrast is not in question;
- non-layout theme variable value.

Default verification:

- changed-file formatting or CSS check when available;
- no full-repository lint by default;
- no typecheck by default;
- no local server by default;
- no rendered QA unless the user requested browser evidence, the same issue repeated, or accessibility/contrast risk is material.

### Layout-affecting CSS

Examples:

- display;
- position;
- width, height, min/max sizes;
- margin, padding, gap;
- grid or flex rules;
- overflow;
- media queries;
- z-index;
- typography that changes wrapping.

Default verification:

- changed-file formatting or CSS check;
- targeted rendered check only for affected route, viewport, or state when browser capability is available and the risk is material.

## Global File Rule

A global stylesheet change is not automatically a full-site visual QA task.

For global CSS:

1. Classify the changed properties.
2. Identify requested or directly affected pages.
3. Sample at most the requested pages or one representative surface for low-risk visual-only changes.
4. Escalate only when the global change affects layout, responsive behavior, focus, contrast, or repeated failure.

## Repeated Request Rule

If the user asks for the same visual correction again, increase verification one level.

- Second request: targeted rendered check on the directly affected route when browser capability exists.
- Third request or explicit failure report: bounded visual QA loop with screenshot evidence when browser capability exists.

## Report Rule

The final report must state why unrelated pages, full repository checks, or browser QA were skipped when the task is intentionally lightweight.
