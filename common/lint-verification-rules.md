---
id: 'agents.common.lint-verification-rules'
title: 'Lint Verification Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'quality/lint'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-linter-manager/SKILL|Frontend Linter Manager]]'
    - '[[common/windows-shell-sandbox-rules|Windows Shell Sandbox Rules]]'
depends_on: []
---

# Lint Verification Rules

Purpose: require honest lint verification for code-changing frontend work.

## Core Rule

After every code-changing fix, feature, refactor, or implementation slice, run the smallest relevant existing lint command before reporting completion.

If no lint command exists, say that lint was not run and explain the impact.

## Applies To

- Bugfixes.
- Feature implementation.
- Layout implementation.
- Refactors.
- Approved greenfield code creation.
- Linter configuration changes.

## Does Not Apply To

- Planning-only work.
- Design-only work.
- Documentation-only work.
- README-only work.
- Analysis-only work.

## Windows Shell Fallback Rule

On Windows, if `npm run <script>`, `pnpm <script>`, or `yarn <script>` fails because PowerShell blocks a `.ps1` shim, retry once with the equivalent `.cmd` command when available.

Do not change PowerShell execution policy, dependencies, scripts, or config to bypass that block.

If the `.cmd` fallback runs and produces lint output, classify that output normally. If it fails with the same shell or sandbox blocker, stop and report lint verification as blocked by environment.

## Setup Rule

The agent may set up linting only when the user explicitly asks for it or approves a setup plan.

Before setup, inspect package manager, framework, TypeScript usage, React usage, existing formatter or linter config, workspace layout, and package scripts.

Do not change dependencies, scripts, or config files without explicit user approval.

## Uploaded Model

When the user asks to use the provided rules, use the uploaded flat ESLint model as the preferred source pattern. It includes TypeScript type-checked rules, React rules, React Hooks rules, JSX accessibility rules, SonarJS rules, Prettier compatibility, ignore rules, optional strict presets, and a format-lint-fix helper.

## Reporting

Every code-changing final response must report lint command, lint result, and unresolved lint issues. If lint was not run, report why.

When a Windows shell or sandbox fallback was used, also report the original blocked command, fallback command, and verification impact.
