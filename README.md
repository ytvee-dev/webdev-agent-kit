# webdev-assistant

Reusable agent rules and skills for React, Next.js, TypeScript, CSS Modules,
and agent-documentation workflows.

## Start Here

- The canonical policy is `.agents/AGENTS.md`.
- The host-root `AGENTS.md` is only a stable pointer to `.agents/AGENTS.md`.
- Do not mirror `.agents/AGENTS.md` into the host-root `AGENTS.md`.
- Use `.agents/SUMMARY.md` to find the right skill, common rule, or project
  overlay.

## What Lives Here

- `AGENTS.md` - canonical bundle policy for agents.
- `SUMMARY.md` - map of docs, skills, overlays, and reading order.
- `common/**` - reusable rules that can be published upstream.
- `skills/**` - reusable workflows agents should load for matching tasks.
- `project/**` - local host-project facts. This directory is ignored and must
  not be published upstream.
- `.gitignore` - keeps local-only overlay files out of upstream publication.

## How To Use

1. Read the host-root `AGENTS.md`.
2. Follow its pointer to `.agents/AGENTS.md`.
3. Use `.agents/SUMMARY.md` to choose the relevant skill.
4. Read only the common docs, project overlays, and source files needed for the
   task.
5. For implementation work, finish with `frontend-review-and-fix`.
6. For documentation changes, check whether this README must be updated.

## Key Skills

- `webapp-task-protocol` - classify React or Next.js work and choose the skill
  chain.
- `nextjs-app-router` - App Router routes, layouts, metadata, and boundaries.
- `react-component-workflow` - components, hooks, props, state, and UI behavior.
- `redux-state-workflow` - Redux, selectors, typed hooks, and shared client
  state.
- `frontend-typescript-rules` - strict TypeScript and safe refactors.
- `boundary-input-validation` - boundary parsing without new dependencies.
- `frontend-review-and-fix` - review pass and verification.
- `agent-rules-skill-author` - maintain agent policy, common docs, overlays,
  and skill packages.
- `readme-maintainer` - keep this README accurate, concise, and user-facing.
- `webdev-assistant-sync` - sync or publish the shared bundle through the
  nested `.agents` repository.

See `.agents/SUMMARY.md` for the full skill list.

## Local-Only Project Context

Keep host-project facts in `.agents/project/**`.

Examples:

- framework and dependency facts
- route and component path indexes
- styling conventions
- local verification commands
- project-specific approved patterns and anti-patterns

Do not move these facts into `AGENTS.md`, `common/**`, `skills/**`, or this
README unless they are generic and reusable.

## Sync From Upstream

Use `webdev-assistant-sync` in sync-down mode.

Rules:

- Run git commands only inside `.agents`.
- Keep `project/**` untouched.
- Keep the host-root `AGENTS.md` as a stable pointer.
- Re-run markdown validation after sync.

## Publish Upstream

Use `webdev-assistant-sync` in publish-up mode.

Rules:

- Publish only `AGENTS.md`, `SUMMARY.md`, `common/**`, `skills/**`,
  `README.md`, and `.gitignore` from inside `.agents`.
- Never publish `project/**`, `upstream/**`, application source, tests, configs,
  or host-project files.
- Keep local work on `.agents` `main`.
- Commit publishable documentation changes locally on `main`.
- Never push local `main` directly.
- Create a short-lived `[fix|feat]-[description]` branch only for push and PR.
- Open the PR to `main` through the GitHub connector.
- Return the local `.agents` checkout to `main`.

Commit and PR naming:

- branch: `[fix|feat]-[description]`
- commit: `fix(docs): <short description>` or
  `feat(docs): <short description>`
- PR title: same tag and core description as the commit

## README Maintenance

After any `.agents` documentation change, use `readme-maintainer` or apply the
same check manually:

- Does a user-facing workflow, path, skill list, or policy pointer change?
- Would a user know how to use the bundle from this README?
- Is anything stale, duplicated, or too detailed?

If the answer requires user-visible guidance, update this README in the same
task.
