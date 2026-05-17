---
id: 'agents.skills.webdev-assistant-sync.references.publish-up'
title: 'Publish Up'
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

# Publish Up

Use this flow when the user wants to publish generic bundle changes back to
`git@github.com:ytvee-dev/webdev-assistant.git`.

If `origin/main` exists, use the normal PR flow below.
If `origin/main` is missing, use the fallback only when the user explicitly asks
for branch+push without a PR.

## Naming contract

- Branch names must use `[fix|feat]-[description]`.
- `description` must be 1-3 lowercase kebab-case words that summarize the
  grouped documentation commits.
- Do not use numbers, timestamps, ticket ids, repo names, or placeholders such
  as `webdev`, `assistant`, or `bundle` in the branch name unless the word is
  the real subject of the change.
- Use `feat` for additive documentation or skill behavior and `fix` for
  corrections, clarifications, or drift repair.
- Documentation commit subjects must use
  `fix(docs): <short description>` or `feat(docs): <short description>`.
- Reuse the same core description across the branch name, commit subject, and
  PR title.
- Keep the local `.agents/` checkout on `main` by default.
- Commit publishable documentation changes locally on `main`.
- Do not create a publication branch, push, open a PR, or report publication
  success while eligible publishable documentation changes remain uncommitted.
- After the documentation commit, verify that eligible publishable paths have no
  remaining staged or unstaged changes.
- Never push local `main` directly to `origin`.
- Before creating the push branch, run `git pull --rebase origin main` while on
  local `main`.
- After pushing the branch and creating the PR, return the local checkout to
  `main`.

## Eligibility rules

Only these checkout-root paths inside `.agents/` are eligible for publication:

- `AGENTS.md`
- `SUMMARY.md`
- `common/**`
- `skills/**`
- `README.md`
- `.gitignore`

Never publish:

- `project/**`
- old helper folders such as `upstream/**`
- application source code or any other host-project file outside `.agents/`

## Steps

### Phase 1: Author On Local Main

1. Run the required checks and working tree guard from `git-preflight.md`.
2. If the checkout is not on `main`, switch to `main` only when the working tree
   is clean. If the checkout has uncommitted changes on another branch, stop and
   report the branch and changed paths.
3. Refresh local `main` before editing when the working tree is clean:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> fetch origin main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> pull --rebase origin main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> rev-list --left-right --count origin/main...main
```

4. If local `main` is already ahead of `origin/main`, inspect the ahead commits.
   Continue only when they are the current publication commits; otherwise stop
   and report the commits.
5. Confirm the repository root `AGENTS.md` is a stable pointer to
   `.agents/AGENTS.md`; do not mirror `.agents/AGENTS.md` into it.
6. Compute the eligible change set from the checkout-root publishable paths and
   apply `.agents/.gitignore` as a denylist for local-only content.
7. If nothing eligible changed, stop and report `nothing eligible`.
8. Stage only eligible publishable paths. If an optional checkout-root path such
   as `SUMMARY.md`, `README.md`, or `.gitignore` does not exist, omit that
   missing path from the `add` command instead of adding any local-only path:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> add -- AGENTS.md SUMMARY.md README.md .gitignore common skills
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> diff --cached --name-only
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> diff --cached --name-only -- project upstream
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> diff --cached --check
```

9. If staged local-only paths are listed, unstage them, stop, and report the
   paths. Never commit `project/**`, `upstream/**`, or host-project files.
10. Commit on local `main` with the shared naming contract:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> commit -m "<TAG>(docs): <short description>"
```

11. Verify that the commit captured every eligible publishable documentation
    change:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> diff --name-only -- AGENTS.md SUMMARY.md README.md .gitignore common skills
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> diff --cached --name-only -- AGENTS.md SUMMARY.md README.md .gitignore common skills
```

If either command lists a path, stop. Commit the missing eligible change or
report the exact blocker. Do not create a branch, push, open a PR, or report
publication success while eligible publishable documentation remains
uncommitted.

### Phase 2: Publish Through A PR Branch

12. Rebase the local publication commit on the latest `origin/main`:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> fetch origin main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> pull --rebase origin main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> rev-list --left-right --count origin/main...main
```

13. If local `main` is not ahead of `origin/main` after the publication commit,
    stop and report `nothing to publish`.
14. If local `main` has ahead commits that are not part of the current
    publication, stop and report them instead of creating a mixed PR.
15. Re-run the eligible publishable path check from step 11. If any eligible
    path is listed, stop and commit it on local `main` before continuing.
16. Confirm the branch name does not already exist locally or remotely. If it
    exists, choose a new `[fix|feat]-[description]` before continuing.
17. Create the branch from local `main`:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout -b <TAG>-<DESCRIPTION>
```

18. Push the branch to `origin`.
19. Create the PR through the GitHub connector with base `main` and title
    `<TAG>(docs): <short description>`.

20. If the connector is missing, request it and stop instead of faking a PR URL
    or switching to `gh`.
21. Return the local checkout to `main`:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout main
```

## Push-only fallback

Use this fallback only when:

- `origin/main` is missing
- the user explicitly accepts branch publication without PR creation

### Steps

1. Run the preflight from `git-preflight.md`.
2. If local `main` exists, keep the working checkout on local `main`.
3. If local `main` does not exist or the repo has no commits, create the
   fallback branch as an orphan before staging files:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout --orphan <TAG>-<DESCRIPTION>
```

4. Confirm the repository root `AGENTS.md` is a stable pointer to
   `.agents/AGENTS.md`; do not mirror `.agents/AGENTS.md` into it.
5. Compute the eligible change set from the checkout-root publishable paths and
   apply `.agents/.gitignore` as a denylist for local-only content.
6. If nothing eligible changed, stop and report `nothing eligible`.
7. Stage only eligible publishable paths with the same staging commands from
   Phase 1, and keep `project/**` and other local-only paths out of the staged
   change set.
8. Commit with the shared naming contract:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> commit -m "<TAG>(docs): <short description>"
```

9. Run the eligible publishable path check from the normal flow. If any
   eligible path remains staged or unstaged, stop and commit it before pushing.
10. Create the branch from local `main` when local `main` exists:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout -b <TAG>-<DESCRIPTION>
```

11. Push the branch to `origin`.
12. Return the local checkout to `main` when that branch exists locally.
13. Report the pushed branch name explicitly and state that no PR was created
    because `origin/main` does not exist yet.

## Required outcome

- Publication uses only the nested `.agents/` git repository.
- The push branch always starts from local `main` after rebasing with
  `git pull --rebase origin main`.
- Branch creation, push, PR creation, and publication success reporting are
  blocked until every eligible publishable documentation change is committed.
- Skipped local-only paths are reported explicitly when they exist.
- In fallback mode, the branch is pushed without PR creation and the missing
  `origin/main` constraint is reported explicitly.
- After publication work completes, the local checkout returns to `main`.
