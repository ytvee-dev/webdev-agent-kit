---
name: playwright-interactive
description: Use for interactive browser QA of local web apps with Playwright, persistent js_repl sessions, screenshots, viewport checks, console/runtime inspection, and optional Electron window debugging. Do not use for pure unit tests, static code review, or backend-only work.
id: 'agents.skills.playwright-interactive.skill'
title: 'Playwright Interactive'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'playwright-interactive'
tags:
    - 'agents/skill-package'
    - 'frontend/verification'
    - 'frontend/browser'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/playwright-interactive/references/interactive-browser-qa|Interactive Browser QA]]'
    - '[[skills/playwright-interactive/references/screenshot-and-viewport-checks|Screenshot And Viewport Checks]]'
    - '[[skills/frontend-review-and-fix/SKILL|Frontend Review and Fix]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Playwright Interactive

## Purpose

Use persistent Playwright sessions for browser verification when a local React or
Next.js task needs real rendered UI evidence: interaction flows, console/runtime
checks, responsive layout, screenshots, canvas, animation, hydration behavior,
or visual QA.

This is a `.agents`-compatible skill. It adapts the local curated
`codex-skills/skills/.curated/playwright-interactive` workflow into this bundle
without importing assets or license-bearing icons.

## When to use

- Debug or verify a local web app in a real browser.
- Exercise user-facing controls after implementation.
- Capture screenshot evidence for layout, responsive behavior, canvas, visual
  polish, or coordinate-based follow-up.
- Inspect console errors, hydration errors, browser-only APIs, or runtime
  behavior that static checks cannot prove.
- Run optional Electron window QA when the target app is Electron and the local
  environment already supports it.

## When not to use

- Pure unit tests, static code review, lint/typecheck-only tasks, backend-only
  work, or documentation-only changes with no rendered UI surface.
- Production URLs, production systems, or production data.
- Package installation or browser binary installation unless the user explicitly
  approves the dependency/setup step.

## Required context

1. Read `AGENTS.md`.
2. Read `.agents/project/verification-profile.md`.
3. Read the changed route/component and nearby styles.
4. Read `.agents/skills/frontend-review-and-fix/references/browser-verification.md`
   when this skill is part of a review or final verification pass.
5. Read `references/interactive-browser-qa.md` before starting or reusing a
   Playwright session.
6. Read `references/screenshot-and-viewport-checks.md` when screenshots,
   responsive behavior, viewport fit, canvas, visual polish, or coordinate
   follow-up are in scope.

## Core workflow

1. Define a QA inventory before opening the browser:
   - user requirements to verify
   - implemented user-visible behavior
   - final-response claims that need evidence
   - controls, modes, states, and off-happy-path scenarios
2. Confirm the app can run locally and choose the normal project dev/start
   command. Keep any server in a persistent session.
3. Use an existing Playwright browser session when available; otherwise start a
   new one only after setup is confirmed.
4. Prefer `http://127.0.0.1:<port>` for local targets.
5. Verify the functional path with normal user input: role, label, visible text,
   stable test selectors, keyboard, pointer, or touch.
6. Run a separate visual QA pass for the same inventory.
7. Capture console messages and treat console or hydration errors as failures
   unless the repo documents them as expected.
8. Check desktop and mobile viewports when responsiveness is part of the change.
9. Verify viewport fit before signoff when the initial view, fixed shell, canvas,
   dashboard, editor, game, or tool surface matters.
10. Clean up Playwright handles only when the task is finished, unless the user
    wants the session kept alive.

## Session defaults

- Use explicit desktop viewport `{ width: 1600, height: 900 }` for routine
  reproducible QA.
- Use mobile viewport `{ width: 390, height: 844, isMobile: true, hasTouch:
  true }` for mobile checks.
- Use native-window mode only as an extra pass for host window size, DPI,
  browser chrome, or Electron-style behavior.
- Reuse handles across iterations. Reload renderer-only web changes; relaunch
  only when process ownership, startup code, or Electron main/preload code
  changed.
- Treat `js_repl_reset` as recovery, not cleanup, because it destroys session
  handles.

## Output expectations

In the final response, report:

- which routes, viewports, and interaction flows were verified
- which screenshots or visual states were reviewed
- console/runtime findings
- any setup that could not run, including missing Playwright, missing browser
  binaries, sandbox restrictions, missing dev server, or unavailable `js_repl`

## Trigger evals

Should trigger:

- "Use Playwright to verify the new responsive menu and capture screenshots."
- "Debug this local Next.js page in a browser; it hydrates but clicking the tab
  does nothing."
- "Run browser QA for the canvas interaction and check mobile viewport fit."

Should not trigger:

- "Review this reducer for TypeScript issues."
- "Run unit tests for the parser."
- "Update `.agents/README.md` wording only."

## Reference map

- `references/interactive-browser-qa.md`
- `references/screenshot-and-viewport-checks.md`
