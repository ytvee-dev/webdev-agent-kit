# Validation Checklist

Use this checklist before and after editing repo-local agent rules or skills.

## Before saving

- Trigger surface is explicit and narrow enough to avoid unrelated invocations.
- No conflict exists with current `AGENTS.md` policy.
- Documentation file contents and directory structure were inspected through
  filesystem MCP when available, with shell reserved for search, git state,
  diffs, formatting, or executable validation.
- The target layer is correct: `AGENTS.md`, `.agents/common`, `.agents/project`, or
  `.agents/skills`.
- `SKILL.md` stays procedural and compact.
- Every referenced file exists and is linked from `SKILL.md`.
- No changed files exist outside `.agents/` except the repository root
  `AGENTS.md` when repo-wide policy, skill discovery, or upstream bundle
  maintenance changed.
- Any `.agents/` documentation branch or commit examples follow the
  `[fix|feat]-[description]` and `fix(docs): ...` / `feat(docs): ...` contract.
- Any `.agents/` documentation gitflow examples keep local work on `main`,
  commit only eligible publishable paths, branch only for push/PR, and return
  the local checkout to `main`.
- Publication workflows include a commit gate: no branch, push, PR, or success
  report may happen while eligible publishable documentation changes remain
  uncommitted.
- Branch switching examples include a dirty-tree and unmerged path guard.
- Removed skill names, stale paths, and outdated references were searched across
  `.agents`.
- `.agents/README.md` was updated or explicitly checked when documentation
  changes affected user-facing workflow, skill lists, path policy, or
  sync/publication instructions.
- No auxiliary docs such as `README.md` or `CHANGELOG.md` were added to the
  skill package.
- `agents/openai.yaml` matches the skill trigger and intent.

## After saving

- Re-read the package as if another agent will use it cold.
- Check that prohibitions, exceptions, and precedence are explicit.
- Check that the workflow leaves no hidden implementation decisions.
- Check that repo-specific facts remain in overlays rather than reusable skill
  text.
- Run `npx prettier --check .` for markdown and skill-only changes.
