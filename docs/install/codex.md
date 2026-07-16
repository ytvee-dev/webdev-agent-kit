---
id: 'agents.docs.install.codex'
title: 'Install WebDev Agent Kit for Codex'
doc_type: 'user-guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/install'
    - 'client/codex'
parent:
    - '[[docs/install/README|Installation Guides]]'
related:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
    - '[[docs/mcp/README|MCP for WebDev Agent Kit]]'
depends_on: []
---

# Install WebDev Agent Kit for Codex

1. Download the latest
   [Codex package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-codex.tar.gz).

2. Extract the archive into the project root. After extraction, the `.agents/`
   directory must be located directly in the root next to the project files.

3. Add the following root-anchored entries to the project's `.gitignore` so the
   local agent kit, Codex configuration, generated project context, and root
   instruction pointer are not committed to the remote repository:

   ```gitignore
   /.agents/
   /.codex/
   /AGENTS.md
   ```

4. Start Codex from the project root and send this prompt:

   ```text
   Adapt this .agents bundle to my project and create AGENTS.md in the root
   ```

5. After adaptation, Codex creates `.agents/project/` with local information
   about the stack, architecture, available tools, and important project paths.
   During subsequent work, this context is updated when the project changes
   substantially. To request an update manually, send:

   ```text
   Update the project context after these changes.
   ```

[← All installation guides](README.md) · [MCP for WebDev Agent Kit](../mcp/README.md) · [All documentation](../README.md)
