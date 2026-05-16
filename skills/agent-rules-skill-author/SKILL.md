---
name: agent-rules-skill-author
description: Use when creating or editing repo-local agent rules, AGENTS.md policy, .agents/common bundle docs, .agents/project overlay docs, or .agents/skills packages. Keep generic publishable policy in AGENTS.md and .agents/common, keep factual host-repo overlays inside .agents/project, and keep reusable workflows inside .agents/skills.
---

# Agent Rules And Skill Author

## Purpose

Create or revise repo-local agent rules and skill packages without leaking
project-specific instructions into the wrong layer.

## Required context order

Before editing:

1. Read `AGENTS.md`.
2. Read `.agents/SUMMARY.md`.
3. Read `.agents/common/documentation-maintenance.md`.
4. Read the relevant `.agents/common/*.md` docs and `.agents/project/*.md`
   overlays for the target change.
5. Read the relevant framework-specific path indexes when the change touches
   repo navigation guidance.
6. Read neighboring skills in `.agents/skills/` when changing an existing skill
   chain or adding a new one.
7. Read the target file or target skill package before writing anything.

## Change classification

Choose the target layer before editing:

- Edit `AGENTS.md` for repo-wide policy, precedence, and the skill map.
- Edit `.agents/common/*.md` for generic publishable bundle docs and rules.
- Edit `.agents/project/*.md` for factual repo overlays tied to this codebase.
- Edit `.agents/skills/*` for reusable workflows another agent should follow.

If a rule is repo-specific, keep it out of `AGENTS.md`, `.agents/common`, and
reusable skills unless the user explicitly wants the reusable bundle to encode
that policy.

## Core rules

- Create and edit skill packages and overlay docs strictly inside `.agents/`.
- Edit the repository root `AGENTS.md` only for repo-wide policy, precedence,
  discovery, or skill-map changes.
- Keep the repository root `README.md` untouched unless the user explicitly asks
  for it.
- Prefer MCP tools, current repo documentation, and targeted lookup indexes
  before broad repo scanning.
- Do not invent missing requirements, architecture, or implementation details;
  search narrowly and then ask the user.
- Keep instructions strict, testable, and free of vague qualifiers such as
  `usually`, `maybe`, `try`, or `ideally` when the rule is meant to be binding.
- Resolve precedence conflicts explicitly instead of stacking duplicate or
  contradictory rules.
- Keep `AGENTS.md` focused on repo-wide policy and discovery, not detailed
  procedural guidance better suited to a skill or overlay doc.
- Keep `.agents/common/*.md` generic and publishable; never leak host-project
  facts, examples, or local stack details into them.
- Keep `.agents/project/*.md` factual and repo-specific; do not turn overlay
  docs into generic reusable playbooks.
- Keep `.agents/skills/*` reusable and procedural; do not hardcode incidental
  repo facts that belong in overlays.
- When a task includes committing or branching `.agents/` documentation, follow
  the git naming contract in `.agents/common/documentation-maintenance.md`.
- Keep `.agents/` as the nested shared-bundle repo and keep
  `.agents/project/**` local-only inside it.
- Keep `.agents/AGENTS.md` synchronized with the repository root `AGENTS.md`.
- If `.agents/` structure changes, update `.agents/SUMMARY.md` in the same task.
- If a new skill changes how tasks should be routed, update the relevant
  path-index or skill-routing docs in the same task.
- If a new approved pattern or anti-pattern is added, inspect the related
  overlays and skills for missing references.
- Keep `SKILL.md` lean. Move detailed checklists, examples, and design notes
  into `references/`.
- Write instructions in imperative form with short rule blocks and checklists.
- Prefer one explicit rule over several overlapping softer rules.
- Keep skill selection prompt-driven. The user should not need to name a skill
  explicitly for the agent to choose it.

## Packaging rules

- Create a dedicated skill package when the workflow is reusable and larger than
  a simple overlay tweak.
- Keep skill folders limited to `SKILL.md`, `agents/openai.yaml`, and only the
  resource directories that are actually needed.
- Do not add auxiliary files such as `README.md`, `CHANGELOG.md`,
  `QUICK_REFERENCE.md`, or similar documentation inside the skill package.
- Keep references at most one level away from `SKILL.md`.
- Keep `agents/openai.yaml` synchronized with the current `SKILL.md` trigger
  and intent.
- Put "when to use" logic in frontmatter `description`; use the body for
  workflow and constraints.

## Validation workflow

1. Re-read the edited files as if another agent will rely on them with no extra
   context.
2. Check that the target layer is correct: repo-wide policy, overlay fact, or
   reusable skill.
3. Check that the trigger surface, prohibitions, and exceptions are explicit.
4. Check that new references are linked from `SKILL.md` and actually exist.
5. Check that `.agents/SUMMARY.md` reflects any new or renamed files.
6. Check that every changed file is either inside `.agents/` or is the
   repository root `AGENTS.md`.
7. Search `.agents` for removed skill names, stale paths, and outdated
   references after editing or deleting agent docs.
8. Run the repo validation step appropriate for markdown and skills changes.

## Reference map

- `references/rules-writing.md`
- `references/skill-design.md`
- `references/trigger-and-metadata.md`
- `references/validation-checklist.md`
- `references/source-backed-prompting.md`
- `references/documentation-maintenance.md`
