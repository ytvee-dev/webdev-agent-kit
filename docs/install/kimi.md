---
id: 'agents.docs.install.kimi'
title: 'Install WebDev Agent Kit for Kimi Code'
doc_type: 'user-guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/install'
    - 'client/kimi'
parent:
    - '[[docs/install/README|Installation Guides]]'
related:
    - '[[docs/install/gpt-model-routing]]'
    - '[[docs/install/first-run|First Run And Installation Checks]]'
    - '[[docs/install/upgrade|Upgrade And Rollback]]'
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
    - '[[docs/mcp/README|MCP for WebDev Agent Kit]]'
depends_on: []
---

# Install WebDev Agent Kit for Kimi Code

Complete the [first-run checks](first-run.md). Preserve existing installations
using [upgrade and rollback](upgrade.md).

1. Download the [Kimi project package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-kimi.tar.gz).
2. Extract it into the project root: skills belong under `.agents/skills`, with
   policy, references and scripts alongside them inside `.agents/`.
3. Preserve existing host instructions and `.agents/project/` and
   `.agents/learning/` state. Keep private state excluded from Git.
4. Start a fresh Kimi Code session in that project and invoke
   `/skill:project-context-adapter`. Ask it to inspect the project and adapt
   project facts, using `.agents/adapters/kimi.md`. Verify that the skill loads
   its policy and supporting files. Do not overwrite an existing AGENTS.md.
5. Keep the selected model and permissions. K3 requires availability in the
   user's Kimi account; this package does not provision credentials or models.

The adapter uses documented project skill discovery and `${KIMI_SKILL_DIR}`.
Packaging checks do not prove live model behavior. Automatic Kimi capture and
Kimi-specific learning evaluation are not included; use explicit canonical JSONL
import and the portable memory CLI when requested. Existing Codex/OpenCode
runners must not be reported as Kimi evaluation.

[Official skill documentation](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)

[All installation guides](README.md)
