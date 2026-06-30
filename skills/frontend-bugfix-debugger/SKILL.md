---
name: frontend-bugfix-debugger
description: Use for evidence-first frontend bugfixes, unclear UI/runtime errors, broken routes, styling regressions, hydration/client issues, and small defects that need symptom reproduction before code changes. Do not use for planned refactors, broad redesigns, quality review only, test generation, or backend-only debugging.
id: 'agents.skills.frontend-bugfix-debugger.skill'
title: 'Frontend Bugfix Debugger'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-bugfix-debugger'
tags:
    - 'agents/skill-package'
    - 'frontend/debugging'
    - 'workflow/bugfix'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[common/debugging-evidence-rules|Debugging Evidence Rules]]'
    - '[[common/typescript-discipline|TypeScript Discipline]]'
    - '[[skills/frontend-linter-manager/SKILL|Frontend Linter Manager]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Bugfix Debugger

## Purpose

Fix frontend defects from symptoms and evidence while keeping the change small.

## When To Use

Use this skill when the user asks to fix:

- a frontend runtime, console, hydration, routing, rendering, or interaction bug;
- a styling or responsive regression;
- an unclear TypeScript or build error in frontend code;
- a broken UI state that needs reproduction or evidence;
- a lightweight or standard bugfix where the root cause is not already obvious.

## When Not To Use

Do not use this skill for planned refactors, broad quality review, visual QA
only, design intake, greenfield planning, backend-only debugging, package
installation, or test creation.

If the task is a behavior-preserving refactor, use
`frontend-refactor-surgeon`. If the user asks only for review, use
`frontend-quality-reviewer`.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when workflow level is unclear.
3. Read `common/debugging-evidence-rules.md`.
4. Read `common/typescript-discipline.md` for TypeScript work.
5. Read relevant project overlays, especially `project/verification-profile.md`
   and path indexes when present.
6. Read the error, log, route, component, styles, or source files needed for
   the active bug hypothesis.
7. Do not read `README.md` or `SUMMARY.md` during normal runtime.

## Tool Contract

- May run existing project commands needed to reproduce or verify the symptom.
- May use Browser or Playwright MCP for rendered bug reproduction when available.
- May use `context7` or official docs when current framework behavior affects
  the fix.
- May use MDN when browser platform behavior affects the bug.
- Must not install packages, add test workflows, change build tooling, or add UI
  libraries without explicit approval.
- Must not interact with production systems, secrets, or production data.

## Workflow

1. Classify workflow level.
   - Keep one clear bug lightweight.
   - Escalate to standard only when root cause, ownership, or verification
     requires more than a narrow slice.
2. Record the symptom, reproduction path, and current evidence.
3. Form one bug hypothesis and inspect only files relevant to it.
4. Fix the smallest cause that explains the evidence.
5. Preserve existing project conventions, state ownership, accessibility, and
   TypeScript strictness.
6. Run the same failing command, interaction, route check, or visual check when
   possible.
7. Use `frontend-linter-manager` after code-changing work when a lint command
   exists.
8. Use `frontend-visual-qa` when the fix changes rendered UI.
9. Report evidence, root cause, fix, verification, and any remaining risk.

## Output Contract

Return:

```text
Symptom:
Evidence:
Root cause:
Fix:
Verification:
Rendered QA:
Remaining risk:
```

## Validation Gates

- The fix must be tied to observed evidence.
- The change must be the smallest scoped correction that addresses the symptom.
- TypeScript safety must not be weakened without explanation and approval.
- Lint verification must run after code changes when a command exists.
- UI changes must trigger visual QA when applicable.
- No testing workflow, UI library, package install, or framework migration may
  be introduced by default.

## Trigger Evals

Should trigger:

- "Fix this hydration error on the dashboard."
- "This route renders blank; debug and patch it."
- "The mobile layout broke after the last change."
- "Find why this frontend TypeScript error happens and fix it."

Should not trigger:

- "Refactor this component without changing behavior."
- "Review this PR for quality issues."
- "Create tests for this bug."
- "Write a design spec from these screenshots."

## Reference Map

- `common/debugging-evidence-rules.md`
- `common/typescript-discipline.md`
- `project/verification-profile.md`
