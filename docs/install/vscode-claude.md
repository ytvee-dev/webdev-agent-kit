---
id: 'agents.docs.install.vscode-claude'
title: 'Install WebDev Agent Kit for VS Code Claude'
doc_type: 'user-guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/install'
    - 'client/claude-code'
parent:
    - '[[docs/install/README|Installation Guides]]'
related:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[docs/mcp/claude|MCP in Claude Clients]]'
depends_on: []
---

# Install WebDev Agent Kit for VS Code Claude

1. Download the latest
   [VS Code Claude package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-vs-code-claude.tar.gz).

2. Extract the archive into a permanent local directory outside the project.
   The extracted plugin root must be the `webdev-agent-kit/` directory containing
   `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.

3. Open the Claude Code extension in VS Code, enter `/plugins`, and go to the
   **Marketplaces** tab.

4. Add a new marketplace and enter the absolute path to the extracted
   `webdev-agent-kit/` directory.

5. Go to the **Plugins** tab, find `webdev-agent-kit`, and select
   **Install for you**. User scope makes the plugin available in every project
   and does not modify `.claude/settings.json` in the current repository.

6. Restart Claude Code when prompted by the extension or run `/reload-plugins`,
   then open the installed plugins list and confirm that
   `webdev-agent-kit@webdev-agent-kit` is enabled.

[← All installation guides](README.md) · [MCP setup](../mcp/claude.md) · [All documentation](../README.md)
