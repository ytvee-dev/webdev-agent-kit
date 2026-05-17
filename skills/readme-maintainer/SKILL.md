---
name: readme-maintainer
description: Use when auditing `.agents/` documentation, agent rules, skills, summaries, sync policy, or user-facing onboarding docs, and when deciding whether `.agents/README.md` must be updated. Produces a structured, accurate, human-readable README that can be detailed when it is the user-facing bundle reference.
---

# README Maintainer

## Purpose

Keep `.agents/README.md` accurate, structured, and useful for a human user who
needs to understand how to use the agent bundle.

The README may be detailed when it is the user-facing reference for bundle
architecture, skills, setup, sync/publication, and operational rules. Do not
force it back to a short quickstart when the requested purpose is a full bundle
guide.

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
- Keep the README direct, technical, and operational.
- Put the most important usage instructions near the top.
- Prefer concrete sections: purpose, scope, architecture, skills, setup,
  implicit rules, prohibited actions, publishable paths, sync/publish workflow,
  and maintenance checks.
- Include enough detail for a user to understand the bundle without opening
  every skill, but do not paste full reference files or every checklist.
- Do not include marketing language, history, vague explanations, emotional
  phrasing, or uncontrolled copies of every rule.
- Do not include host-project stack facts in `.agents/README.md`; keep those in
  `.agents/project/**`.
- Keep README aligned with `.agents/AGENTS.md`, `.agents/SUMMARY.md`, and the
  actual skill folders. Link users to specific skills for deeper procedure.
- When showing `agents/openai.yaml`, use the actual bundle shape with
  `interface:` and `policy:`.

## Update Decision

Update `.agents/README.md` when a documentation change affects any of these:

- canonical policy path or host-root pointer behavior
- publishable vs local-only path rules
- skill list, skill names, or skill routing
- reading order or onboarding flow
- sync-down, publish-up, PR, branch, or commit workflow
- instructions a user needs before asking an agent to work in the repo
- VS Code/Codex setup expectations for this bundle

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
5. Verify examples match actual bundle conventions, especially
   `agents/openai.yaml`.
6. Run markdown formatting validation for the changed docs.
