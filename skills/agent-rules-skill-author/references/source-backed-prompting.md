# Source-Backed Prompting

Use these sources when shaping agent rules, skill triggers, or workflow
instructions:

- OpenAI Codex Agent Skills: https://developers.openai.com/codex/skills
- OpenAI Codex Best Practices: https://developers.openai.com/codex/learn/best-practices
- OpenAI Prompting: https://platform.openai.com/docs/guides/prompting
- OpenAI Prompt Engineering: https://platform.openai.com/docs/guides/prompt-engineering
- OpenAI Evals: https://platform.openai.com/docs/guides/evals
- OpenAI Docs MCP: https://developers.openai.com/learn/docs-mcp
- OpenAI Reasoning Best Practices: https://developers.openai.com/api/docs/guides/reasoning-best-practices
- OpenAI Agents Guidance: https://developers.openai.com/api/docs/guides/agents
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
