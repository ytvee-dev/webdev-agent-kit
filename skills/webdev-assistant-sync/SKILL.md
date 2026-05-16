---
name: webdev-assistant-sync
description: Use when syncing the shared agent bundle from or to `git@github.com:ytvee-dev/webdev-assistant.git`, including `sync-down`, `publish-up` through a new branch and GitHub PR, or an explicit branch-push fallback when upstream `main` does not exist yet.
---

# Webdev Assistant Sync

## When to use

- Pull the shared bundle from `git@github.com:ytvee-dev/webdev-assistant.git`
  into the current host project
- Publish generic bundle changes from the current host project back to the
  shared upstream repository
- Push a generic bundle branch to upstream without a PR when `origin/main` does
  not exist yet and the user explicitly asks for branch-only publication
- Rebuild or verify the nested `.agents/` checkout itself
- Review whether a documentation change is publishable or must remain local-only

## Required context

Before acting:

1. Read `AGENTS.md`.
2. Read `.agents/SUMMARY.md`.
3. Read `.agents/common/documentation-maintenance.md`.
4. Read `references/path-contract.md`.
5. Read `references/git-preflight.md`.
6. Read the workflow reference for the requested mode:
   - `references/sync-down.md`
   - `references/publish-up.md`

## Core rules

- The host project repository must never be used for upstream publication git
  commands.
- The only canonical upstream checkout path is `.agents/`.
- Host-project local-only files must stay local-only:
  `.agents/project/**`, source code, and any other repo-specific documentation
  or configuration.
- Publishable checkout-root bundle content is limited to `AGENTS.md`,
  `SUMMARY.md`, `common/**`, `skills/**`, `README.md`, and `.gitignore`.
- `.agents/AGENTS.md` is the canonical publishable copy; the host repository
  root `AGENTS.md` must stay synchronized with it.
- All git commands for the upstream checkout must use
  `git -c safe.directory=<absolute-upstream-path> -C <absolute-upstream-path> ...`.
- For `publish-up`, GitHub connector access is mandatory for PR creation.
- If the GitHub connector is unavailable, request installation or connection of
  the GitHub connector before continuing the PR flow.
- `publish-up` must start with an upstream `main` refresh. If `origin/main`
  does not exist, stop and report the preflight failure instead of inventing a
  bootstrap flow.
- If `origin/main` does not exist and the user explicitly asks only for
  branch+push without a PR, use the push-only fallback described in
  `references/publish-up.md`.
- The push-only fallback must still publish only eligible checkout-root bundle
  paths and must never include `.agents/project/**` or any host-project files.

## Trigger expectations

- Load this skill for prompts such as:
  - “создай PR в webdev-assistant”
  - “опубликуй shared rules upstream”
  - “запушь generic skill changes в assistant repo”
  - “просто закомить и запушь ветку в webdev-assistant”
  - “подтяни обновления webdev-assistant в текущий проект”
- Use `sync-down` when the user wants local bundle updates from upstream.
- Use `publish-up` when the user wants to publish generic bundle changes back to
  upstream.
- Use the push-only fallback when `origin/main` is missing and the user
  explicitly accepts a branch push without PR creation.

## Reference map

- `references/path-contract.md`
- `references/git-preflight.md`
- `references/sync-down.md`
- `references/publish-up.md`
