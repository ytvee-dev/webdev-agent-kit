# Path Contract

## Canonical paths

- Host project root: the repository where the agent is currently working
- Nested upstream checkout root: `.agents/`
- Canonical publishable AGENTS copy: `.agents/AGENTS.md`
- Host-root mirror: `AGENTS.md`
- Local host-project overlays: `.agents/project/**`
- Publishable bundle docs: `.agents/common/**`
- Publishable reusable workflows: `.agents/skills/**`

## Publishable checkout-root paths

- `AGENTS.md`
- `SUMMARY.md`
- `common/**`
- `skills/**`
- `README.md`
- `.gitignore`

## Local-only paths

- `project/**`
- old helper folders such as `upstream/**`
- any application source code, tests, configs, build outputs, and any other
  host-project files outside the nested `.agents/` repo surface

## Mirror rule

- `.agents/AGENTS.md` is the canonical publishable policy file
- host-root `AGENTS.md` is the synchronized mirror used by the embedded bundle
- `README.md` and `.gitignore` live only at `.agents/` checkout root and are
  not mirrored into the host repository root
