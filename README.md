# webdev-assistant

Shared upstream repository for the reusable `AGENTS.md` + `.agents/` bundle.

## Purpose

This nested repository stores only generic agent-bundle documentation and
reusable skill workflows that can be embedded into many different host
projects.

Host-project facts must stay local and must not be published here.

## Publishable scope

This repository is expected to contain:

- `AGENTS.md`
- `SUMMARY.md`
- `common/**`
- `skills/**`
- this `README.md`
- `.gitignore`

## Never publish

Do not publish any host-project-only content here, including:

- `project/**`
- old helper folders such as `upstream/**`
- application source code
- application tests
- application configs
- host repository root `README.md`
- any local project examples or stack facts

## Local workflow

The canonical local checkout path is:

```text
.agents/
```

All upstream git commands must run only inside that checkout and must always
use:

```text
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> ...
```

Do not run publication git commands from the host project repository root.

## Root AGENTS Mirror

- `AGENTS.md` inside this nested repo is the canonical publishable policy file.
- `../AGENTS.md` in the host project root is a synchronized mirror of this file.
- Bundle sync must keep those two files aligned.

## Sync Down

Use the `webdev-assistant-sync` skill in `sync-down` mode to:

1. refresh the upstream checkout from `origin/main`
2. update tracked publishable files directly inside `.agents/`
3. mirror `.agents/AGENTS.md` to the host project root `AGENTS.md`
4. leave `project/**` and other local-only files untouched

## Publish Up

Use the `webdev-assistant-sync` skill in `publish-up` mode to:

1. refresh upstream `main`
2. compute the eligible bundle change set from this nested checkout
3. keep `project/**` and other local-only files out of the staged change set
4. create a new branch from refreshed `main`
5. commit and push
6. open a PR to `main` through the GitHub connector

If `origin/main` does not exist yet and the user explicitly asks only for a
branch push, use the push-only fallback:

1. compute the same eligible bundle change set
2. create a branch in the form `[fix|feat]-[description]`
3. commit and push the branch
4. report that no PR was created because `main` does not exist yet

### Required naming

- branch: `[fix|feat]-[description]`
- branch `description`: 1-3 lowercase kebab-case words that summarize the
  grouped documentation commits
- commit: `fix(docs): <short description>` or `feat(docs): <short description>`
- PR title: reuse the same tag and core description as the commit subject
- PR base: `main`
- do not use numbers, timestamps, ticket ids, repo names, or placeholders such
  as `webdev`, `assistant`, or `bundle` in branch names unless the word is the
  real subject of the change

### Required preflight

- `origin/main` must exist
- GitHub connector must be available for PR creation
- if `origin/main` is missing, stop and report the preflight failure instead of
  inventing a bootstrap flow

### Explicit fallback exception

- if `origin/main` is missing and the user explicitly requests branch-only
  publication without a PR, the skill may create and push a fallback branch
  instead of stopping

## Maintenance rule

Whenever bundle structure, cross-links, or skill routing changes, update:

- `AGENTS.md`
- `SUMMARY.md`
- relevant `common/**`
- relevant `skills/**`
- this `README.md` when the upstream management contract changed
