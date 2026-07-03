---
id: 'agents.skills.agent-rules-skill-author.references.codex-native-skill-contract'
title: 'Codex Native Skill Contract'
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
    - '[[skills/agent-rules-skill-author/references/trigger-and-metadata|Trigger And Metadata]]'
    - '[[skills/agent-rules-skill-author/references/validation-checklist|Validation Checklist]]'
    - '[[skills/agent-rules-skill-author/references/source-backed-prompting|Source-Backed Prompting]]'
depends_on:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
---

# Codex Native Skill Contract

Use this guide when a skill authoring decision depends on what Codex natively
understands versus what this `.agents` bundle adds locally.

## Section Map

- `Source hierarchy` for which authority wins when docs disagree.
- `Native Codex contract` for the strict OpenAI-portable shape.
- `Repo-local .agents extension` for the extra metadata this bundle adds.
- `Plugin packaging` for the native plugin entrypoint versus internal inventory.
- `agents/openai.yaml` and `Local toolkit contract` for UI metadata and local
  helper scripts.

## Source hierarchy

Treat these as the source of truth in this order:

1. OpenAI Codex Skills docs: https://developers.openai.com/codex/skills
2. OpenAI AGENTS docs: https://developers.openai.com/codex/guides/agents-md
3. OpenAI system skills in `codex-skills/skills/.system/`, especially
   `skill-creator`, `openai-docs`, and `skill-installer`
4. This bundle's `.agents` conventions and graph metadata

## Native Codex contract

For skill triggering and discovery, the native contract is:

- Codex discovers repo-local skills under `.agents/skills/`.
- Every skill needs a `SKILL.md`.
- `SKILL.md` must expose `name` and `description` in YAML frontmatter.
- `name` should be lowercase hyphen-case, use letters, digits, and hyphens
  only, and stay within 64 characters.
- `description` is the primary trigger surface and should stay within 1024
  characters.
- `description` should explain both what the skill does and when to use it,
  because the body is loaded after the skill is selected.

The OpenAI system `skill-creator` validator also allows these native
frontmatter keys:

- `metadata`
- `license`
- `allowed-tools`

`metadata.short-description` appears in OpenAI system skills as a UI helper
pattern. Treat it as an official local pattern, not as the only valid UI path
or as a trigger field.

## Repo-local `.agents` extension

This bundle extends the native contract with graph metadata:

- Keep `name` and `description` first.
- Append `.agents` navigation fields such as `id`, `title`, `doc_type`,
  `layer`, `status`, `publishable`, `local_only`, `skill`, `tags`, `parent`,
  `related`, and `depends_on`.
- Treat these extra fields as local navigation metadata. They do not replace the
  native trigger contract.

Do not write rules that imply Codex needs the graph metadata to discover when a
skill should trigger.

Because of that extension, `.agents`-compatible skills are not automatically
strict native-portable skills. An official native validator such as the system
`quick_validate.py` accepts only the native frontmatter keys.

## Plugin packaging

Keep the two packaging contracts separate:

- `.codex-plugin/plugin.json` is the native Codex plugin manifest. Its
  `skills` field points to `./skills/` and it belongs in the Codex target.
- `bundle-manifest.json` is this repository's internal inventory for source
  synchronization and validation. It is not a Codex or Claude platform
  manifest.

Do not copy `.codex-plugin/` into the Claude target. Do not rename the internal
inventory to `plugin.json` or treat it as a native manifest.

## `agents/openai.yaml`

`agents/openai.yaml` is recommended native skill metadata and should be treated
as the UI and harness contract, not the trigger contract.

Common fields:

- `interface.display_name`
- `interface.short_description`
- `interface.default_prompt`
- `interface.icon_small`
- `interface.icon_large`
- `interface.brand_color`
- `policy.allow_implicit_invocation`
- `dependencies.tools`

Rules to preserve:

- Quote string values when generating YAML.
- Keep `short_description` concise and within 25-64 characters.
- If `default_prompt` is present, make it short and include `$skill-name`.
- Use `dependencies.tools` when the skill depends on MCP servers or other
  explicit tool contracts. Keep these dependencies factual and narrow.

## Local toolkit contract

Inside this bundle, prefer the local helper scripts when creating or validating
skills:

- `skills/agent-rules-skill-author/scripts/init_agent_skill.py` for scaffolding a new `.agents` skill package
- `skills/agent-rules-skill-author/scripts/generate_openai_yaml.py` for UI metadata generation or regeneration
- `skills/agent-rules-skill-author/scripts/validate_agent_skill.py` for native and `.agents`-specific checks

These helpers exist to encode the OpenAI-native contract without losing this
bundle's graph metadata and local publishing rules.

Treat them as `.agents`-first helpers, not as generic portable OpenAI skill
scaffolders.
