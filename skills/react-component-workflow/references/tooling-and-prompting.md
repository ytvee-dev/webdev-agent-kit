---
id: 'agents.skills.react-component-workflow.references.tooling-and-prompting'
title: 'Tooling And Prompting'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'react-component-workflow'
tags:
    - 'agents/skill-package'
    - 'frontend/react'
    - 'agents/reference'
parent:
    - '[[skills/react-component-workflow/SKILL|React Component Workflow]]'
related:
    []
depends_on:
    - '[[skills/react-component-workflow/SKILL|React Component Workflow]]'
---

# Tooling And Prompting

- Prefer MCP tools and framework indexes before broad repo scanning whenever the
  required tool or context is available.
- Keep prompts, implementation notes, and review summaries direct and explicit.
- Do not invent missing component behavior, API shapes, or architecture. Narrow
  the search first, then ask the user when the repo still does not answer the need.
- Keep constraints explicit and success criteria concrete.

## Source-backed guidance

- OpenAI Prompting: https://platform.openai.com/docs/guides/prompting
- OpenAI Prompt Engineering: https://platform.openai.com/docs/guides/prompt-engineering
- OpenAI Reasoning Best Practices: https://developers.openai.com/api/docs/guides/reasoning-best-practices
- OpenAI Agents Guidance: https://developers.openai.com/api/docs/guides/agents
- Anthropic Prompt Best Practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#structure-prompts-with-xml-tags
