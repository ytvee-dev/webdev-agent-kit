# Validation Checklist

Use this checklist before and after editing repo-local agent rules or skills.

## Before saving

- Trigger surface is explicit and narrow enough to avoid unrelated invocations.
- No conflict exists with current `AGENTS.md` policy.
- The target layer is correct: `AGENTS.md`, `.agents/common`, `.agents/project`, or
  `.agents/skills`.
- `SKILL.md` stays procedural and compact.
- Every referenced file exists and is linked from `SKILL.md`.
- No changed files exist outside `.agents/` except the repository root
  `AGENTS.md` when repo-wide policy, skill discovery, or upstream bundle
  maintenance changed.
- Removed skill names, stale paths, and outdated references were searched across
  `.agents`.
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
