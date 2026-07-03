---
name: frontend-bugfix-debugger
description: Use for evidence-first frontend bugfixes, unclear UI/runtime errors, broken routes, styling regressions, hydration/client issues, and small defects that need symptom reproduction before code changes. Supports bounded retry when verification fails. Do not use for planned refactors, broad redesigns, quality review only, test generation, or backend-only debugging.
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
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/debugging-evidence-rules|Debugging Evidence Rules]]'
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/bounded-retry-rules|Bounded Retry Rules]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
    - '[[common/typescript-discipline|TypeScript Discipline]]'
    - '[[skills/frontend-linter-manager/SKILL|Frontend Linter Manager]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Bugfix Debugger

## Purpose

Fix frontend defects from symptoms and evidence while keeping the change small. When verification fails and repair is in scope, use a bounded retry loop instead of guessing repeatedly.

## When To Use

Use this skill when the user asks to fix a frontend runtime, console, hydration, routing, rendering, interaction, styling, responsive, TypeScript, or build defect that needs evidence.

## When Not To Use

Do not use this skill for planned refactors, broad quality review, visual QA only, design intake, greenfield planning, backend-only debugging, package installation, or test creation.

If the task is a behavior-preserving refactor, use `frontend-refactor-surgeon`. If the user asks only for review, use `frontend-quality-reviewer`.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when workflow level is unclear.
3. Read `common/debugging-evidence-rules.md`.
4. Read `common/agent-loop-policy.md`, `common/bounded-retry-rules.md`, and `common/verification-loop-rules.md` when the user asks to continue until verification passes or repeated failure appears.
5. Read `common/typescript-discipline.md` for TypeScript work.
6. Read relevant project overlays, especially `project/verification-profile.md` and path indexes when present.
7. Read the error, log, route, component, styles, or source files needed for the active bug hypothesis.
8. Do not read human-facing `README.md` during normal runtime.

## Tool Contract

- May run existing project commands needed to reproduce or verify the symptom.
- May use Browser or Playwright MCP for rendered bug reproduction when available.
- May use `context7` or official docs when current framework behavior affects the fix.
- May use MDN when browser platform behavior affects the bug.
- Must not install packages, add test workflows, change build tooling, or add UI libraries without explicit approval.
- Must not interact with production systems, secrets, or production data.

## Workflow

1. Classify workflow level and keep one clear bug lightweight.
2. Record the symptom, reproduction path, and current evidence.
3. Form one bug hypothesis and inspect only files relevant to it.
4. Fix the smallest cause that explains the evidence.
5. Preserve existing project conventions, state ownership, accessibility, and TypeScript strictness.
6. Run the same failing command, interaction, route check, or visual check when possible.
7. If verification fails and the failure is related to the current change, apply `common/bounded-retry-rules.md`: record the failed attempt, identify the likely cause, change hypothesis or implementation strategy, avoid repeating the same patch, and retry only within the attempt limit.
8. If verification fails for likely pre-existing or unrelated reasons, document it separately and do not expand scope without approval.
9. Use `frontend-linter-manager` after code-changing work when a lint command exists.
10. Use `frontend-visual-qa` when the fix changes rendered UI.
11. Use `frontend-quality-reviewer` when the loop repaired a non-trivial failure or the user asks for review.
12. Report evidence, root cause, fix, verification, attempt count, and any remaining risk.

## Output Contract

```text
Symptom:
Evidence:
Root cause:
Fix:
Attempts:
Verification:
Rendered QA:
Remaining risk:
```

## Validation Gates

- The fix must be tied to observed evidence.
- The change must be the smallest scoped correction that addresses the symptom.
- Retry attempts must use new evidence or a changed hypothesis.
- TypeScript safety must not be weakened without explanation and approval.
- Lint verification must run after code changes when a command exists.
- UI changes must trigger visual QA when applicable.
- No testing workflow, UI library, package install, or framework migration may be introduced by default.

## Trigger Evals

Should trigger:

- "Reproduce and fix this broken route."
- "This UI bug survived the first fix; change the hypothesis and retry."

Should not trigger:

- "Refactor this component without changing behavior."
- "Review this implementation without fixing it."

## Reference Map

- `common/debugging-evidence-rules.md`
- `common/agent-loop-policy.md`
- `common/bounded-retry-rules.md`
- `common/verification-loop-rules.md`
- `common/typescript-discipline.md`
- `project/verification-profile.md`
