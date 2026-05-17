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
- For external products or APIs, verify current behavior from official docs or
  configured docs MCP tools before encoding instructions.
- Define the reusable workflow the skill adds. Do not create a skill for advice
  the agent can already apply reliably without extra context.
- Capture the decision points an implementing agent must not guess: audience,
  inputs, outputs, defaults, compatibility boundaries, and verification.

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
- Do not create extra docs just to explain the skill package itself.

## Reusability test

Before finalizing a skill, ask:

- Would another agent know when to load this skill from the frontmatter alone?
- Does the body tell the agent what to do without re-explaining the entire
  domain?
- Are repo-specific facts kept in overlays rather than buried in the skill?
- Does the package avoid hidden decisions for the implementing agent?
- Does the skill name realistic should-trigger and should-not-trigger prompts?
- Does the workflow include a validation path proportional to the task risk?
