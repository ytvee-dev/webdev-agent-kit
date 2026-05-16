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

1. Run the preflight from `git-preflight.md`.
2. Refresh upstream `main` before doing anything else:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> fetch origin main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout -B main origin/main
```

3. If the repository root `AGENTS.md` differs from `.agents/AGENTS.md`, mirror
   `.agents/AGENTS.md` into the repository root before finishing the task.
4. Compute the eligible change set from the checkout-root publishable paths and
   apply `.agents/.gitignore` as a denylist for local-only content.
5. If nothing eligible changed, stop and report `nothing eligible`.
6. Keep `project/**` and other local-only paths out of the staged change set.
7. Create the branch from refreshed `main`:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout -b <TAG>-<DESCRIPTION>
```

8. Commit with:

```text
<TAG>(docs): <short description>
```

9. Push the branch to `origin`.
10. Create the PR through the GitHub connector with:
   - base: `main`
   - title: `<TAG>(docs): <short description>`
11. If the connector is missing, request it and stop instead of faking a PR URL
    or switching to `gh`.

## Push-only fallback

Use this fallback only when:

- `origin/main` is missing
- the user explicitly accepts branch publication without PR creation

### Steps

1. Run the preflight from `git-preflight.md`.
2. If the repository root `AGENTS.md` differs from `.agents/AGENTS.md`, mirror
   `.agents/AGENTS.md` into the repository root before finishing the task.
3. Compute the eligible change set from the checkout-root publishable paths and
   apply `.agents/.gitignore` as a denylist for local-only content.
4. If nothing eligible changed, stop and report `nothing eligible`.
5. Keep `project/**` and other local-only paths out of the staged change set.
6. Create the branch:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout -b <TAG>-<DESCRIPTION>
```

7. If branch creation from the current checkout fails because the repo has no
   commits yet, create an orphan branch instead:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout --orphan <TAG>-<DESCRIPTION>
```

8. Commit with:

```text
<TAG>(docs): <short description>
```

9. Push the branch to `origin`.
10. Report the pushed branch name explicitly and state that no PR was created
    because `origin/main` does not exist yet.

## Required outcome

- Publication uses only the nested `.agents/` git repository.
- The branch always starts from refreshed upstream `main`.
- Skipped local-only paths are reported explicitly when they exist.
- In fallback mode, the branch is pushed without PR creation and the missing
  `origin/main` constraint is reported explicitly.
