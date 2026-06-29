---
name: frontend-quality-reviewer
description: Use for evidence-backed frontend quality review of code, UI implementation, architecture boundaries, TypeScript, security, performance, verification, and anti-slop concerns. Produces pass, pass with concerns, or fail. Do not use to perform broad rewrites, create tests, install tools, or implement fixes unless separately requested.
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
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[common/review-severity-model|Review Severity Model]]'
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

Review frontend work for correctness, maintainability, security, performance,
TypeScript safety, architecture fit, visual quality, and verification honesty
without turning review findings into an unapproved rewrite.

## When To Use

Use this skill when:

- the user asks for review, audit, critique, or quality check;
- a significant frontend implementation needs a final quality pass;
- a bugfix or refactor has broad impact and review is appropriate;
- claims about security, performance, architecture, visual fidelity, or
  verification need evidence.

## When Not To Use

Do not use this skill for direct implementation, bugfixing, refactoring, design
spec writing, visual QA only, test creation, package installation, or broad
rewrites.

If review finds required fixes, report them first. Do not apply fixes unless
the user asked for a combined review-and-fix task or explicitly approves a
follow-up fix.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/review-severity-model.md`.
3. Read `common/typescript-discipline.md` for TypeScript surfaces.
4. Read `common/security-review-rules.md` when auth, secrets, unsafe HTML,
   redirects, external input, or permissions are in scope.
5. Read `common/performance-review-rules.md` when performance claims are in
   scope.
6. Read `common/build-tool-boundary-rules.md` and
   `common/lint-verification-rules.md` when code changed.
7. Read affected source files, diffs, project overlays, verification output,
   and rendered evidence needed for the review.
8. Do not read `README.md` or `SUMMARY.md` during normal runtime.

## Tool Contract

- May inspect diffs, affected files, project overlays, and verification output.
- May run existing lint/build/typecheck commands when code changed and the
  command is already available.
- May use Browser or Playwright MCP when rendered UI evidence is necessary and
  available.
- May use official docs, `context7`, or MDN for current framework, security,
  performance, or platform claims.
- Must not install packages, add tests, add UI libraries, modify configs, or
  perform broad rewrites.

## Workflow

1. Define review scope and changed surfaces.
2. Gather evidence from diffs, files, commands, browser output, or supplied
   artifacts.
3. Check correctness, architecture boundaries, TypeScript safety, accessibility,
   visual quality, security, performance, build/workspace fit, and verification
   honesty only where relevant.
4. Assign severity labels: `blocking`, `high`, `medium`, `low`, `nit`, or
   `praise`.
5. Distinguish required fixes from optional improvements.
6. Produce verdict:
   - `pass` when no required fixes are found;
   - `pass with concerns` when no required fixes remain but risks exist;
   - `fail` when blocking or unresolved required high issues exist.
7. Check lint result when code changed and a lint command exists.
8. Report unknowns and blocked checks honestly.

## Output Contract

Return findings first, ordered by severity:

```text
Verdict:
Required fixes:
Optional improvements:
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
- Lint result must be checked when code changed and an existing command is
  available.
- Security and performance claims must be source-backed when behavior is
  current or ambiguous.
- No testing workflow, UI library, package install, or framework migration may
  be introduced by default.

## Trigger Evals

Should trigger:

- "Review this frontend change before I merge it."
- "Check this implementation for AI slop and quality issues."
- "Audit the TypeScript, performance, and accessibility risks here."
- "Give me a pass/fail verdict on this UI implementation."

Should not trigger:

- "Fix this bug."
- "Refactor this component."
- "Run visual QA only."
- "Create tests for this feature."

## Reference Map

- `common/review-severity-model.md`
- `common/security-review-rules.md`
- `common/performance-review-rules.md`
- `common/typescript-discipline.md`
- `common/build-tool-boundary-rules.md`
- `common/lint-verification-rules.md`
