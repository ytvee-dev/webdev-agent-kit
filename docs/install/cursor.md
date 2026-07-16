---
id: 'agents.docs.install.cursor'
title: 'Install WebDev Agent Kit for Cursor'
doc_type: 'user-guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/install'
    - 'client/cursor'
parent:
    - '[[docs/install/README|Installation Guides]]'
related:
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[docs/mcp/cursor|MCP in Cursor]]'
depends_on: []
---

# Install WebDev Agent Kit for Cursor

1. Download the latest
   [Cursor package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-cursor.tar.gz).

2. Extract the archive into the project root. After extraction, the `.agents/`
   directory and the following rule must be next to the project files:
   `.cursor/rules/webdev-agent-kit.mdc`.

3. Add the following root-anchored entries to the project's `.gitignore` so the
   local agent kit, Cursor rule, generated project context, and root instruction
   pointer are not committed to the remote repository:

   ```gitignore
   /.agents/
   /.cursor/rules/webdev-agent-kit.mdc
   /AGENTS.md
   ```

4. Open the project in Cursor, start Agent, and send this prompt:

   ```text
   Adapt this .agents bundle to my project and create AGENTS.md in the root
   ```

5. After adaptation, Cursor creates `.agents/project/` with local information
   about the stack, architecture, available tools, and important project paths.
   During subsequent work, this context is updated when the project changes
   substantially. To request an update manually, send:

   ```text
   Update the project context after these changes.
   ```

## Installation Video Guide

[![Watch the Cursor installation video guide](https://res.cloudinary.com/duyqvi0ig/video/upload/so_0,w_1280,c_limit,q_auto/v1784235087/cursor_qj5lqq.jpg)](https://res.cloudinary.com/duyqvi0ig/video/upload/v1784235087/cursor_qj5lqq.mp4)

[← All installation guides](README.md) · [MCP setup](../mcp/cursor.md) · [All documentation](../README.md)
