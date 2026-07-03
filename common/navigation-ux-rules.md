---
id: 'agents.common.navigation-ux-rules'
title: 'Navigation UX Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/navigation'
    - 'quality/ux'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/ui-ux-priority-checklist|UI UX Priority Checklist]]'
    - '[[common/mobile-responsive-rules|Mobile Responsive Rules]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on: []
---

# Navigation UX Rules

Purpose: keep frontend navigation predictable, recoverable, accessible, and consistent with the current project architecture.

Use when changing menus, nav bars, sidebars, breadcrumbs, tabs, route links, filters encoded in URLs, modal flows, dashboard navigation, or multi-step journeys.

## Core Rules

- Current location must be visually identifiable when navigation is persistent or repeated.
- Primary navigation, secondary navigation, page actions, and destructive actions must not appear as the same hierarchy.
- Back behavior must stay predictable. Do not silently reset route history, filters, scroll position, or form context unless the product flow requires it.
- Deep states that users need to share, reload, bookmark, or return to should be represented in routes, params, query state, or a documented project-native state mechanism.
- Breadcrumbs are useful only when hierarchy is deep enough to help orientation. Do not add breadcrumbs to flat pages as decoration.
- Modal and drawer flows must include a clear escape path and must not replace primary navigation.
- Search and filters should preserve enough state for the user to understand what list or result set they are viewing.
- Destructive actions such as delete account, remove workspace, logout, or reset data must be spatially and visually separated from ordinary navigation.

## Responsive Navigation

- Mobile navigation must be designed explicitly; do not shrink a desktop sidebar into a broken layout.
- Avoid putting more than one primary navigation model at the same hierarchy level, such as tabs, sidebar, and bottom nav all competing.
- Fixed headers, bottom bars, and sidebars must reserve space so content and controls are not hidden.
- Touch targets in navigation must be large enough for reliable use on small screens.
- Mobile menu open, close, focus, and scroll behavior must be considered when the project has interactive navigation.

## Accessibility Rules

- Navigation landmarks and labels should match project conventions and semantic HTML patterns.
- Focus should not disappear behind fixed overlays, modals, drawers, or route transitions.
- Icon-only navigation needs accessible labels.
- Active, expanded, selected, and disabled navigation states should be semantically represented when existing project patterns support it.

## Implementation Boundaries

- Reuse existing route structure, link components, active-link helpers, CSS Modules patterns, and responsive breakpoints.
- Do not introduce a router, navigation library, URL-state library, animation library, or UI component package without explicit approval.
- Do not redesign global navigation while implementing a scoped page unless the user asked for navigation changes.

## Validation Gate

Before final reporting, verify that users can identify where they are, move forward, go back, recover from overlays, and use the navigation at the relevant responsive viewports.
