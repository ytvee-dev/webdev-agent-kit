---
id: 'agents.docs.install.index'
title: 'Installation Guides'
doc_type: 'user-guide-index'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/install'
parent:
    - '[[docs/README|WebDev Agent Kit Documentation]]'
related:
    - '[[docs/install/opencode]]'
    - '[[docs/install/model-capability-guide]]'
    - '[[docs/install/roles]]'
    - '[[docs/install/codex|Install for Codex]]'
    - '[[docs/install/claude-code|Install for Claude Code]]'
    - '[[docs/install/cursor|Install for Cursor]]'
    - '[[docs/install/vscode-codex|Install for VS Code Codex]]'
    - '[[docs/install/vscode-claude|Install for VS Code Claude]]'
    - '[[docs/mcp/README|MCP for WebDev Agent Kit]]'
depends_on: []
---

# Installation Guides

[← All documentation](../README.md)

Choose the client you use to open your project:

| Client | Guide |
| --- | --- |
| Codex | [Install for Codex](codex.md) |
| Claude Code | [Install the Claude plugin](claude-code.md) |
| Cursor | [Install for Cursor](cursor.md) |
| VS Code with Codex | [Install for VS Code Codex](vscode-codex.md) |
| VS Code with Claude Code | [Install for VS Code Claude](vscode-claude.md) |
| OpenCode on Windows | [Use the OpenCode installer](opencode.md) |

Read [first-run checks](first-run.md) before extracting a package. If the Kit
is already installed, use [upgrade and rollback](upgrade.md).

## After installation

- [Choose a model and check tool support](model-capability-guide.md)
- [Set up MCP servers](../mcp/README.md)
- [Select a frontend or designer role](roles.md)
- [Set up Codex subagents](gpt-model-routing.md)
- [Adapt the Claude plugin to a project](claude-agents.md)

## Video guides

- [Cursor — text and video guide](cursor.md)
- [VS Code Codex — text and video guide](vscode-codex.md)

These pages are user guides, not runtime policy. Maintainers define package
contents in `bundle-manifest.json` and check them with the archive validators.
