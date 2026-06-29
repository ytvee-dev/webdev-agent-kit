# Lint Policy Note

Status: draft.

Code-changing tasks must run the smallest relevant existing lint command before completion. If no lint command exists, the agent must say that lint was not run and explain why.

Applies to code fixes, features, refactors, implementation slices, and approved new-project code creation.

Does not apply to planning-only, design-only, documentation-only, README-only, or analysis-only tasks.

User-requested lint setup is allowed only after the agent inspects the existing package manager, framework, TypeScript usage, React usage, formatter or linter config, workspace layout, and package scripts.

The agent must not change dependencies, scripts, or config files without explicit user approval.
