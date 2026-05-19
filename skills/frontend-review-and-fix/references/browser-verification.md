---
id: 'agents.skills.frontend-review-and-fix.references.browser-verification'
title: 'Browser Verification'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-review-and-fix'
tags:
    - 'agents/skill-package'
    - 'frontend/review'
    - 'frontend/verification'
    - 'agents/reference'
parent:
    - '[[skills/frontend-review-and-fix/SKILL|Frontend Review and Fix]]'
related:
    - '[[skills/playwright-interactive/SKILL|Playwright Interactive]]'
depends_on:
    - '[[skills/frontend-review-and-fix/SKILL|Frontend Review and Fix]]'
---

# Browser Verification

Use this reference when the touched surface includes rendered UI, interaction,
hydration, responsive layout, browser-only APIs, canvas, animation, or console
errors. It complements the commands in `.agents/project/verification-profile.md`.
Use `playwright-interactive` when verification needs persistent browser
interaction, screenshot evidence, desktop/mobile viewport checks, or
console/runtime inspection.

## Decision tree

- Static HTML or static route output: inspect the source and rendered page, then
  verify key selectors and screenshots.
- Dynamic React app: wait for the page to finish rendering before inspecting the
  DOM or taking screenshots.
- Interactive or visual QA: load `playwright-interactive` and build a QA
  inventory before testing.
- Existing dev server: use the running URL.
- No dev server: start the repo's normal local server only when browser
  verification is needed, then stop it before finishing.

## Verification pattern

1. Navigate to the relevant route in a real browser.
2. Wait for the app to reach a settled rendered state before inspecting DOM.
3. Capture console messages and runtime errors.
4. Inspect visible text, controls, landmarks, and key selectors from the
   rendered DOM.
5. Exercise the changed interaction flow with role, text, label, or stable test
   selectors.
6. Capture screenshots when layout, responsive behavior, canvas, or visual
   polish matters.
7. Verify the relevant desktop and mobile viewport when responsiveness changed.
8. Close the browser and stop any server started for the check.

## Rules

- Do not use `npm run dev` as a substitute for verification commands.
- Do not inspect a dynamic app before it has rendered.
- Prefer user-facing selectors such as role, label, and visible text over brittle
  DOM paths.
- Treat console errors and hydration errors as verification failures unless the
  repo documents them as expected.
- Do not use production systems or production data for browser checks.
