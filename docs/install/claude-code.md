---
id: 'agents.docs.install.claude-code'
title: 'Install WebDev Agent Kit for Claude Code'
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

# Install WebDev Agent Kit for Claude Code

1. Download the latest
   [Claude Code package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-claude-code.tar.gz).

2. Extract the archive into a permanent local directory outside the project.
   The extracted plugin root must be the `webdev-agent-kit/` directory containing
   `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.

3. Add the extracted directory as a local marketplace. Replace the quoted path
   with the absolute path to the `webdev-agent-kit/` directory:

   ```text
   claude plugin marketplace add "<path-to-directory>/webdev-agent-kit"
   ```

4. Install the plugin in user scope so it is available in every project and does
   not modify `.claude/settings.json` in the current repository:

   ```text
   claude plugin install webdev-agent-kit@webdev-agent-kit --scope user
   ```

5. Start Claude Code. If the installation was performed during an open session,
   apply the changes without restarting:

   ```text
   /reload-plugins
   ```

6. Verify the installation with `claude plugin list`, or open `/plugin` and
   confirm that `webdev-agent-kit@webdev-agent-kit` is enabled in user scope.

[← All installation guides](README.md) · [MCP setup](../mcp/claude.md) · [All documentation](../README.md)
