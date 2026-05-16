# Skill Design

Use this guide when deciding whether to create a new skill or edit an existing
one.

## Choose the right intervention

- Edit an existing skill when the workflow already exists and the change only
  tightens triggers, adds a missing rule, or updates a reference.
- Create a new skill when the task has its own trigger surface, workflow, or
  reusable constraints that would make an existing skill unfocused.
- Edit `.agents/project/*.md` instead of a reusable skill when the change is
  just a host-repo fact or local convention.
- Edit `.agents/common/*.md` instead of a reusable skill when the change is a
  generic publishable rule, anti-pattern, or approved-pattern policy rather than
  a workflow.

## Choose the degree of freedom

- Use high freedom when multiple implementations are valid and the skill mainly
  needs routing heuristics.
- Use medium freedom when a preferred pattern exists but some adaptation is
  still expected.
- Use low freedom when the workflow is fragile, repetitive, or easy to get
  wrong without explicit steps.

## Keep the package lean

- Put only the trigger, workflow, and non-obvious constraints in `SKILL.md`.
- Add `references/` when examples, checklists, or design variants would bloat
  `SKILL.md`.
- Add `agents/openai.yaml` so the skill has stable UI metadata and prompt text.
- Do not create extra docs just to explain the skill package itself.

## Reusability test

Before finalizing a skill, ask:

- Would another agent know when to load this skill from the frontmatter alone?
- Does the body tell the agent what to do without re-explaining the entire
  domain?
- Are repo-specific facts kept in overlays rather than buried in the skill?
- Does the package avoid hidden decisions for the implementing agent?
