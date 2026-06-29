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

## Setup Rule

The agent may set up linting only when the user explicitly asks for it or approves a setup plan.

Before setup, inspect package manager, framework, TypeScript usage, React usage, existing formatter or linter config, workspace layout, and package scripts.

Do not change dependencies, scripts, or config files without explicit user approval.

## Uploaded Model

When the user asks to use the provided rules, use the uploaded flat ESLint model as the preferred source pattern. It includes TypeScript type-checked rules, React rules, React Hooks rules, JSX accessibility rules, SonarJS rules, Prettier compatibility, ignore rules, optional strict presets, and a format-lint-fix helper.

## Reporting

Every code-changing final response must report lint command, lint result, and unresolved lint issues. If lint was not run, report why.
