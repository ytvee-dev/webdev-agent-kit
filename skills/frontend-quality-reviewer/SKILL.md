---
name: frontend-quality-reviewer
description: Use for evidence-backed frontend quality review of code, UI implementation, architecture boundaries, TypeScript, security, performance, verification, decomposition, UX gates, and anti-slop concerns. Produces pass, pass with concerns, or fail. Do not use to perform broad rewrites, create tests, install tools, or implement fixes unless separately requested.
id: 'agents.skills.frontend-quality-reviewer.skill'
title: 'Frontend Quality Reviewer'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-quality-reviewer'
tags:
    - 'agents/skill-package'
    - 'frontend/review'
    - 'workflow/quality-review'
parent: []
related:
    - '[[common/review-severity-model|Review Severity Model]]'
    - '[[common/approved-patterns|Approved Patterns]]'
    - '[[common/anti-patterns|Common Anti-Patterns]]'
    - '[[common/ui-ux-priority-checklist|UI UX Priority Checklist]]'
    - '[[common/css-modules-specificity-rules|CSS Modules Specificity Rules]]'
    - '[[common/form-feedback-rules|Form Feedback Rules]]'
    - '[[common/navigation-ux-rules|Navigation UX Rules]]'
    - '[[common/data-visualization-rules|Data Visualization Rules]]'
    - '[[common/icon-quality-rules|Icon Quality Rules]]'
    - '[[common/mobile-responsive-rules|Mobile Responsive Rules]]'
    - '[[common/security-review-rules|Security Review Rules]]'
    - '[[common/performance-review-rules|Performance Review Rules]]'
    - '[[common/typescript-discipline|TypeScript Discipline]]'
    - '[[common/build-tool-boundary-rules|Build Tool Boundary Rules]]'
    - '[[common/lint-verification-rules|Lint Verification Rules]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Quality Reviewer

## Purpose

Review frontend work for correctness, maintainability, decomposition, security, performance, TypeScript safety, architecture fit, visual quality, UX gates, and verification honesty without turning review findings into an unapproved rewrite.

## When To Use

Use this skill when:

- the user asks for review, audit, critique, or quality check;
- a significant frontend implementation needs a final quality pass;
- a bugfix or refactor has broad impact and review is appropriate;
- claims about security, performance, architecture, decomposition, visual fidelity, UX, or verification need evidence.

## When Not To Use

Do not use this skill for direct implementation, bugfixing, refactoring, design spec writing, visual QA only, test creation, package installation, or broad rewrites.

If review finds required fixes, report them first. Do not apply fixes unless the user asked for a combined review-and-fix task or explicitly approves a follow-up fix.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/review-severity-model.md`.
3. Read `common/approved-patterns.md` and `common/anti-patterns.md` when reviewing changed components.
4. Read `common/ui-ux-priority-checklist.md` when reviewing rendered UI or user interaction.
5. Read conditional UX rules only when the changed surface includes them:
   - `common/css-modules-specificity-rules.md` for CSS Modules changes;
   - `common/form-feedback-rules.md` for forms and feedback states;
   - `common/navigation-ux-rules.md` for navigation and route flows;
   - `common/data-visualization-rules.md` for dashboards, charts, tables, metrics, or reports;
   - `common/icon-quality-rules.md` for icons or visual symbols;
   - `common/mobile-responsive-rules.md` for responsive surfaces.
6. Read `common/typescript-discipline.md` for TypeScript surfaces.
7. Read `common/security-review-rules.md` when auth, secrets, unsafe HTML, redirects, external input, or permissions are in scope.
8. Read `common/performance-review-rules.md` when performance claims are in scope.
9. Read `common/build-tool-boundary-rules.md` and `common/lint-verification-rules.md` when code changed.
10. Read affected source files, diffs, project overlays, verification output, and rendered evidence needed for the review.
11. Do not read `README.md` during normal runtime.

## Tool Contract

- May inspect diffs, affected files, project overlays, and verification output.
- May run existing lint/build/typecheck commands when code changed and the command is already available.
- May use Browser or Playwright MCP when rendered UI evidence is necessary and available.
- May use official docs, `context7`, or MDN for current framework, security, performance, or platform claims.
- Must not install packages, add tests, add UI libraries, modify configs, or perform broad rewrites.

## Workflow

1. Define review scope and changed surfaces.
2. Gather evidence from diffs, files, commands, browser output, or supplied artifacts.
3. Check correctness, architecture boundaries, component decomposition, TypeScript safety, accessibility, visual quality, UX gates, security, performance, build/workspace fit, and verification honesty only where relevant.
4. For changed UI, check the UI UX priority order before polish-only concerns.
5. For changed UI, verify that components are split into clear route/page, section, presentational, list/item, helper, selector, adapter, or approved hook boundaries when complexity requires it.
6. Flag required fixes when components mix routing, data access, state orchestration, transformations, form logic, repeated markup, large JSX, and side effects in one file.
7. Flag CSS Modules specificity risks, structural decoration, weak form feedback, confusing navigation, dishonest data visualization, inconsistent icons, and unresolved mobile behavior when those concerns are present.
8. Assign severity labels: `blocking`, `high`, `medium`, `low`, `nit`, or `praise`.
9. Distinguish required fixes from optional improvements.
10. Produce verdict:
    - `pass` when no required fixes are found;
    - `pass with concerns` when no required fixes remain but risks exist;
    - `fail` when blocking or unresolved required high issues exist.
11. Check lint result when code changed and a lint command exists.
12. Report unknowns and blocked checks honestly.

## Output Contract

Return findings first, ordered by severity:

```text
Verdict:
Required fixes:
Optional improvements:
Decomposition review:
UX gates reviewed:
Evidence checked:
Lint/build/visual verification:
Unknowns or blocked checks:
Praise:
```

Use file and line references for code findings whenever available.

## Validation Gates

- Every blocking or high claim must cite concrete evidence.
- Review must not trigger broad rewrite by itself.
- Required fixes and optional improvements must be separate.
- Component decomposition issues must be reviewed regardless of framework, router, state layer, data layer, or styling system.
- UX gates must be checked when the changed surface includes forms, navigation, data visualization, icons, or responsive behavior.
- Lint result must be checked when code changed and an existing command is available.
- Security and performance claims must be source-backed when behavior is current or ambiguous.
- No testing workflow, UI library, package install, or framework migration may be introduced by default.

## Trigger Evals

Should trigger:

- "Review this frontend change before I merge it."
- "Check this implementation for AI slop and quality issues."
- "Audit the TypeScript, performance, and accessibility risks here."
- "Give me a pass/fail verdict on this UI implementation."
- "Check whether this component should be split."

Should not trigger:

- "Fix this bug."
- "Refactor this component."
- "Run visual QA only."
- "Create tests for this feature."

## Reference Map

- `common/review-severity-model.md`
- `common/approved-patterns.md`
- `common/anti-patterns.md`
- `common/ui-ux-priority-checklist.md`
- `common/css-modules-specificity-rules.md`
- `common/form-feedback-rules.md`
- `common/navigation-ux-rules.md`
- `common/data-visualization-rules.md`
- `common/icon-quality-rules.md`
- `common/mobile-responsive-rules.md`
- `common/security-review-rules.md`
- `common/performance-review-rules.md`
- `common/typescript-discipline.md`
- `common/build-tool-boundary-rules.md`
- `common/lint-verification-rules.md`
