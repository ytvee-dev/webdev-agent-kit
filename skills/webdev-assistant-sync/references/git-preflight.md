---
id: 'agents.skills.webdev-assistant-sync.references.git-preflight'
title: 'Git Preflight'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'webdev-assistant-sync'
tags:
    - 'agents/skill-package'
    - 'agents/sync'
    - 'agents/reference'
parent:
    - '[[skills/webdev-assistant-sync/SKILL|Webdev Assistant Sync]]'
related:
    []
depends_on:
    - '[[skills/webdev-assistant-sync/SKILL|Webdev Assistant Sync]]'
---

# Git Preflight

Run this preflight before `sync-down` or `publish-up`.

## Section Map

- `Required checks` for upstream checkout, remote, and `origin/main`.
- `Working Tree Guard` before checkout, pull, rebase, branch, stash, or restore.
- `PR preflight` before the normal `publish-up` flow.
- `Push-only fallback preflight` when the user explicitly requested no PR.

## Required checks

1. Confirm that `.agents/.git` exists.
2. Resolve the absolute upstream checkout path and reuse it for every git
   command.
3. Confirm the upstream remote:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> remote -v
```

4. Confirm that upstream `main` exists:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> ls-remote --heads origin main
```

5. If step 4 returns no `main`, stop and report that `origin/main` is missing
   unless the user explicitly asked for the push-only fallback with no PR.
6. Never write to global git config for `safe.directory`; always pass it inline
   with `-c safe.directory=...`.
7. Never run upstream publication commands from the host project repository.

## Working Tree Guard

Run this guard before any checkout, pull, rebase, branch creation, stash, or
restore command:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> status --short --branch
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> diff --name-only --diff-filter=U
```

- If unmerged paths are listed, stop and report the paths.
- If the checkout is on a non-`main` branch and has uncommitted changes, do not
  switch branches. Stop and report the current branch and changed paths.
- If the checkout is on `main` and has uncommitted publishable changes, finish
  the authoring phase in `publish-up.md` before running publication commands.
- If the checkout is on `main` and has uncommitted local-only changes such as
  `project/**`, stop and report those paths. Do not stage, stash, or publish
  them.

## PR preflight

Before `publish-up`:

1. Confirm that the GitHub connector is available.
2. If unavailable, request installation or connection of the GitHub connector
   and stop until it is available.
3. Run the working tree guard above.
4. Return the local checkout to `main` only when the working tree is clean.
5. Refresh local `main` before branching:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> fetch origin main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> pull --rebase origin main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> rev-list --left-right --count origin/main...main
```

- If local `main` is ahead of `origin/main` before the current publication
  commit exists, stop and inspect the ahead commits:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> log origin/main..main --oneline
```

- If local `main` is ahead because the current publication commit already
  exists, continue and create the push branch from that local `main`.
- If `origin/main` is ahead after `pull --rebase`, stop and report the rebase
  failure or retry the pull only after resolving the cause.

## Push-only fallback preflight

Use this path only when both conditions are true:

1. `origin/main` is missing.
2. The user explicitly wants a branch push without PR creation.

Then:

1. Skip GitHub connector checks because no PR will be created.
2. Reuse the same eligibility filters as `publish-up`.
3. Run the working tree guard above.
4. Return the local checkout to `main` only when that branch exists and the
   working tree is clean.
5. If local `main` exists, create the fallback branch from local `main`.
6. If the checkout has no commits or no local `main`, create an orphan branch
   for the fallback publication.
