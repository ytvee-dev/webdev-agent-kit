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

Project mode requires the managed `.kimi-code/AGENTS.md` pointer: preview
`configure_kimi.py --project ROOT`, then approve within authorized onboarding.
Kimi does not auto-read project `.agents/AGENTS.md`.
Alternatively install a clean release staging directory as a user-wide plugin;
never install a working project's `.agents`, which may contain private state.
Reinstall clean payloads after upgrades. Avoid duplicate local/plugin runtimes.
Plugin skill names use `webdev-agent-kit:`. Keep facts/memory in host
`.agents/project` and `.agents/learning`.

Nine `wdk-*` roles need bounded handoffs with absolute bundle/host roots,
evidence, owned paths and acceptance criteria. Nested delegation is disabled.
Model selection follows Kimi's secondary-model configuration, not role names.
Verify delegation; retain single-agent fallback.

Capture is opt-in: preview `install_kimi_hooks.py`, approve setup, separately
enable `learning.py on`. Missing/truncated content stays marked. Never read
transcripts implicitly. Proposals/benchmarks accept `--engine kimi --kimi-model ALIAS`
with tools/subagents disabled; attachments remain metadata-only.

Follow the installation guide. Static checks do not establish live behavior.
