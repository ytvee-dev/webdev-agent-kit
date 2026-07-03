---
id: 'agents.skills.agent-rules-skill-author.references.trigger-and-metadata'
title: 'Trigger And Metadata'
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

# Trigger And Metadata

Use this guide when writing skill frontmatter and `agents/openai.yaml`.

## Section Map

- `Native versus local metadata` and `Frontmatter` for trigger contract shape.
- `Trigger writing` and `Trigger evals` for matching quality.
- `UI metadata` and `Metadata sync checklist` for `agents/openai.yaml` and
  invocation policy.

## Native versus local metadata

- Native Codex trigger metadata is `name` plus `description`.
- This bundle adds graph metadata after those native fields.
- Keep `name` and `description` first so the native contract stays obvious.
- Do not describe `.agents` graph fields as if Codex required them for
  triggering. They are local navigation metadata.

## Frontmatter

- Keep native trigger information in `name` and `description`.
- Use lowercase hyphen-case for `name`.
- Write `description` as the primary trigger surface: what the skill does and
  when to use it.
- Make `description` cover the capability, the trigger conditions, and the
  important `when not` boundary when overlap risk is real.
- Mention concrete task shapes in the description, not only broad topics.
- Keep `description` non-empty and under 1024 characters.
- Front-load the most important trigger words because long skill lists may
  shorten descriptions before matching.
- Keep descriptions dense and informative. Codex includes skill descriptions in
  the initial skills list budget, so marketing phrasing wastes scarce context.
- If the skill is `.agents`-specific, say so in the trigger wording or the
  body instead of implying generic portability.
- For `.agents` skills, append graph metadata after `name` and `description`
  instead of replacing the native contract.
- `metadata.short-description` is an official system-skill pattern for UI help,
  not a trigger field. Use it only when it adds value.

## Trigger writing

- Include both verbs and artifacts: `create`, `edit`, `refresh`, `rules`,
  `skills`, `AGENTS.md`, `.agents/project`, `.agents/skills`.
- Mention the target boundary when it matters, such as `inside .agents/`.
- Avoid vague triggers that could accidentally match unrelated app work.
- Describe user intent instead of internal implementation. Say when the user
  needs the workflow, not only what files the skill contains.
- Include near-miss exclusions when keywords overlap with unrelated work.
- Avoid keyword stuffing and overly pushy descriptions that try to win every
  adjacent prompt.

## Trigger evals

Before finalizing trigger wording for a new or broadened skill:

- Write realistic should-trigger prompts that vary phrasing, explicitness,
  detail, and complexity.
- Write near-miss should-not-trigger prompts that share keywords but require a
  different workflow.
- Make should-trigger prompts substantive enough that Codex would benefit from
  consulting a skill instead of handling the request as a trivial one-step task.
- Confirm explicit invocation still works through `$skill-name`.
- Confirm implicit invocation is appropriate before keeping
  `allow_implicit_invocation: true`.

## UI metadata

- Keep `display_name` human-readable and close to the skill title.
- Keep `short_description` compact and specific.
- Keep `short_description` within 25-64 characters.
- Write `default_prompt` as a direct invocation sentence using `$skill-name`.
- Keep `allow_implicit_invocation` aligned with prompt-driven skill selection.
  If a skill should run from user intent, set it to `true` and avoid manual-only
  language in `SKILL.md`.
- Treat `icon_small`, `icon_large`, and `brand_color` as optional UI fields.
- Use `dependencies.tools` when the skill depends on MCP servers or another
  explicit tool contract. Keep dependency metadata factual and narrow.
- Prefer `skills/agent-rules-skill-author/scripts/generate_openai_yaml.py` when regenerating `.agents`
  `openai.yaml` files so quoting, length checks, and preserved policy fields
  stay consistent.

## Metadata sync checklist

- If the package is `.agents`-compatible, make that scope visible enough that a
  reader will not mistake it for a strict native-portable skill.
- `description` and `default_prompt` should point at the same workflow.
- `short_description` should not promise more than the skill actually covers.
- If the skill becomes broader or narrower, update both `SKILL.md` and
  `agents/openai.yaml` in the same change.
- When trigger wording changes, refresh the trigger eval examples in the same
  pass so the boundary stays testable.
- If `dependencies.tools` is present, keep it aligned with the real MCP or
  connector dependency instead of speculative future tooling.
