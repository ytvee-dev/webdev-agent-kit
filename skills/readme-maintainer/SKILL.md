---
name: readme-maintainer
description: Use when auditing `.agents/` documentation, agent rules, skills, summaries, sync policy, or user-facing onboarding docs, and when deciding whether `.agents/README.md` must be updated. Produces a concise, human-readable README for users with the main usage instructions and no filler.
---

# README Maintainer

## Purpose

Keep `.agents/README.md` accurate, concise, and useful for a human user who
needs to understand how to use the agent bundle.

## Required Context

Before editing `.agents/README.md`:

1. Read `.agents/AGENTS.md`.
2. Read `.agents/SUMMARY.md`.
3. Read `.agents/common/documentation-maintenance.md`.
4. Read the changed docs, rules, skills, references, and sync contracts.
5. Read `.agents/project/**` only when user-facing project behavior is affected.

## Deep Analysis Pass

- Build the current documentation model from source files, not memory.
- Identify the canonical policy path, publishable paths, local-only paths, and
  user-facing workflows.
- Check whether skill names, trigger intent, reading order, publish/sync rules,
  and root `AGENTS.md` behavior changed.
- Check whether `.agents/README.md` still answers the practical user questions:
  what this bundle is, where canonical rules live, how to use skills, what is
  local-only, how sync/publication works, and which files not to edit.
- Treat stale README guidance as documentation drift and fix it in the same
  task.

## README Writing Rules

- Write for a human user, not for an internal implementation note.
- Keep the README short, direct, and operational.
- Put the most important usage instructions near the top.
- Prefer concrete sections: purpose, how to use, what to edit, what not to
  publish, sync/publish workflow, maintenance checks.
- Do not include marketing language, history, vague explanations, or repeated
  policy text copied from other docs.
- Do not include host-project stack facts in `.agents/README.md`; keep those in
  `.agents/project/**`.
- Do not turn README into a full rulebook. Link users to `.agents/AGENTS.md`,
  `.agents/SUMMARY.md`, and specific skills for details.

## Update Decision

Update `.agents/README.md` when a documentation change affects any of these:

- canonical policy path or host-root pointer behavior
- publishable vs local-only path rules
- skill list, skill names, or skill routing
- reading order or onboarding flow
- sync-down, publish-up, PR, branch, or commit workflow
- instructions a user needs before asking an agent to work in the repo

Skip README edits only when the change is purely internal and no user-facing
instruction, workflow, path, or skill list changes.

## Final Checks

Before finishing:

1. Verify `.agents/README.md` matches `.agents/AGENTS.md`, `.agents/SUMMARY.md`,
   and changed skills.
2. Verify no `.agents/project/**` facts leaked into the publishable README.
3. Verify the README does not tell agents to mirror `.agents/AGENTS.md` into the
   host-root `AGENTS.md`.
4. Verify every referenced path exists or is intentionally described as a
   pattern.
5. Run markdown formatting validation for the changed docs.
