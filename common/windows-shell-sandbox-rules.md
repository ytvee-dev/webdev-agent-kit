---
id: 'agents.common.windows-shell-sandbox-rules'
title: 'Windows Shell Sandbox Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'quality/verification'
    - 'platform/windows'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/smart-verification-budget|Smart Verification Budget]]'
    - '[[common/lint-verification-rules|Lint Verification Rules]]'
    - '[[common/bounded-retry-rules|Bounded Retry Rules]]'
    - '[[common/rendered-visual-verification-policy|Rendered Visual Verification Policy]]'
depends_on: []
---

# Windows Shell Sandbox Rules

Purpose: prevent repeated failed verification attempts when Windows shell policy or sandbox boundaries block commands that may otherwise be valid.

## Recognize Shell And Sandbox Blocks

Classify a failure as `environment-blocked` or `sandbox-blocked`, not as a project code failure, when the evidence matches one of these patterns:

- PowerShell blocks `npm.ps1`, `pnpm.ps1`, `yarn.ps1`, or another package-manager shim because scripts are disabled.
- The command fails with `EACCES`, `EPERM`, `Access is denied`, `operation not permitted`, or equivalent filesystem access errors before project compilation starts.
- Vite, esbuild, SWC, Next.js, Playwright, or a dev server fails because the sandbox cannot access a binary, cache, config, parent directory, temporary directory, or spawned process.
- A dev server or browser verification tool cannot start for environment or permission reasons before the changed route or component is evaluated.

## Windows Package Manager Fallback

When PowerShell blocks a package-manager `.ps1` shim on Windows, do not change execution policy and do not treat the result as a lint, build, or test failure.

Use exactly one equivalent `.cmd` fallback when available:

```text
npm.cmd run <script>
pnpm.cmd run <script>
yarn.cmd <script>
```

If the `.cmd` fallback passes, report the original PowerShell block as an environment fallback, not as a fixed code issue.

If the `.cmd` fallback fails with real lint, type, build, or application errors, classify those errors normally.

## Esbuild And Dev Server Sandbox Fallback

When build or dev-server startup fails because esbuild, Vite, Next.js, Playwright, or a spawned binary is blocked by sandbox access, make at most one approved fallback attempt outside the sandbox when the host supports approval.

If out-of-sandbox approval is unavailable, denied, or the same sandbox-class failure repeats, stop retrying and report rendered or build verification as blocked.

Do not repeatedly restart the dev server, browser, build, or the same command with cosmetic variations after a sandbox-class failure.

## Retry Budget

A retry is valid only when it changes the execution boundary or the command form in a way that addresses the blocker.

Allowed retry examples:

- `npm run lint` fails because `npm.ps1` is blocked -> run `npm.cmd run lint` once.
- `npm.cmd run build` fails because esbuild cannot access a sandboxed path -> request or use one out-of-sandbox run when available.

Invalid retry examples:

- Re-running `npm run lint` after a PowerShell execution-policy block.
- Re-running `npm.cmd run dev` several times after the same esbuild sandbox access error.
- Starting browser QA after the dev server failed to start for the same sandbox reason.
- Changing project code, scripts, dependencies, config, or execution policy to bypass a shell or sandbox blocker without explicit user approval.

## Reporting

When shell or sandbox limits affect verification, report:

```text
Command attempted:
Failure class: environment-blocked | sandbox-blocked
Evidence:
Fallback attempted:
Result:
Verification impact:
Approval needed:
```

Record durable host facts such as `Windows PowerShell requires npm.cmd` or `dev server requires out-of-sandbox approval` in local-only `project/verification-profile.md` when project context refresh or onboarding scope allows it.
