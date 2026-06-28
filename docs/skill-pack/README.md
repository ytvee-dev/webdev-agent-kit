# WebDev Assistant Skill Pack Architecture

Status: draft architecture.
Branch: `architecture/webdev-assistant-skill-pack`.
Scope: documentation only. No production skill behavior is changed by this draft.

This directory captures the proposed architecture for turning `webdev-assistant` into an installable frontend engineering skill pack for coding agents.

## Documents

- `ARCHITECTURE.md` - full skill pack blueprint, layers, skill catalog, pipelines, file model, and source hierarchy.
- `OPERATING_MODEL.md` - goal setting, planning, execution loops, checkpoints, token budget, approval gates, and stop/resume behavior.
- `MCP_TOOLING.md` - required and optional MCP/tooling model, safe installation workflow, and `agents/openai.yaml` dependency policy.
- `DESIGN_INTELLIGENCE.md` - design-direction layer, anti-template defaults, visual memory, screenshot repair loop, copy rules, motion rules, and CSS specificity checks.
- `IMPLEMENTATION_PLAN.md` - staged plan for turning this architecture into concrete skills later.

## Non-Goals For This Draft

- Do not implement new skills yet.
- Do not rename existing skills yet.
- Do not change existing runtime routing yet.
- Do not create a pull request from this branch.
- Do not copy project-specific facts into reusable skill instructions.

## Language Policy

All reusable skill instructions, architecture documents, rules, templates, and future skill files in this package must be written in English.

## Architecture Sources

This architecture is based on:

- OpenAI Codex Agent Skills documentation: https://developers.openai.com/codex/skills
- OpenAI Codex best practices: https://developers.openai.com/codex/learn/best-practices
- Model Context Protocol tools specification: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- Anthropic frontend-design skill: https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md
- React docs: https://react.dev
- Redux docs: https://redux.js.org
- TypeScript docs: https://www.typescriptlang.org/docs
- MDN Web Docs: https://developer.mozilla.org
- W3C WAI / WCAG: https://www.w3.org/WAI/standards-guidelines/wcag
- web.dev performance guidance: https://web.dev/learn/performance
- OWASP cheat sheets: https://cheatsheetseries.owasp.org
