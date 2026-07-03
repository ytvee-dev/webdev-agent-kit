---
id: 'agents.common.mobile-responsive-rules'
title: 'Mobile Responsive Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/responsive'
    - 'quality/ux'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/ui-ux-priority-checklist|UI UX Priority Checklist]]'
    - '[[common/navigation-ux-rules|Navigation UX Rules]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
depends_on: []
---

# Mobile Responsive Rules

Purpose: make mobile and intermediate viewport behavior explicit instead of treating small screens as compressed desktop.

Use when implementing, reviewing, or visually verifying screens, sections, navigation, forms, dashboards, tables, charts, sticky UI, modals, drawers, or text-heavy pages.

## Viewport Model

Consider these viewport classes when relevant:

- small phone around 375px wide;
- tablet around 768px wide;
- desktop around 1024px and above;
- wide desktop around 1440px when the design depends on wide space;
- landscape when fixed UI, forms, media, or app-like screens are affected.

## Core Rules

- Avoid uncontrolled horizontal overflow.
- Keep long text readable and wrapping intentional.
- Keep the primary content and primary action reachable on small screens.
- Fixed and sticky UI must not hide content.
- Full-height mobile layouts should account for browser chrome using existing project patterns.
- Touch targets should be reliable on small screens.
- Dense dashboards and tables need an explicit small-screen strategy.
- Desktop-only hover behavior must not be required for task completion.

## Implementation Boundary

Reuse existing breakpoints, CSS Modules conventions, and responsive primitives. Do not introduce a global breakpoint system, utility framework, or styling library without approval.

## Validation Gate

Before final reporting, state which viewports were considered, which were verified, and which responsive behaviors remain inferred or blocked.
