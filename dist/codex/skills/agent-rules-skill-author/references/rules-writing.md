---
id: 'agents.skills.agent-rules-skill-author.references.rules-writing'
title: 'Rules Writing'
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

# Rules Writing

Use this guide when drafting or tightening agent rules.

## Decide the rule type first

- Use repo-wide policy in `AGENTS.md` for precedence, required reading order,
  global prohibitions, and skill discovery.
- Use `.agents/common/*.md` for generic reusable bundle rules, approved
  patterns, anti-patterns, and bundle-maintenance policy that may be published
  upstream.
- Use `.agents/project/*.md` for facts about this repository, such as stack,
  architecture, styling, verification, or local anti-patterns.
- Use `.agents/skills/*` for reusable workflows that another agent should load
  and follow.

## Write enforceable rules

- Prefer `must`, `must not`, `only when`, and `unless explicitly requested`
  when the rule is binding.
- State the target object of the rule directly: file, folder, task type,
  workflow, or boundary.
- Name the exception in the same sentence when one exists.
- Avoid layered duplicates that say the same thing with different wording.

## Keep scope explicit

- Say whether the rule applies to repo-wide policy, overlays, or skills.
- Say whether the rule is manual-only or safe for implicit invocation.
- Say what the rule does not cover when that boundary prevents misuse.

## Conflict handling

- Read existing rules before writing new ones.
- If two rules overlap, keep the stronger and clearer rule and remove or tighten
  the weaker one.
- If repo-wide policy and skill guidance differ, align the skill to the repo
  policy unless the user explicitly wants the repo policy changed.

## Useful rule templates

- `Do not modify <target> unless the user explicitly asks for it.`
- `Use <location> for <purpose>; do not put <content> in <other-location>.`
- `Only use <tool or pattern> when <condition>.`
- `Run <check> after <change-type>.`
- `Keep <artifact> focused on <scope>, not <excluded-scope>.`
