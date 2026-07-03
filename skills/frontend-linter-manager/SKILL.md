---
name: frontend-linter-manager
description: Use when a code-changing frontend task needs lint verification, lint repair loops for related failures, or when the user explicitly asks to add lint setup. Prefer existing project lint commands. Do not change dependencies, scripts, or config files without explicit user approval.
id: 'agents.skills.frontend-linter-manager.skill'
title: 'Frontend Linter Manager'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-linter-manager'
tags:
    - 'agents/skill-package'
    - 'agents/quality'
    - 'workflow/lint'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/bounded-retry-rules|Bounded Retry Rules]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Linter Manager

## Purpose

Run or plan lint verification for frontend code changes, repair related lint failures within a bounded loop, and manage user-requested lint setup safely.

## When To Use

Use this skill after any code-changing fix, feature, refactor, implementation slice, or approved greenfield code creation.

Use it before code changes only when the user explicitly asks to add or repair lint setup.

## When Not To Use

Do not use this skill for planning-only, design-only, documentation-only, README-only, or analysis-only tasks. Do not treat lint setup as a testing workflow.

## Required Context

1. Read `AGENTS.md`.
2. Read package scripts or `project/verification-profile.md` to find existing lint commands.
3. Read `common/verification-loop-rules.md` and `common/bounded-retry-rules.md` when lint repair is in scope.
4. Read only files needed to understand the package manager or workspace boundary.
5. Do not read `README.md` or `SUMMARY.md` during normal runtime.

## Tool Contract

- May run an existing lint command after code changes.
- May inspect package scripts and workspace files.
- May update `project/verification-profile.md` when durable lint command facts are useful.
- May fix lint failures related to the current change when safe and in scope.
- Must not add packages, scripts, or config files without explicit user approval.
- Must not create tests or testing workflows.
- Must not introduce UI component libraries.

## Workflow

1. Detect the smallest relevant existing lint command.
2. Run that command after the code change.
3. If lint passes, record command and result.
4. If lint fails, classify failures as related, likely pre-existing, unrelated environment issue, blocked, or unknown.
5. If lint fails because of the current change, fix it when safe and in scope.
6. Rerun the same lint command after related fixes.
7. Use bounded retry rules when multiple related lint repair attempts are needed.
8. Do not switch to an easier command just to claim success.
9. Report lint command, result, attempt count, and unresolved lint issues.
10. If no lint command exists, report that lint was not run.
11. If the user asks for lint setup, propose a setup plan first and wait for approval.

## User-Provided ESLint Model

When the user asks to add the provided lint rules, use the uploaded flat ESLint model as the preferred source pattern.

The model includes TypeScript type-checked rules, React rules, React Hooks rules, JSX accessibility rules, SonarJS rules, Prettier compatibility, ignore rules, optional strict presets, and a format-lint-fix helper.

Adapt the model to the host project after inspecting the existing package manager, framework, TypeScript usage, React usage, formatter or linter config, workspace layout, and scripts.

## Output Contract

```text
Lint command run:
Lint result:
Attempts:
Related failures fixed:
Unresolved lint issues:
```

If lint was not run, include the reason and impact.

## Validation Gates

- Lint was run for code-changing work when a command exists.
- Lint status is reported honestly.
- Related lint repairs use bounded retry rules.
- Unrelated or pre-existing failures are not silently claimed as fixed.
- No dependency, script, or config change happened without approval.
- No testing workflow was introduced.
- No UI component library was introduced.

## Reference Map

- `AGENTS.md` - canonical policy and routing.
- `common/verification-loop-rules.md` - verification classification and rerun rules.
- `common/bounded-retry-rules.md` - bounded repair loop rules.
- `project/verification-profile.md` - local-only verification commands.
- user-provided ESLint model - preferred setup pattern when setup is explicitly requested.
