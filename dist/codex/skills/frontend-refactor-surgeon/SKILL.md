---
name: frontend-refactor-surgeon
description: Use for behavior-preserving frontend refactors with clear boundaries, including component extraction, file reorganization, prop/interface cleanup, state simplification, and TypeScript tightening. Do not use for bugfixes, feature work, broad rewrites, redesign, package installation, or behavior changes without approval.
---

# Frontend Refactor Surgeon

## Purpose

Refactor frontend code while preserving behavior, rendered output, and public
contracts unless the user explicitly approves a behavior change.

## When To Use

Use this skill when the user asks to:

- simplify or reorganize frontend code;
- extract components, hooks, utilities, or styles;
- tighten TypeScript types;
- remove duplication within a clear frontend boundary;
- prepare code for a future change without adding the feature yet.

## When Not To Use

Do not use this skill for bugfix-first debugging, new feature implementation,
design/spec work, visual QA only, broad rewrites without a boundary, backend
refactors, package installation, or testing workflow creation.

Use `frontend-bugfix-debugger` when the primary goal is to fix a defect.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when workflow level is unclear.
3. Read `common/refactor-safety-rules.md`.
4. Read `common/typescript-discipline.md`.
5. Read relevant boundary docs such as `common/state-ownership-rules.md` when
   the refactor touches state.
6. Read project overlays and affected source files needed to define the
   behavior boundary.
7. Do not read `README.md` or `SUMMARY.md` during normal runtime.

## Tool Contract

- May inspect affected source, styles, configs, and project overlays.
- May run existing lint, typecheck, build, or preview commands relevant to the
  refactor.
- May use Browser or Playwright MCP when rendered output must be checked.
- Must not install packages, add testing workflows, change build tooling, add
  UI libraries, or migrate frameworks without explicit approval.
- Must not change production systems, secrets, or production data.

## Workflow

1. Define the refactor boundary and behavior contract.
2. Identify public APIs, rendered output, route behavior, state ownership,
   accessibility, and TypeScript contracts that must remain stable.
3. Split the refactor into small mechanical steps.
4. Edit one boundary at a time.
5. Preserve project naming, folder, styling, and state conventions.
6. Run the smallest relevant verification after meaningful edits.
7. Use `frontend-linter-manager` after code-changing work when a lint command
   exists.
8. Use `frontend-visual-qa` when rendered UI could have changed.
9. Stop and ask before behavior change, architecture expansion, dependency
   changes, or broad rewrite.

## Output Contract

Return:

```text
Refactor boundary:
Behavior preserved:
Changes made:
Verification:
Rendered QA:
Deferred work:
Risks:
```

## Validation Gates

- The behavior boundary must be explicit before editing.
- Public contracts must remain stable unless approved.
- Refactor must not introduce feature work by default.
- Lint verification must run after code changes when a command exists.
- Rendered UI changes or risk must trigger visual QA when applicable.
- No testing workflow, UI library, package install, or framework migration may
  be introduced by default.

## Trigger Evals

Should trigger:

- "Refactor this component without changing behavior."
- "Extract the repeated dashboard card markup safely."
- "Tighten these frontend TypeScript props."
- "Clean up this route implementation but keep the UI the same."

Should not trigger:

- "Fix this runtime error."
- "Add this new feature."
- "Review this PR."
- "Create tests for this component."

## Reference Map

- `common/refactor-safety-rules.md`
- `common/typescript-discipline.md`
- `common/state-ownership-rules.md`
- `project/verification-profile.md`
