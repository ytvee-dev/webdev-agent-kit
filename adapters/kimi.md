---
id: 'agents.adapters.kimi'
title: 'Kimi Code Adapter'
doc_type: 'adapter'
layer: 'adapter'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/adapter'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related: []
depends_on:
    - '[[common/core/runtime-core-policy|Portable Runtime Core]]'
---

# Kimi Code Adapter

Target Kimi Code v2: `.agents/skills`, `${KIMI_SKILL_DIR}`, Markdown agents and
native plugins. Preserve host instructions, model, authentication and permissions.

Project skills load policy through their prelude. For startup instructions,
install the extracted `.agents` directory with `/plugins install ABSOLUTE_PATH`,
then `/plugins reload`. Plugins are user-wide managed copies; reinstall after
upgrades. Plugin skill names use `webdev-agent-kit:`. Avoid duplicate installations.
Keep host facts/memory under the host `.agents/project` and `.agents/learning`.

Nine `wdk-*` roles require bounded handoffs with absolute bundle/host roots,
evidence, owned paths and acceptance criteria. Nested delegation is disabled.
Verify tools and delegation; retain single-agent fallback.

Capture is opt-in: preview `install_kimi_hooks.py --project ROOT`, approve setup,
then separately enable `learning.py on`. Missing assistant text stays marked;
never read transcripts implicitly. Proposals and benchmarks accept `--engine kimi`
with tools/subagents disabled. Attachments remain metadata-only.

Follow the installation guide for commands and acceptance checks. Static checks
do not establish live client behavior.

[Official docs](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)
inspected 2026-11-03.
