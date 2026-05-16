# Sync Down

Use this flow when the user wants local bundle updates from upstream.

## Steps

1. Run the preflight from `git-preflight.md`.
2. Run the working tree guard from `git-preflight.md`.
3. If publishable paths have uncommitted changes, stop and report them instead
   of pulling over local edits.
4. If only local-only paths such as `project/**` have uncommitted changes, keep
   them untouched and continue only when checkout and pull can run without
   touching those paths.
5. Refresh the nested `.agents/` checkout:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> fetch origin main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> pull --rebase origin main
```

6. Treat the refreshed checkout-root publishable paths as the source of truth:
    - `AGENTS.md`
    - `SUMMARY.md`
    - `common/**`
    - `skills/**`
    - `README.md`
    - `.gitignore`
7. Let git update tracked checkout-root files directly inside `.agents/`.
8. Leave ignored local-only paths such as `project/**` untouched.
9. Keep the host repository root `AGENTS.md` as a stable pointer to
   `.agents/AGENTS.md`; do not mirror `.agents/AGENTS.md` into it.
10. Re-run markdown validation after the sync.

## Required outcome

- The nested `.agents/` repo receives upstream-managed bundle changes directly.
- Host-project overlays in `.agents/project/**` remain untouched.
- The repository root `AGENTS.md` remains a stable pointer to
  `.agents/AGENTS.md`.
- The local checkout stays on `main` after the sync.
