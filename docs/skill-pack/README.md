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
- `PROMPT_INTENT_ROUTING.md` - prompt intent and task scale gate that prevents small prompts from triggering heavy planning.
- `CODEX_CLAUDE_COMPATIBILITY.md` - cross-agent compatibility plan for Codex and Claude Code targets.
- `README_RUNTIME_BOUNDARY.md` - rule that repository README files are human-facing only and must not participate in agent runtime flow.
- `DIST_CLEANUP.md` - source-first generated distribution cleanup policy.
- `LINT_POLICY_NOTE.md` - lint verification and approval-gated linter setup note.
- `TARGET_STACK_NARROWING.md` - active note that narrows the pack to React, Next.js, CSS Modules, Redux, TanStack, and Axios.

## Non-Goals For This Draft

- Do not implement new skills yet.
- Do not rename existing skills yet.
- Do not change existing runtime routing yet.
- Do not create a pull request from this branch.
- Do not copy project-specific facts into reusable skill instructions.

## Language Policy

All reusable skill instructions, architecture documents, rules, templates, and future skill files in this package must be written in English.

## Architecture Sources

This architecture is based on official docs for OpenAI Codex skills, MCP, React, Next.js, CSS Modules, Redux, TanStack, Axios, TypeScript, MDN, accessibility, performance, and frontend security.
