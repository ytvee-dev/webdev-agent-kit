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
    []
depends_on:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
---

# Source-Backed Prompting

Use these sources when shaping agent rules, skill triggers, or workflow
instructions:

- OpenAI Codex Agent Skills: https://developers.openai.com/codex/skills
- OpenAI AGENTS guide: https://developers.openai.com/codex/guides/agents-md
- OpenAI Codex Best Practices: https://developers.openai.com/codex/learn/best-practices
- OpenAI Prompting: https://platform.openai.com/docs/guides/prompting
- OpenAI Prompt Engineering: https://platform.openai.com/docs/guides/prompt-engineering
- OpenAI Evals: https://platform.openai.com/docs/guides/evals
- OpenAI Docs MCP: https://developers.openai.com/learn/docs-mcp
- OpenAI Reasoning Best Practices: https://developers.openai.com/api/docs/guides/reasoning-best-practices
- OpenAI Agents Guidance: https://developers.openai.com/api/docs/guides/agents
- Local OpenAI system skills:
  - `codex-skills/skills/.system/skill-creator`
  - `codex-skills/skills/.system/openai-docs`
  - `codex-skills/skills/.system/skill-installer`
- Agent Skills Specification and related third-party material only as secondary
  context after OpenAI-native sources are exhausted
- Agent Skills Specification: https://agentskills.io/specification
- Agent Skills Best Practices: https://agentskills.io/skill-creation/best-practices
- Agent Skills Description Optimization: https://agentskills.io/skill-creation/optimizing-descriptions
- Agent Skills Evaluation: https://agentskills.io/skill-creation/evaluating-skills
- Agent Skills Scripts: https://agentskills.io/skill-creation/using-scripts

## Practical takeaways

- Keep instructions explicit, direct, and constraint-heavy when behavior must be
  reliable.
- Use clear sections and delimiters when prompts mix rules, examples, and
  context.
- For OpenAI API, Codex, ChatGPT, Apps SDK, MCP, model, or tool behavior, use
  the official OpenAI docs or configured OpenAI Docs MCP before relying on
  memory.
- Treat skill descriptions as the main trigger surface; test realistic positive
  and near-miss negative prompts before broadening descriptions.
- Use progressive disclosure: keep core workflow in `SKILL.md`, and link
  references only when the agent needs them.
- Prefer eval-minded iteration over speculative prompt wording.
- Keep missing requirements explicit and ask the user instead of guessing.

## OpenAI-first transfer rules

- Treat the official OpenAI system `skill-creator` as the primary local model
  for scaffolding, validation, `openai.yaml`, and resource packaging.
- Treat Claude-oriented skill-creator patterns only as historical comparison,
  not as the contract another `.agents` skill should inherit.
- Reusable local scripts are acceptable when they implement Codex-compatible
  scaffolding or validation without introducing a foreign workflow contract.
- Keep local `.agents` extensions clearly separated from the native Codex skill
  contract so another agent can tell what is required versus bundle-specific.

Useful ideas that transfer into `.agents` skill authoring:

- progressive disclosure between frontmatter, `SKILL.md`, and optional
  references;
- trigger evals with realistic should-trigger and near-miss should-not-trigger
  prompts;
- workflow evals that test the drafted skill on realistic user requests;
- trace review, not just output review, when refining instructions;
- moving repeated deterministic helper work into `scripts/` or `assets/` only
  when repetition and stability justify the extra package weight.

For skill structure, discovery, and metadata, keep official OpenAI Codex docs
as the primary source of truth.
