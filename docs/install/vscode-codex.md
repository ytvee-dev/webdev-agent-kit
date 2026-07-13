---
id: 'agents.docs.install.vscode-codex'
title: 'VS Code Codex Install Guide'
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
depends_on: []
---

# Install WebDev Agent Kit for VS Code Codex

1. Download the latest
   [VS Code Codex bundle](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-vs-code-codex.tar.gz).

2. Extract the archive into your project root. After extraction, `.agents/`
   should be located directly in the root alongside your project files.

3. Add the following root-scoped entries to your project's `.gitignore` to
   keep the local agent bundle, Codex configuration, generated project context,
   and root instruction pointer out of the remote repository:

   ```gitignore
   /.agents/
   /.codex/
   /AGENTS.md
   ```

4. Open the Codex extension in VS Code and submit this prompt:

   ```text
   Adapt this .agents bundle to my project & create AGENTS.md into root
   ```

5. Open the Codex extension settings, go to **Personalization**, and select
   **Pragmatic** as the personality. Then copy the recommended prompt from
   [Custom instructions](https://github.com/ytvee-dev/webdev-agent-kit/wiki/Custom-instructions)
   into the **Custom instructions** field.

6. After adaptation, Codex creates `.agents/project/` with local project
   profiles, capability facts, and path indexes. During later work, it refreshes
   the affected context when material project facts change, such as after major
   refactors or new features. This is task-driven rather than a background file
   watcher. If the cached context needs a manual refresh, submit:

   ```text
   Refresh project context after these changes.
   ```

## Video Installation Guide

<video controls src="https://res.cloudinary.com/duyqvi0ig/video/upload/v1783954898/vscode-codex_tpg1aq.mp4"></video>
