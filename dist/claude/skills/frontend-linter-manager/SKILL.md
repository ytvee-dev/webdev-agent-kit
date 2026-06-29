---
name: frontend-linter-manager
description: Use when a code-changing frontend task needs lint verification, or when the user explicitly asks to add lint setup. Prefer existing project lint commands. Do not change dependencies, scripts, or config files without explicit user approval.
---

# Frontend Linter Manager

## Purpose

Run or plan lint verification for frontend code changes, and manage user-requested lint setup safely.

## When To Use

Use this skill after any code-changing fix, feature, refactor, implementation slice, or approved greenfield code creation.

Use it before code changes only when the user explicitly asks to add or repair lint setup.

## When Not To Use

Do not use this skill for planning-only, design-only, documentation-only, README-only, or analysis-only tasks.

Do not treat lint setup as a testing workflow.

## Required Context

1. Read `AGENTS.md`.
2. Read package scripts or `project/verification-profile.md` to find existing lint commands.
3. Read only files needed to understand the package manager or workspace boundary.
4. Do not read `README.md` or `SUMMARY.md` during normal runtime.

## Tool Contract

- May run an existing lint command after code changes.
- May inspect package scripts and workspace files.
- May update `project/verification-profile.md` when durable lint command facts are useful.
- Must not add packages, scripts, or config files without explicit user approval.
- Must not create tests or testing workflows.
- Must not introduce UI component libraries.

## Workflow

1. Detect the smallest relevant existing lint command.
2. Run that command after the code change.
3. If lint fails because of the current change, fix it when safe and in scope.
4. Run the same command again.
5. Report lint command, lint result, and unresolved lint issues.
6. If no lint command exists, report that lint was not run.
7. If the user asks for lint setup, propose a setup plan first and wait for approval.

## User-Provided ESLint Model

When the user asks to add the provided lint rules, use the uploaded flat ESLint model as the preferred source pattern.

The model includes TypeScript type-checked rules, React rules, React Hooks rules, JSX accessibility rules, SonarJS rules, Prettier compatibility, ignore rules, optional strict presets, and a format-lint-fix helper.

Adapt the model to the host project after inspecting the existing package manager, framework, TypeScript usage, React usage, formatter or linter config, workspace layout, and scripts.

## Output Contract

Return:

```text
Lint command run:
Lint result:
Unresolved lint issues:
```

If lint was not run, include the reason and impact.

## Validation Gates

Before finishing, verify:

- lint was run for code-changing work when a command exists;
- lint status is reported honestly;
- no dependency, script, or config change happened without approval;
- no testing workflow was introduced;
- no UI component library was introduced.

## Trigger Evals

Should trigger:

- "Run lint after this fix."
- "Check this feature with the project linter."
- "Add the linter rules I provided."
- "Set up ESLint for this React TypeScript project."

Should not trigger:

- "Plan this architecture."
- "Create a visual direction."
- "Edit README."
- "Create tests."

## Reference Map

- `AGENTS.md` - canonical policy and routing.
- `project/verification-profile.md` - local-only verification commands.
- user-provided ESLint model - preferred setup pattern when setup is explicitly requested.
