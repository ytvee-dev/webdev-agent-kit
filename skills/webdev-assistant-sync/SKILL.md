---
name: webdev-assistant-sync
description: Use when syncing the shared agent bundle from or to `git@github.com:ytvee-dev/webdev-assistant.git`, including `sync-down`, `publish-up` through a new branch and GitHub PR, or an explicit branch-push fallback when upstream `main` does not exist yet.
id: 'agents.skills.webdev-assistant-sync.skill'
title: 'Webdev Assistant Sync'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'webdev-assistant-sync'
tags:
    - 'agents/skill-package'
    - 'agents/sync'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/webdev-assistant-sync/references/git-preflight|Git Preflight]]'
    - '[[skills/webdev-assistant-sync/references/path-contract|Path Contract]]'
    - '[[skills/webdev-assistant-sync/references/publish-up|Publish Up]]'
    - '[[skills/webdev-assistant-sync/references/sync-down|Sync Down]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
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
- Publishable Markdown files must keep graph frontmatter valid before commit or
  publication. Local-only `.agents/project/**` and `.agents/.obsidian/**` must
  never be staged.
- `.agents/AGENTS.md` is the canonical publishable policy file; the host
  repository root `AGENTS.md` is a stable pointer to it, not a synchronized
  copy.
- For documentation publication, use branch names in the form
  `[fix|feat]-[description]`.
- Keep `description` to 1-3 lowercase kebab-case words that summarize the
  grouped documentation commits.
- Do not use numbers, timestamps, ticket ids, repo names, or placeholders such
  as `webdev`, `assistant`, or `bundle` in publication branch names unless the
  word is the real subject of the change.
- Use `fix(docs): <short description>` or `feat(docs): <short description>` for
  documentation commits and reuse the same core description in the branch name
  and PR title.
- Keep the local `.agents/` checkout on `main` by default; treat feature
  branches as push/PR transport only.
- Commit publishable documentation changes locally on `main`.
- Do not create a publication branch, push, open a PR, or report publication
  success while eligible publishable documentation changes remain uncommitted.
- After committing publishable documentation, verify that eligible publishable
  paths have no remaining staged or unstaged changes before continuing.
- Before committing or publishing Markdown changes, verify every staged
  publishable Markdown file starts with frontmatter and keeps `SKILL.md`
  `name`/`description` first.
- Do not switch `.agents/` branches while uncommitted or unmerged changes are
  present; resolve, commit, or stop and report the exact paths first.
- Stage and commit only eligible publishable paths before creating a push
  branch.
- Do not mirror `.agents/AGENTS.md` into the host-root `AGENTS.md`; update the
  root pointer only when the canonical policy path changes.
- Never push local `main` directly to `origin`.
- Before pushing a publication branch, run `git pull --rebase origin main`
  while on local `main`.
- After that pull, create the new `[fix|feat]-[description]` branch from local
  `main`, push it, create the PR to `main`, and then return the local checkout
  to `main`.
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
