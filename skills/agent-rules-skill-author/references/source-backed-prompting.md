---
id: 'agents.skills.agent-rules-skill-author.references.source-backed-prompting'
title: 'Source-Backed Prompting'
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
    - '[[common/codex-official-docs-policy|Codex Official Docs Policy]]'
depends_on:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
---

# Source-Backed Prompting

Use official sources when shaping agent rules, skill triggers, or workflow instructions.

## Primary OpenAI Codex Sources

- Codex Official Docs Policy: `common/codex-official-docs-policy.md`
- Codex Best Practices: https://developers.openai.com/codex/learn/best-practices
- Codex Quickstart: https://developers.openai.com/codex/quickstart
- Codex CLI: https://developers.openai.com/codex/cli
- AGENTS.md guide: https://developers.openai.com/codex/guides/agents-md
- Config Basics: https://developers.openai.com/codex/config-basic
- Sandbox: https://developers.openai.com/codex/concepts/sandboxing
- MCP for Codex: https://developers.openai.com/codex/mcp
- Agent Skills: https://developers.openai.com/codex/skills
- OpenAI Developers Videos: https://developers.openai.com/learn/videos

## Secondary Sources

Use Agent Skills Specification material only as secondary context after OpenAI-native sources are exhausted.

- Agent Skills Specification: https://agentskills.io/specification
- Agent Skills Best Practices: https://agentskills.io/skill-creation/best-practices
- Agent Skills Description Optimization: https://agentskills.io/skill-creation/optimizing-descriptions
- Agent Skills Evaluation: https://agentskills.io/skill-creation/evaluating-skills
- Agent Skills Scripts: https://agentskills.io/skill-creation/using-scripts

## Practical Takeaways

- Keep instructions explicit, direct, and constraint-heavy when behavior must be reliable.
- Use clear sections when prompts mix rules, examples, and context.
- For OpenAI, Codex, Apps SDK, MCP, model, or tool behavior, use official OpenAI docs or configured OpenAI Docs MCP first.
- Treat skill descriptions as the main trigger surface; test realistic positive and near-miss negative examples before broadening descriptions.
- Use progressive disclosure: keep core workflow in `SKILL.md`, and link references only when the agent needs them.
- Prefer eval-minded iteration over speculative wording.
- Keep missing requirements explicit and ask the user instead of guessing.

## OpenAI-First Transfer Rules

- Treat official Codex examples as the primary model for scaffolding, validation, `openai.yaml`, and resource packaging.
- Treat Claude-oriented skill patterns only as historical comparison, not as the contract another `.agents` skill should inherit.
- Reusable local scripts are acceptable when they implement Codex-compatible scaffolding or validation without introducing a foreign workflow contract.
- Keep local `.agents` extensions clearly separated from the native Codex skill contract so another agent can tell what is required versus bundle-specific.

Useful ideas that transfer into `.agents` skill authoring:

- progressive disclosure between frontmatter, `SKILL.md`, and optional references;
- trigger evals with realistic should-trigger and near-miss should-not-trigger prompts;
- workflow evals that test the drafted skill on realistic user requests;
- trace review, not just output review, when refining instructions;
- moving repeated deterministic helper work into `scripts/` or `assets/` only when repetition and stability justify the extra package weight.

For skill structure, discovery, metadata, configuration, MCP, sandbox, and approval behavior, keep official OpenAI Codex docs as the primary source of truth.