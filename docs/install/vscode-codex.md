---
id: 'agents.docs.install.vscode-codex'
title: 'Install WebDev Agent Kit for VS Code Codex'
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
    - '[[docs/mcp/codex-vscode|MCP in VS Code Codex]]'
depends_on: []
---

# Install WebDev Agent Kit for VS Code Codex

1. Download the latest
   [VS Code Codex package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-vs-code-codex.tar.gz).

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

4. Open the Codex extension in VS Code and send this prompt:

   ```text
   Adapt this .agents bundle to my project and create AGENTS.md in the root
   ```

5. Open the Codex extension settings, go to **Personalization**, and select the
   **Pragmatic** personality. Then copy the recommended prompt from
   [Custom instructions](https://github.com/ytvee-dev/webdev-agent-kit/wiki/Custom-instructions)
   into the **Custom instructions** field.

6. After adaptation, Codex creates `.agents/project/` with local project
   profiles, capability information, and path indexes. During subsequent work,
   it updates the affected context when project facts change substantially, for
   example after a major refactor or feature addition. This happens as part of
   tasks, not through background file monitoring. To refresh cached context
   manually, send:

   ```text
   Update the project context after these changes.
   ```

## Installation Video Guide

[![Watch the VS Code Codex installation video guide](https://res.cloudinary.com/duyqvi0ig/video/upload/so_0,w_1280,c_limit,q_auto/v1784235091/vs-code-codex_ilqrde.jpg)](https://res.cloudinary.com/duyqvi0ig/video/upload/v1784235091/vs-code-codex_ilqrde.mp4)

[← All installation guides](README.md) · [MCP setup](../mcp/codex-vscode.md) · [All documentation](../README.md)
