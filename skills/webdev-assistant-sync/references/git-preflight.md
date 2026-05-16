# Git Preflight

Run this preflight before `sync-down` or `publish-up`.

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

## PR preflight

Before `publish-up`:

1. Confirm that the GitHub connector is available.
2. If unavailable, request installation or connection of the GitHub connector
   and stop until it is available.
3. Refresh `main` before branching:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> fetch origin main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout -B main origin/main
```

## Push-only fallback preflight

Use this path only when both conditions are true:

1. `origin/main` is missing.
2. The user explicitly wants a branch push without PR creation.

Then:

1. Skip GitHub connector checks because no PR will be created.
2. Reuse the same eligibility filters as `publish-up`.
3. If the checkout already has commits, create the fallback branch from the
   current checkout state.
4. If the checkout has no commits yet, create an orphan branch for the fallback
   publication.
