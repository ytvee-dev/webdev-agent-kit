---
id: 'agents.common.smart-verification-budget'
title: 'Smart Verification Budget'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/verification'
    - 'routing/performance'
parent:
    - '[[common/lightweight-routing-policy|Lightweight Routing Policy]]'
related:
    - '[[common/diff-impact-verification-rules|Diff Impact Verification Rules]]'
    - '[[common/mcp-availability-detection-rules|MCP Availability Detection Rules]]'
    - '[[common/rendered-visual-verification-policy|Rendered Visual Verification Policy]]'
depends_on: []
---

# Smart Verification Budget

Purpose: keep verification proportional to the actual change, user intent, risk, and repeated-failure history.

## Verification Levels

Use the smallest level that gives honest evidence.

```text
Level 0: no code changed
- Answer only. Do not run commands.

Level 1: docs or comments only
- Do not run lint, typecheck, build, browser, or MCP checks unless docs tooling changed.

Level 2: CSS-only local visual tweak
- Check or format changed CSS files when a formatter exists.
- Do not run full-repository lint by default.
- Do not run typecheck by default.
- Do not start a dev server by default.
- Do not inspect Playwright packages or MCP installation state.
- Do not run rendered visual QA unless requested, repeated, or layout-affecting risk is present.

Level 3: local component JSX/TSX change
- Check or format changed files.
- Run changed-file lint when available.
- Run targeted typecheck or build only when imports, JSX, TypeScript, dependency usage, or bundling behavior changed.

Level 4: shared component, route, data, state, form, navigation, or build-boundary change
- Run the smallest relevant existing lint/type/build command.
- Verify directly affected routes or flows when the app can run and the task requires it.

Level 5: visual implementation from a spec or repeated visual failure
- Use rendered visual evidence when the capability is available.
- Limit checks to directly affected routes, viewports, and states.

Level 6: repeated failure or high-risk regression
- Use a bounded verification loop with acceptance criteria, attempt limit, changed hypothesis, and final evidence.
```

## Escalation Rules

Escalate one level only when one of these is true:

- the user explicitly asks for heavier verification;
- the same issue has been reported again after a previous fix;
- targeted checks fail in a way tied to the current change;
- the diff touches shared layout, route, state, data, form, navigation, build, or cross-page ownership;
- the changed CSS affects layout, typography, positioning, overflow, media queries, or responsive behavior.

## De-escalation Rules

Do not escalate merely because tools are available.

Do not start a local server or browser session after sufficient source or build evidence for a low-risk change unless rendered evidence is explicitly requested or the change remains visually risky.

Do not run broad repository commands before changed-file checks for lightweight work.

## Cost And Context Rule

For small tasks, preserve user quota and context budget. A heavier check must have a named risk, directly affected surface, repeated-failure signal, or explicit user request.

## Final Report

Report the chosen verification level, exact commands run, skipped heavier checks, and why heavier checks were unnecessary or blocked.
