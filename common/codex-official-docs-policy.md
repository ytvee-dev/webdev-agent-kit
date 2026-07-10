---
id: 'agents.common.codex-official-docs-policy'
title: 'OpenAI And Codex Official Docs Policy'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/policy'
    - 'codex'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules Skill Author]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
    - '[[common/documentation-maintenance|Documentation Maintenance]]'
depends_on: []
---

# OpenAI And Codex Official Docs Policy

Purpose: keep OpenAI and Codex-specific rules source-backed without duplicating official links across every skill.

## Official Sources

Use these official OpenAI sources as the source of truth when changing Codex behavior, distribution, skill authoring, MCP setup, permissions, or local configuration rules:

- Codex Best Practices: https://developers.openai.com/codex/learn/best-practices
- Codex Quickstart: https://developers.openai.com/codex/quickstart
- Codex CLI: https://developers.openai.com/codex/cli
- AGENTS.md guide: https://developers.openai.com/codex/guides/agents-md
- Config Basics: https://developers.openai.com/codex/config-basic
- Sandbox: https://developers.openai.com/codex/concepts/sandboxing
- MCP for Codex: https://developers.openai.com/codex/mcp
- Agent Skills: https://developers.openai.com/codex/skills
- OpenAI Developer Docs MCP: https://developers.openai.com/learn/docs-mcp
- OpenAI Developer Docs MCP server: https://developers.openai.com/mcp
- OpenAI Developers Videos: https://developers.openai.com/learn/videos

## When To Read Which Source

- Read Codex Best Practices when changing task context, prompting, validation, MCP, skills, or automation habits.
- Read the AGENTS.md guide when changing root or bundle instruction discovery, fallback file names, durable guidance, or instruction layering.
- Read Agent Skills when changing skill directory shape, `SKILL.md` metadata, trigger descriptions, `agents/openai.yaml`, plugin packaging, or skill distribution.
- Read Config Basics when changing `.codex/config.toml`, project config guidance, profile behavior, model defaults, approval policy, sandbox settings, or MCP configuration locations.
- Read Sandbox when changing rules about autonomous command execution, approval flow, network access, filesystem boundaries, or safety gates.
- Read MCP for Codex when changing MCP server guidance, official install source checks, MCP transport assumptions, OAuth, tool instructions, or `project/mcp-profile.md` behavior.
- Read OpenAI Developer Docs MCP when changing its provider mapping, supported documentation scope, client setup, or fallback behavior.
- Read Codex CLI or Quickstart when changing installation, first-run, CLI usage, IDE usage, or onboarding instructions.
- Use OpenAI Developers Videos only as supplementary learning material. Do not treat video titles as binding runtime policy unless the same rule is backed by docs.

## Retrieval Route And Budget

Activate `openai_platform_docs` only when current OpenAI API, ChatGPT Apps SDK, Codex, model, tool, MCP, skill, plugin, sandbox, or configuration behavior can change the answer or implementation.

1. If the current session exposes the official OpenAI Developer Docs MCP, use one targeted search and read only the decisive page sections.
2. Otherwise use the declared official OpenAI web docs fallback.
3. If neither route is available, state the affected unknown or confidence limit instead of relying on memory.

The Docs MCP is read-only and documentation-only. It cannot call the OpenAI API, inspect account state, or prove live API behavior. Do not invoke it for generic frontend work, stable local facts, or questions already answered by verified repository evidence. Summarize only decision-relevant facts; do not dump retrieved pages into context or output.

## Bundle Rules

- Keep official OpenAI links centralized here or in the owning skill-author reference. Do not paste the full link list into every skill.
- A skill may point to this policy when it depends on current Codex-native behavior.
- For OpenAI, Codex, ChatGPT, Apps SDK, MCP, model, or tool behavior, follow the `openai_platform_docs` route instead of relying on memory.
- Keep host-project facts about installed tools, missing MCP servers, available docs sources, and accepted fallbacks in `project/mcp-profile.md`, not in reusable bundle docs.
- Do not use unofficial blog posts, search summaries, generated guesses, or random package names as authority for Codex setup, MCP installation, permissions, or skill packaging.

## Safety Rules From Official Docs

- Treat `AGENTS.md` as durable guidance that Codex reads before work; keep repository-level instructions small enough to stay inside discovery limits.
- Treat skills as progressive-disclosure workflows: frontmatter names and descriptions are the trigger surface; detailed instructions and references are loaded only after selection.
- Treat `.codex/config.toml` as configuration, not runtime policy text. Do not create or change it without explicit user approval.
- Treat sandbox and approval policy as separate controls: sandbox defines technical boundaries, and approval policy defines when Codex must ask before crossing them.
- Treat MCP configuration as explicit tool setup. Verify official install sources and ask for approval before installing servers or changing configuration.

## Maintenance Checklist

When Codex-native behavior changes in this bundle:

1. Check the relevant official source above.
2. Update the smallest owning file: `AGENTS.md`, a `common/**` rule, a skill reference, or `agents/openai.yaml`.
3. Avoid duplicating official URLs across unrelated skills.
4. Update `project/mcp-profile.md` only for host-project tool facts.
5. Report which official source was checked and which validation was run.
