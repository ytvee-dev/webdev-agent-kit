# Documentation Maintenance

Purpose: define bundle-wide rules for changing `AGENTS.md`, `.agents/common/**`,
`.agents/skills/**`, and the upstream-sync contract without leaking host-project
facts into publishable documentation.

## Required reading

Before changing bundle documentation:

1. Read `.agents/SUMMARY.md`.
2. Read `.agents/skills/agent-rules-skill-author/SKILL.md`.
3. Read the affected `.agents/common/**`, `.agents/skills/**`, and
   `.agents/project/**` files.

## Layer rules

- Keep bundle-wide reusable rules in `.agents/common/**`.
- Keep host-repo facts, local examples, and project-specific addenda in
  `.agents/project/**`.
- Keep reusable workflows in `.agents/skills/**`.
- Keep the nested bundle git checkout rooted at `.agents/`.
- Keep `.agents/AGENTS.md` as the canonical publishable policy copy and keep
  the repository root `AGENTS.md` synchronized with it.
- Do not put host-project stack facts, file paths, architecture, or examples
  into `.agents/common/**` or reusable skill packages.

## Change rules

- Identify every directly and indirectly affected file before editing.
- Update cross-links after adding, renaming, deleting, or materially changing
  files.
- If a common doc changes, check related skills and `AGENTS.md`.
- If a skill changes, check `.agents/SUMMARY.md`, routing docs, and relevant
  common docs.
- If a new approved pattern or anti-pattern is added, decide whether it belongs
  in `.agents/common/**` or only in `.agents/project/**`.
- If a task reveals documentation drift, fix it in the same task instead of
  leaving the mismatch behind.
- Never publish `.agents/project/**`, old helper folders such as `upstream/**`,
  or any file outside the nested `.agents/` repo surface
  to the shared `webdev-assistant` repository.

## Scope checklist

- Check whether `AGENTS.md` must change.
- Check whether `.agents/SUMMARY.md` must change.
- Check whether `.agents/common/**` must change.
- Check whether `.agents/project/**` local addenda must change.
- Check whether `.agents/skills/**` or skill-routing references must change.
- Check whether `.agents/README.md` or `.agents/.gitignore` must change.
