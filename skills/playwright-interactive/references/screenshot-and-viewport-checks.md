---
id: 'agents.skills.playwright-interactive.references.screenshot-and-viewport-checks'
title: 'Screenshot And Viewport Checks'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'playwright-interactive'
tags:
    - 'agents/skill-package'
    - 'frontend/verification'
    - 'frontend/visual-qa'
    - 'agents/reference'
parent:
    - '[[skills/playwright-interactive/SKILL|Playwright Interactive]]'
related:
    - '[[skills/playwright-interactive/references/interactive-browser-qa|Interactive Browser QA]]'
depends_on:
    - '[[skills/playwright-interactive/SKILL|Playwright Interactive]]'
---

# Screenshot And Viewport Checks

Use this reference when screenshots, responsive layout, viewport fit, canvas,
visual polish, or model-assisted coordinate follow-up matter.

## Section Map

- `Visual QA rules` for what screenshot review must cover.
- `Screenshot defaults` for CSS-pixel screenshot handling.
- `Viewport fit gate` for required numeric and visual checks.
- `Common failure modes` for debugging Playwright sessions.

## Visual QA rules

- Treat visual QA as separate from functional QA.
- Review the initial viewport before scrolling.
- Inspect every state named in the QA inventory, including at least one
  meaningful post-interaction state for interactive work.
- Inspect dense or loaded states, not only empty or collapsed states.
- For motion or transitions, inspect at least one in-transition state when it is
  relevant.
- Treat clipping, overflow, occlusion, unreadable text, weak contrast, broken
  layering, awkward spacing, and unstable layout as failures.
- Prefer viewport screenshots for signoff. Use full-page screenshots as
  secondary debugging artifacts.
- If screenshot review and numeric checks disagree, investigate. Visible
  clipping is a failure even when metrics look acceptable.

## Screenshot defaults

Prefer CSS-pixel screenshots for model-bound evidence and coordinate follow-up:

```javascript
var emitJpeg = async function (bytes) {
  await codex.emitImage({
    bytes,
    mimeType: "image/jpeg",
    detail: "original",
  });
};

var emitWebJpeg = async function (surface, options = {}) {
  await emitJpeg(await surface.screenshot({
    type: "jpeg",
    quality: 85,
    scale: "css",
    ...options,
  }));
};

var clickCssPoint = async function ({ surface, x, y, clip }) {
  await surface.mouse.click(
    clip ? clip.x + x : x,
    clip ? clip.y + y : y
  );
};

var tapCssPoint = async function ({ page, x, y, clip }) {
  await page.touchscreen.tap(
    clip ? clip.x + x : x,
    clip ? clip.y + y : y
  );
};
```

Use `page` or `mobilePage` as the `surface`. For clipped screenshots, add the
clip origin back when clicking or tapping.

Desktop:

```javascript
await emitWebJpeg(page);
```

Mobile:

```javascript
await emitWebJpeg(mobilePage);
```

Raw screenshots are an exception for pixel-fidelity debugging, such as DPI or
Retina artifacts. They are not the default for model-bound coordinate work.

Electron screenshot rule:

- Do not use `appWindow.context().newPage()` or
  `electronApp.context().newPage()` as a scratch screenshot page.
- Capture Electron screenshots through the main process and normalize to the
  renderer content size when model-bound coordinates matter.

## Viewport fit gate

Define the intended initial view before signoff. For app-like shells, games,
editors, dashboards, and tools, the intended initial view includes the primary
interactive surface plus the controls and status needed to use it.

Run a document-level check:

```javascript
console.log(await page.evaluate(() => ({
  innerWidth: window.innerWidth,
  innerHeight: window.innerHeight,
  clientWidth: document.documentElement.clientWidth,
  clientHeight: document.documentElement.clientHeight,
  scrollWidth: document.documentElement.scrollWidth,
  scrollHeight: document.documentElement.scrollHeight,
  canScrollX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
  canScrollY: document.documentElement.scrollHeight > document.documentElement.clientHeight,
})));
```

Also check required regions with `getBoundingClientRect()` when clipping is a
realistic risk. Document-level metrics do not catch every fixed-shell or
hidden-overflow failure.

Signoff fails when a required visible region is clipped, cut off, obscured, or
pushed outside the viewport in the intended initial view. Scrolling is acceptable
only when the product is designed to scroll and the startup view still exposes
the required starting context.

## Common failure modes

- `Cannot find module 'playwright'`: Playwright is not installed in the current
  workspace. Ask before installing dependencies.
- Browser executable missing: ask before running `npx playwright install
  chromium`.
- `page.goto: net::ERR_CONNECTION_REFUSED`: verify the dev server is still
  running and prefer `http://127.0.0.1:<port>`.
- Stale page or context: set the stale binding to `undefined` and recreate it.
- `Identifier has already been declared`: reuse existing `var` handles or choose
  a new binding name.
- `js_repl` timeout or reset: rerun bootstrap and keep later cells shorter.
- Immediate browser launch or network failure under sandboxing: report the
  sandbox blocker and the verification that was completed.
