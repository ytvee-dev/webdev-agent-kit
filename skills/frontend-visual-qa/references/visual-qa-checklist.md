---
id: 'agents.skills.frontend-visual-qa.references.visual-qa-checklist'
title: 'Visual QA Checklist'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-visual-qa'
tags:
    - 'agents/skill-package'
    - 'frontend/verification'
    - 'agents/reference'
parent:
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
related:
    - '[[common/rendered-visual-verification-policy|Rendered Visual Verification Policy]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
depends_on:
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
---

# Visual QA Checklist

## Use Rendered Browser Evidence For

- Page or route loads without blocking runtime errors when visual QA is in scope.
- Primary content is visible above the fold at required viewports.
- Layout does not overflow horizontally.
- Text wraps acceptably as visible layout behavior.
- Fixed headers, sidebars, modals, and toolbars do not occlude content.
- Desktop, tablet, and mobile layout match supplied references when those viewports are in scope.
- Hover, focus, active, selected, disabled, loading, empty, and error states visibly match the spec when supplied.

## Do Not Use Rendered Browser Evidence For

- Reading font family, size, weight, line height, color, spacing, CSS variables, or token values when source files or copied inspect values are available.
- Checking typography by computed styles only.
- Replacing lint, typecheck, build, or static review.
- Project onboarding, stack detection, or MCP availability detection.

## Static Style Source Order

For font, color, spacing, and token questions, inspect in this order:

1. Design Implementation Spec or copied inspect values.
2. Local CSS, module styles, tokens, variables, and component files.
3. Project style overlays when present.
4. MDN or official docs when browser behavior affects interpretation.

Use Browser or Playwright only if the typography, spacing, or color issue is part of a broader visible mismatch that source inspection cannot answer.

## Visual Comparison

- Compare layout structure, alignment, spacing rhythm, typography hierarchy, colors, borders, radii, shadows, assets, and states from screenshots or visual references.
- Record each material mismatch with viewport and visible evidence.
- Distinguish approved project-native deviations from accidental mismatches.

## Availability Check

- Browser or Playwright MCP must be callable in the current agent session before reporting rendered browser QA.
- A running local app or installed Playwright dependency is not enough to claim Browser or Playwright MCP availability.
- When the tool is unavailable, report blocked rendered checks and continue only with honest static or manual checks.
