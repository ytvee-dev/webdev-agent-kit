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
- Keep `.agents/AGENTS.md` as the canonical publishable policy copy.
- Keep the repository root `AGENTS.md` as a stable pointer to
  `.agents/AGENTS.md`, not as a synchronized mirror.
- Do not put host-project stack facts, file paths, architecture, or examples
  into `.agents/common/**` or reusable skill packages.

## Change rules

- Identify every directly and indirectly affected file before editing.
- Update cross-links after adding, renaming, deleting, or materially changing
  files.
- If a common doc changes, check related skills and `AGENTS.md`.
- If a skill changes, check `.agents/SUMMARY.md`, routing docs, and relevant
  common docs.
- If a documentation change affects user-facing workflow, skill lists, path
  policy, or sync/publication instructions, update `.agents/README.md` in the
  same task.
- If a new approved pattern or anti-pattern is added, decide whether it belongs
  in `.agents/common/**` or only in `.agents/project/**`.
- If a task reveals documentation drift, fix it in the same task instead of
  leaving the mismatch behind.
- Never publish `.agents/project/**`, old helper folders such as `upstream/**`,
  or any file outside the nested `.agents/` repo surface
  to the shared `webdev-assistant` repository.
- Do not mirror `.agents/AGENTS.md` into the host-root `AGENTS.md`; update the
  root pointer only when the canonical policy path changes.

## Git naming rules

- When a documentation task in `.agents/` includes branch or commit work, use
  branch names in the form `[fix|feat]-[description]`.
- Keep `description` to 1-3 lowercase kebab-case words that summarize the
  grouped documentation commits.
- Do not use numbers, timestamps, ticket ids, repo names, or placeholders such
  as `webdev`, `assistant`, or `bundle` in documentation branch names unless
  the word is the real subject of the change.
- Use `feat` for additive documentation or skill behavior and `fix` for
  corrections, clarifications, or drift repair.
- For documentation commits, use `fix(docs): <short description>` or
  `feat(docs): <short description>`.
- Keep the local `.agents/` checkout on `main` by default; treat feature
  branches as push/PR transport only.
- Commit publishable documentation changes locally on `main`.
- Do not create a publication branch, push, open a PR, or report publication
  success while eligible publishable documentation changes remain uncommitted.
- After committing publishable documentation, verify that eligible publishable
  paths have no remaining staged or unstaged changes before continuing.
- Do not switch `.agents/` branches while uncommitted or unmerged changes are
  present; resolve, commit, or stop and report the exact paths first.
- Stage and commit only eligible publishable paths before creating a push
  branch.
- Never push local `main` directly to `origin`.
- Before pushing a documentation branch, run `git pull --rebase origin main`
  while on local `main`.
- After that pull, create the new `[fix|feat]-[description]` branch from local
  `main`, push it, open the PR to `main`, and then return the local checkout to
  `main`.
- Reuse the same core description across the branch name, commit subject, and
  PR title when the task creates a PR.

## Scope checklist

- Check whether `AGENTS.md` must change.
- Check whether `.agents/SUMMARY.md` must change.
- Check whether `.agents/README.md` must change.
- Check whether `.agents/common/**` must change.
- Check whether `.agents/project/**` local addenda must change.
- Check whether `.agents/skills/**` or skill-routing references must change.
- Check whether `.agents/.gitignore` must change.
