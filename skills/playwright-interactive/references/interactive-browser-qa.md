---
id: 'agents.skills.playwright-interactive.references.interactive-browser-qa'
title: 'Interactive Browser QA'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'playwright-interactive'
tags:
    - 'agents/skill-package'
    - 'frontend/verification'
    - 'frontend/browser'
    - 'agents/reference'
parent:
    - '[[skills/playwright-interactive/SKILL|Playwright Interactive]]'
related:
    - '[[skills/playwright-interactive/references/screenshot-and-viewport-checks|Screenshot And Viewport Checks]]'
depends_on:
    - '[[skills/playwright-interactive/SKILL|Playwright Interactive]]'
---

# Interactive Browser QA

Use this reference when starting, reusing, or debugging a persistent Playwright
session for local browser verification.

## Section Map

- `Preconditions` for setup and tool availability.
- `QA inventory` for coverage before testing.
- `Bootstrap pattern` for shared Playwright handles.
- `Web session modes` for desktop, mobile, and native-window checks.
- `Iteration loop` for reload, relaunch, functional QA, visual QA, and cleanup.
- `Optional Electron pass` for Electron-specific behavior.

## Preconditions

- `js_repl` must be available before using the persistent-session snippets.
- Playwright must already be installed in the workspace or explicitly approved
  for installation by the user.
- Browser binaries must already exist or be explicitly approved for
  installation.
- Run setup and browser control from the same workspace being debugged.
- For local web apps, keep the dev server in a persistent session and verify the
  port responds before `page.goto(...)`.
- Do not use production URLs, production systems, or production data.

## QA inventory

Write a short inventory before the browser pass:

- user requirements and acceptance criteria
- implemented user-visible features
- final-response claims that need evidence
- controls, mode switches, and state changes
- one main happy path
- at least two off-happy-path or exploratory checks for interactive products
- visual states that need screenshot review

Every user-visible claim in the final response must map to at least one
functional or visual check.

## Bootstrap pattern

Use shared top-level bindings so later `js_repl` cells can reuse handles:

```javascript
var chromium;
var browser;
var context;
var page;
var mobileContext;
var mobilePage;

({ chromium } = await import("playwright"));

var resetWebHandles = function () {
  context = undefined;
  page = undefined;
  mobileContext = undefined;
  mobilePage = undefined;
};

var ensureWebBrowser = async function () {
  if (browser && !browser.isConnected()) {
    browser = undefined;
    resetWebHandles();
  }

  browser ??= await chromium.launch({ headless: false });
  return browser;
};
```

If a handle is stale, set the handle to `undefined` and recreate it. Use
`js_repl_reset` only when the kernel itself is broken.

## Web session modes

Desktop default:

```javascript
var TARGET_URL = "http://127.0.0.1:3000";

await ensureWebBrowser();
context ??= await browser.newContext({
  viewport: { width: 1600, height: 900 },
});
page ??= await context.newPage();

await page.goto(TARGET_URL, { waitUntil: "domcontentloaded" });
console.log("Loaded:", await page.title());
```

Mobile default:

```javascript
var MOBILE_TARGET_URL = TARGET_URL;

await ensureWebBrowser();
mobileContext ??= await browser.newContext({
  viewport: { width: 390, height: 844 },
  isMobile: true,
  hasTouch: true,
});
mobilePage ??= await mobileContext.newPage();

await mobilePage.goto(MOBILE_TARGET_URL, { waitUntil: "domcontentloaded" });
console.log("Loaded mobile:", await mobilePage.title());
```

Native-window pass:

```javascript
await ensureWebBrowser();

await page?.close().catch(() => {});
await context?.close().catch(() => {});
page = undefined;
context = undefined;

context = await browser.newContext({ viewport: null });
page = await context.newPage();
await page.goto(TARGET_URL, { waitUntil: "domcontentloaded" });
```

Use native-window mode only as a separate pass when real window behavior, DPI,
or host-specific layout matters.

## Iteration loop

- Reload existing web contexts after renderer-only changes:

```javascript
for (const currentContext of [context, mobileContext]) {
  if (!currentContext) continue;
  for (const currentPage of currentContext.pages()) {
    await currentPage.reload({ waitUntil: "domcontentloaded" });
  }
}
```

- Use normal user input for signoff. `page.evaluate(...)` may inspect or stage
  state, but it does not count as user-input verification.
- Cover every meaningful visible control at least once.
- For toggles or reversible controls, test initial state, changed state, and
  return to initial state.
- Capture console/runtime errors during the pass.
- Run visual QA separately from functional QA.
- Keep screenshots for final evidence only after the UI reaches the state being
  evaluated.

Cleanup when the task is finished:

```javascript
if (mobileContext) await mobileContext.close().catch(() => {});
if (context) await context.close().catch(() => {});
if (browser) await browser.close().catch(() => {});

browser = undefined;
context = undefined;
page = undefined;
mobileContext = undefined;
mobilePage = undefined;
```

## Optional Electron pass

Use Electron only when the target app is Electron and the local workspace
already has the required dependency and entrypoint.

- Launch Electron through Playwright so the session owns the process.
- Treat Electron as native-window behavior by default.
- Reload renderer-only changes with `appWindow.reload(...)`.
- Relaunch after main-process, preload, or startup changes.
- Do not open scratch pages from an Electron context for screenshots; use the
  Electron-specific screenshot path in
  `references/screenshot-and-viewport-checks.md`.
