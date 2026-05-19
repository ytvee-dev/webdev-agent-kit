---
id: 'agents.skills.agent-rules-skill-author.references.skill-design'
title: 'Skill Design'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'agent-rules-skill-author'
tags:
    - 'agents/skill-package'
    - 'agents/authoring'
    - 'agents/reference'
parent:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
related:
    []
depends_on:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
---

# Skill Design

Use this guide when deciding whether to create a new skill or edit an existing
one.

## Section Map

- `Choose the right intervention` for deciding between an existing skill, a new
  skill, `.agents/common`, or `.agents/project`.
- `Ground the design` and `Capture intent before drafting` for source gathering
  and contract capture.
- `Choose the validation style`, `Choose the structure on purpose`, and
  `Choose the degree of freedom` for package shape.
- `Keep the package lean`, `Reusability test`, and `Organize variants
  deliberately` for progressive disclosure and final packaging choices.

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

## Ground the design

- Start from concrete task examples, user corrections, real failure modes,
  existing docs, schemas, APIs, or review feedback.
- State whether the target is `.agents`-compatible or strict native-portable
  before you encode structural rules that depend on frontmatter or bundle
  layout.
- For external products or APIs, verify current behavior from official docs or
  configured docs MCP tools before encoding instructions.
- Define the reusable workflow the skill adds. Do not create a skill for advice
  the agent can already apply reliably without extra context.
- Capture the decision points an implementing agent must not guess: audience,
  inputs, outputs, defaults, compatibility boundaries, and verification.

## Capture intent before drafting

Before writing or widening a skill, lock the core contract:

- What capability should the skill enable?
- When should it trigger, and when should it stay out of the way?
- What output shape or report structure matters to the user?
- Which inputs, constraints, file types, or environment assumptions are
  required?
- Is the workflow objectively checkable, or is it mainly judgment-heavy?

Extract as much of this as possible from the current conversation, task
examples, user corrections, repo docs, and failure cases before asking the user
for more detail. Ask only about gaps that materially change the workflow or the
trigger boundary.

## Choose the validation style

- Objective workflows need concrete workflow test prompts and observable checks
  that confirm the skill changed behavior, not just wording.
- Judgment-heavy workflows need explicit human review criteria; do not invent
  fake assertions that imply precision the workflow does not actually have.
- Use trigger evals to validate `description`, then use 2-3 realistic workflow
  prompts to validate the draft itself.

## Choose the structure on purpose

Prefer one of these shapes before writing the package:

- Workflow-based: best when the skill is a sequence of decisions or ordered
  steps.
- Task-based: best when the skill is a toolbox of distinct operations.
- Reference or guidelines-based: best when the skill encodes standards,
  policies, or specifications another agent must follow.
- Capabilities-based: best when the skill combines several related features
  behind one trigger surface.

If a skill mixes patterns, keep the dominant pattern visible in `SKILL.md` and
move variant-heavy detail into `references/`.

## Choose the degree of freedom

- Use high freedom when multiple implementations are valid and the skill mainly
  needs routing heuristics.
- Use medium freedom when a preferred pattern exists but some adaptation is
  still expected.
- Use low freedom when the workflow is fragile, repetitive, or easy to get
  wrong without explicit steps.
- Mix degrees of freedom inside one skill when needed: keep judgment-heavy
  review guidance flexible, but make stateful commands, publication flows, and
  validators exact.

## Keep the package lean

- Put only the trigger, workflow, and non-obvious constraints in `SKILL.md`.
- Add `references/` when examples, checklists, or design variants would bloat
  `SKILL.md`.
- Add `agents/openai.yaml` so the skill has stable UI metadata and prompt text.
- If the target is strict native portability, keep `.agents` navigation
  metadata out of the portable `SKILL.md`.
- Keep the `SKILL.md` body under roughly 500 lines when practical. Split before
  it turns into a reference dump.
- For reference files longer than 100 lines, add a table of contents or another
  clear section map near the top.
- Do not create extra docs just to explain the skill package itself.

## Reusability test

Before finalizing a skill, ask:

- Would another agent know when to load this skill from the frontmatter alone?
- Does the package clearly say whether it is `.agents`-compatible or strict
  native-portable?
- Does the body tell the agent what to do without re-explaining the entire
  domain?
- Are repo-specific facts kept in overlays rather than buried in the skill?
- Does the package avoid hidden decisions for the implementing agent?
- Does the skill name realistic should-trigger and should-not-trigger prompts?
- Does the workflow include a validation path proportional to the task risk?

## Organize variants deliberately

If one skill supports several frameworks, domains, or operating modes:

- Keep `SKILL.md` as the router and shared workflow contract.
- Point to the specific reference file for each variant instead of telling the
  agent to read every reference.
- Split only when the trigger surface stays shared and the execution details
  truly differ by domain.
