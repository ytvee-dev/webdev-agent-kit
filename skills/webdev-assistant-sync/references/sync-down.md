# Sync Down

Use this flow when the user wants local bundle updates from upstream.

## Steps

1. Run the preflight from `git-preflight.md`.
2. Refresh the nested `.agents/` checkout:

```powershell
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> fetch origin main
git -c safe.directory=<ABS_UPSTREAM> -C <ABS_UPSTREAM> checkout -B main origin/main
```

3. Treat the refreshed checkout-root publishable paths as the source of truth:
   - `AGENTS.md`
   - `SUMMARY.md`
   - `common/**`
   - `skills/**`
   - `README.md`
   - `.gitignore`
4. Let git update tracked checkout-root files directly inside `.agents/`.
5. Leave ignored local-only paths such as `project/**` untouched.
6. Mirror `.agents/AGENTS.md` into the host repository root `AGENTS.md` if the
   contents differ.
7. Re-run markdown validation after the sync.

## Required outcome

- The nested `.agents/` repo receives upstream-managed bundle changes directly.
- Host-project overlays in `.agents/project/**` remain untouched.
- The repository root `AGENTS.md` stays synchronized with `.agents/AGENTS.md`.
