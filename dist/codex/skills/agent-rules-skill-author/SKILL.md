---
name: agent-rules-skill-author
description: Use when creating, evaluating, or editing this .agents screenshot-to-frontend skill bundle, repo-local agent rules, AGENTS.md, common/**, project/**, or skills/**. Focus on precise skill authoring, trigger boundaries, source-backed instructions, progressive disclosure, validation, and layer-correct docs.
---

# Agent Rules And Skill Author

## Purpose

Create or revise repo-local agent rules and `.agents`-compatible skill
packages without leaking project-specific instructions into the wrong layer.

## When To Use

- The user asks to create, evaluate, rename, delete, or edit skills.
- The user asks to change `AGENTS.md`, `SUMMARY.md`, `README.md`, `common/**`,
  `project/**`, or `skills/**`.
- The screenshot-to-frontend pipeline rules, tool contracts, or skill routing
  need maintenance.

## When Not To Use

- The user asks to write a design implementation spec from screenshots. Use
  `design-screenshot-spec`.
- The user asks to implement a frontend layout from a spec. Use
  `frontend-layout-implementer`.
- The user asks to visually verify rendered UI. Use `frontend-visual-qa`.
- The user asks to adapt a new project in Plan Mode. Use
  `project-onboarding-adapter`.

## Required Context

1. Read `AGENTS.md`.
2. Confirm the classified task is `skill-documentation-refactor`,
   `documentation`, or another `.agents` rule-maintenance task.
3. Read `common/documentation-maintenance.md`.
4. Read affected `common/**`, `skills/**`, `project/**`, and root pointer files
   for the requested change.
5. Consult `SUMMARY.md` only when the task explicitly edits, audits, or
   verifies the manual catalog.
6. Read relevant references from this skill only when their topic is in scope.
7. Read current OpenAI Codex docs when native skill behavior, `AGENTS.md`,
   MCP, plugins, or `agents/openai.yaml` behavior may have changed.

## Tool Contract

- Use filesystem reads and targeted search for local bundle facts.
- Use official OpenAI Codex docs for current skill and MCP behavior.
- Use `context7` and `mdn` only when authoring rules depend on current
  framework or web platform behavior.
- Do not use Figma MCP for this bundle.

## Workflow

1. Classify the target layer: `AGENTS.md`, `SUMMARY.md`, `README.md`,
   `common/**`, `project/**`, or `skills/**`.
2. Confirm whether a new skill is needed or an existing skill/reference/common
   rule should be edited.
3. Define trigger surface, non-trigger cases, inputs, outputs, defaults, tool
   contract, failure modes, and validation gates.
4. Keep skill packages in the standard section order used by this bundle.
5. Keep graph frontmatter and `agents/openai.yaml` synchronized.
6. Remove stale links after renames or deletions.
7. Validate changed skill packages and run documentation checks.

## Output Contract

Report:

- files changed;
- skill routing or trigger changes;
- tool dependency changes;
- validation performed;
- unresolved risks or blocked checks.

## Validation Gates

- `name` and `description` stay first in `SKILL.md` frontmatter.
- Every skill has `Purpose`, `When To Use`, `When Not To Use`,
  `Required Context`, `Tool Contract`, `Workflow`, `Output Contract`,
  `Validation Gates`, `Trigger Evals`, and `Reference Map`.
- New references are linked from the owning `SKILL.md`.
- `agents/openai.yaml` matches skill trigger, scope, and factual tool
  dependencies.
- No Figma MCP or Figma whiteboard workflow is introduced.

## Trigger Evals

Should trigger:

- "Create a new skill for visual QA."
- "Audit and rewrite the .agents skill routing."
- "Update AGENTS.md and SUMMARY.md for renamed skills."

Should not trigger:

- "Implement this Design Implementation Spec."
- "Compare the rendered page to the screenshot."
- "Write a layout spec from these screenshots."

## Authoring modes

Default to `.agents`-compatible skill authoring:

- Use the native Codex trigger contract plus this bundle's graph metadata.
- Use the local toolkit and publishable bundle conventions.
- Treat this as the authoritative mode unless the user explicitly asks for a
  portable OpenAI skill outside this bundle.

Use strict native-portable OpenAI skill authoring only when the user explicitly
asks for portability outside `.agents/` or compatibility with the official
native validator:

- Keep `SKILL.md` frontmatter limited to the native OpenAI keys.
- Do not present `.agents` graph metadata as part of the portable package
  contract.
- Keep bundle-specific navigation and publication metadata out of the portable
  `SKILL.md`.

## Required context order

Before editing:

1. Read `AGENTS.md`.
2. Read `.agents/common/documentation-maintenance.md`.
3. Read the relevant `.agents/common/*.md` docs and `.agents/project/*.md`
   overlays for the target change.
4. Consult `.agents/SUMMARY.md` only when the task explicitly edits, audits, or
   verifies the manual catalog.
5. Read the relevant framework-specific path indexes when the change touches
   repo navigation guidance.
6. Read neighboring skills in `.agents/skills/` when changing an existing skill
   chain or adding a new one.
7. Read the target file or target skill package before writing anything.
8. Read `references/codex-native-skill-contract.md` when native Codex behavior,
   `agents/openai.yaml`, or skill scaffolding details affect the change.

## Change classification

Choose the target layer before editing:

- Edit `AGENTS.md` for repo-wide policy, precedence, and the skill map.
- Edit `.agents/common/*.md` for generic publishable bundle docs and rules.
- Edit `.agents/project/*.md` for factual repo overlays tied to this codebase.
- Edit `.agents/skills/*` for reusable workflows another agent should follow.

If a rule is repo-specific, keep it out of `AGENTS.md`, `.agents/common`, and
reusable skills unless the user explicitly wants the reusable bundle to encode
that policy.

## Skill authoring quality pass

Before creating or materially changing a skill package:

1. Define concrete user intents the skill must handle, including at least one
   realistic should-trigger prompt and one near-miss should-not-trigger prompt
   when the trigger boundary is not obvious.
2. Decide the correct intervention: edit an existing skill, create a new skill,
   update `.agents/common`, or update `.agents/project`. Do not create a new
   skill when a focused reference or trigger fix is enough.
3. Decide the compatibility target before drafting.
   - Default to `.agents`-compatible authoring. Switch to strict native-portable
     authoring only when the user explicitly asks for an OpenAI-native portable
     skill.
4. Ground the workflow in source material: existing repo docs, real task
   traces, official product docs, schemas, APIs, or user-provided examples.
   Avoid generic best-practice prose that does not change agent behavior.
5. Calibrate specificity to risk. Use flexible guidance for judgment-heavy
   work, explicit ordered steps for fragile workflows, and scripts only when
   repeatability or deterministic validation is worth the extra package weight.
6. Specify the inputs, outputs, defaults, failure modes, and validation gates an
   implementing agent needs. For ambiguous requirements, ask the user instead
   of hiding a decision inside the skill.
7. Keep `SKILL.md` focused on trigger, workflow, defaults, and gotchas. Move
   detailed examples, rubrics, and optional variants into linked
   `references/`.
8. Add graph frontmatter to every new Markdown file when the target is
   `.agents`-compatible. In `.agents` `SKILL.md`, keep
   `name` and `description` first, then add `id`, `title`, `doc_type`,
   `layer`, `status`, `publishable`, `local_only`, `skill`, `tags`, `parent`,
   `related`, and `depends_on`.
9. Link each new reference or asset back to the owning `SKILL.md`, and update
   the owning skill's `related` links. If the skill changes routing, update
   graph links in `SUMMARY.md`, `README.md`, and neighboring skills.
10. Run a cold-read check: another agent with only the frontmatter and the
   linked files must know when to use the skill, what to do, when to stop, and
   how to verify the result.
11. For new `.agents` skills, prefer the local helper scripts when they fit the
    task: `scripts/init_agent_skill.py`, `scripts/generate_openai_yaml.py`, and
    `scripts/validate_agent_skill.py`.

Read `references/skill-quality-rubric.md` when creating a new skill, making a
skill broader, changing trigger behavior, or improving a skill that produced
imprecise or inconsistent results.

Read references selectively instead of bulk-loading the whole package:

- `references/codex-native-skill-contract.md` when native portability,
  frontmatter shape, `agents/openai.yaml`, or validator expectations matter.
- `references/rules-writing.md` when drafting or tightening policy wording,
  scope, or precedence.
- `references/skill-design.md` when deciding whether to create a new skill,
  split variants, or choose the package shape.
- `references/skill-quality-rubric.md` when testing trigger precision,
  workflow quality, or anti-overfitting revisions.
- `references/trigger-and-metadata.md` when editing `name`, `description`,
  `agents/openai.yaml`, implicit invocation, or dependency metadata.
- `references/validation-checklist.md` before finalizing a material skill or
  policy change.
- `references/figma-derived-conventions.md` when the bundle needs to encode
  reusable routing or policy learned from Figma workflows.
- `references/source-backed-prompting.md` when current OpenAI docs, system
  skills, or external source hierarchy affect the instructions.
- `references/documentation-maintenance.md` when the change affects
  `.agents/README.md`, `.agents/SUMMARY.md`, graph links, or bundle structure.

## Skill Creation Loop

Use this loop when the task is to create a new skill or materially improve an
existing one:

1. Decide whether a new skill is justified at all.
   - Prefer editing an existing skill, a reference, `.agents/common`, or
     `.agents/project` when the workflow already exists.
2. Extract the workflow before drafting.
   - Mine the current conversation, repo docs, task traces, user corrections,
     and known failure cases before asking the user to restate the workflow.
3. Lock the reusable contract and compatibility target.
   - Record the trigger surface, expected inputs, output shape, defaults, stop
     conditions, important constraints the implementing agent must not guess,
     and whether the package is `.agents`-compatible or strict native-portable.
4. Plan the package shape.
   - Decide whether the skill should be workflow-based, task-based,
     reference-based, or capabilities-based, and choose the resource set before
     writing files.
5. Initialize new skills with the local toolkit.
   - For a new `.agents` skill, use `scripts/init_agent_skill.py` after the
     package shape is clear. For an existing skill, skip initialization and
     inspect the current package instead.
6. Write the first draft.
   - Keep `SKILL.md` focused on trigger, workflow, defaults, gotchas, and
     validation; push long examples and variants into `references/`.
7. Run a trigger eval pass.
   - Write realistic should-trigger and near-miss should-not-trigger prompts to
     test the `description` and `agents/openai.yaml` metadata.
8. Run a workflow eval pass.
   - Use 2-3 realistic user prompts to check whether the skill improves actual
     behavior, not only the text of the package.
9. Inspect traces and outputs before tightening rules.
   - Read the agent's steps, not only the final answer. If the skill wastes
     effort or follows irrelevant branches, fix the general cause before adding
     narrower rules.
10. Revise for reusable behavior.
   - Keep changes general enough to help future prompts. Do not overfit the
     skill to one eval prompt or one user phrasing.
11. Sync package metadata.
   - Keep `SKILL.md`, `agents/openai.yaml`, references, and any eval examples
     aligned whenever trigger wording, portability target, or scope changes.
12. Run script-backed validation.
    - Run `python scripts/validate_agent_skill.py <skill-dir>` before finalizing
      a new or materially changed skill package.
13. Run the cold-read final gate.
    - Another agent should be able to load the package, understand the trigger
      boundary, and follow the workflow without hidden context or Claude-only
      tooling.

## Improvement Heuristics

- Extract an existing workflow from conversation history or repo context before
  inventing a new one from scratch.
- When eval feedback reveals a failure, prefer durable, reusable corrections to
  one-off prompt patches.
- If several test prompts repeatedly force the agent to perform the same
  deterministic helper work, consider `scripts/` or `assets/`.
- Keep the package instruction-only when the repeated helper work is not stable
  enough to justify more artifacts.
- Treat `name` and `description` as the native Codex trigger contract, then
  layer `.agents` graph metadata after them.
- State the portability target clearly. Do not present a `.agents`-specific
  package as if it were a strict portable OpenAI skill.

## Core rules

- Create and edit skill packages and overlay docs strictly inside `.agents/`.
- Edit the repository root `AGENTS.md` only for repo-wide policy, precedence,
  discovery, or skill-map changes.
- Keep the repository root `README.md` untouched unless the user explicitly asks
  for it.
- Prefer MCP tools, current repo documentation, and targeted lookup indexes
  before broad repo scanning.
- For skill structure, frontmatter, and `agents/openai.yaml`, prefer official
  OpenAI docs and the local `codex-skills/skills/.system/` patterns over
  third-party guidance.
- Default to `.agents`-compatible skill authoring. Switch to strict
  native-portable authoring only when the user explicitly asks for it.
- Prefer filesystem MCP tools for reading file contents and directory structure
  when they are available. Use shell commands for search, git state, diffs,
  formatting, or executable validation output.
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
- When a task includes `.agents/` documentation gitflow, keep local work on
  `main`, commit only eligible publishable paths, create a new branch only for
  push/PR, and return the local checkout to `main` afterward.
- Keep `.agents/` as the nested shared-bundle repo and keep
  `.agents/project/**` local-only inside it.
- Keep `.agents/AGENTS.md` as canonical policy and keep the repository root
  `AGENTS.md` as a stable pointer, not a synchronized mirror.
- If `.agents/` structure changes, update `.agents/SUMMARY.md` in the same task.
- If documentation changes affect user-facing workflow, skill lists, or path
  policy, update `README.md` in the same task.
- If a new skill changes how tasks should be routed, update the relevant
  path-index or skill-routing docs in the same task.
- If a new approved pattern or anti-pattern is added, inspect the related
  overlays and skills for missing references.
- Keep `SKILL.md` lean. Move detailed checklists, examples, and design notes
  into `references/`.
- Keep graph frontmatter current on every Markdown file in `.agents/**`. For
  `SKILL.md`, preserve Codex-critical `name` and `description` as the first
  frontmatter fields before `id`, `title`, `doc_type`, links, and tags.
- If the target is strict native portability, keep `SKILL.md` frontmatter to
  the official native keys only and keep `.agents` navigation metadata outside
  the portable package.
- Treat graph frontmatter as navigation metadata. Do not put binding workflow
  steps, hidden policy, or long operational instructions into frontmatter; put
  them in the document body.
- Write instructions in imperative form with short rule blocks and checklists.
- Prefer one explicit rule over several overlapping softer rules.
- Keep skill selection prompt-driven. The user should not need to name a skill
  explicitly for the agent to choose it.

## Packaging rules

- Create a dedicated skill package when the workflow is reusable and larger than
  a simple overlay tweak.
- Keep skill folders limited to `SKILL.md`, `agents/openai.yaml`, and only the
  resource directories that are actually needed.
- For new `.agents` skills, prefer `scripts/init_agent_skill.py` over manual
  folder creation unless the scaffolder would clearly get in the way.
- Do not add auxiliary files such as `README.md`, `CHANGELOG.md`,
  `QUICK_REFERENCE.md`, or similar documentation inside the skill package.
- Keep references at most one level away from `SKILL.md`.
- For reference files longer than 100 lines, add a table of contents or another
  clear section map near the top.
- Keep `agents/openai.yaml` synchronized with the current `SKILL.md` trigger
  and intent. Use `scripts/generate_openai_yaml.py` when the local helper can
  regenerate the file without losing required fields.
- Put "when to use" logic in native frontmatter `description`; use the body for
  workflow and constraints.
- Add graph metadata to new Markdown files, link references/assets back to the
  owning `SKILL.md`, and use `.agents`-relative Obsidian wikilinks in
  `parent`, `related`, and `depends_on`.
- Update graph links when skill names, reference files, assets, routing,
  ownership, publishable/local-only status, or related workflows change.

## Validation workflow

1. Re-read the edited files as if another agent will rely on them with no extra
   context.
2. Check that the target layer is correct: repo-wide policy, overlay fact, or
   reusable skill.
3. Check that the portability target is explicit: `.agents`-compatible or
   strict native-portable.
4. Check that the trigger surface, prohibitions, and exceptions are explicit.
5. Check that new references are linked from `SKILL.md`, say when to read
   them, and actually exist.
6. For skill changes, check the quality pass: concrete intents, source-backed
   workflow, right resource split, and validation gates.
7. Check that `.agents/SUMMARY.md` reflects any new or renamed files.
8. Check that every changed file is either inside `.agents/` or is the
   repository root `AGENTS.md`.
9. Search `.agents` for removed skill names, stale paths, and outdated
   references after editing or deleting agent docs.
10. Check graph frontmatter coverage and link validity for changed Markdown
   files.
11. Run `python scripts/validate_agent_skill.py <skill-dir>` when a skill
    package was created or materially changed.
12. Run the repo validation step appropriate for markdown and skills changes.

## Reference map

- `references/codex-native-skill-contract.md`
- `references/rules-writing.md`
- `references/skill-design.md`
- `references/skill-quality-rubric.md`
- `references/trigger-and-metadata.md`
- `references/validation-checklist.md`
- `references/figma-derived-conventions.md`
- `references/source-backed-prompting.md`
- `references/documentation-maintenance.md`
