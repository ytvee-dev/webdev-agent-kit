---
id: 'agents.docs.mcp.index'
title: 'MCP for WebDev Agent Kit'
doc_type: 'user-guide-index'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/mcp'
parent:
    - '[[docs/README|WebDev Agent Kit Documentation]]'
related:
    - '[[docs/mcp/claude|MCP in Claude Clients]]'
    - '[[docs/mcp/codex-vscode|MCP in VS Code Codex]]'
    - '[[docs/mcp/cursor|MCP in Cursor]]'
    - '[[docs/install/README|Installation Guides]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
depends_on: []
---

# MCP for WebDev Agent Kit

[← All documentation](../README.md) · [Install WebDev Agent Kit](../install/README.md)

This document is the common entrypoint for installing and verifying MCP tools
that complement `webdev-agent-kit-main`. Select your client in the table below,
open the instructions for a specific MCP, and return to the
[MCP verification](#mcp-verification) section after installation.

WebDev Agent Kit uses a **capability-first** approach: a skill declares the
capability it needs, and an MCP, a built-in client tool, or another verified
provider can supply it. A server name alone does not prove availability. An MCP
is considered operational only after one of its tools is called successfully in
the current session.

## Installation Matrix

| MCP | Claude | VS Code Codex | Cursor |
| --- | --- | --- | --- |
| Context7 | [Claude: Context7](claude.md#claude-context7) | [Codex: Context7](codex-vscode.md#codex-context7) | [Cursor: Context7](cursor.md#cursor-context7) |
| Filesystem | [Claude: Filesystem](claude.md#claude-filesystem) | [Codex: Filesystem](codex-vscode.md#codex-filesystem) | [Cursor: Filesystem](cursor.md#cursor-filesystem) |
| MDN Docs | [Claude: MDN](claude.md#claude-mdn) | [Codex: MDN](codex-vscode.md#codex-mdn) | [Cursor: MDN](cursor.md#cursor-mdn) |
| OpenAI Developer Docs | [Claude: OpenAI Docs](claude.md#claude-openai-docs) | [Codex: OpenAI Docs](codex-vscode.md#codex-openai-docs) | [Cursor: OpenAI Docs](cursor.md#cursor-openai-docs) |
| Playwright | [Claude: Playwright](claude.md#claude-playwright) | [Codex: Playwright](codex-vscode.md#codex-playwright) | [Cursor: Playwright](cursor.md#cursor-playwright) |

Complete client instructions:

- [Claude Code CLI, VS Code, and Claude Desktop](claude.md#claude-clients);
- [VS Code Codex extension](codex-vscode.md#codex-in-vs-code);
- [Cursor](cursor.md#cursor-settings).

## Capability Map

| MCP | Capability | Primary purpose |
| --- | --- | --- |
| Context7 | `current_library_docs` | Current documentation for React, Next.js, TypeScript, and other libraries |
| Filesystem | `project_files` | Controlled access to project files |
| MDN Docs | `web_platform_docs` | HTML, CSS, Web APIs, accessibility, and browser compatibility |
| OpenAI Developer Docs | `openai_platform_docs` | Current documentation for OpenAI, Codex, and the Apps SDK |
| Playwright | `rendered_visual_evidence` | Browser, accessibility tree, viewport, console/network, and screenshots |

## General Requirements

Local STDIO Filesystem and Playwright servers require Node.js, npm, and npx.
Check them in PowerShell:

```powershell
node --version
npm --version
npx --version
```

If the commands are unavailable, install the current Node.js LTS release from
the [official website](https://nodejs.org/) and restart the client completely.

You will also need:

- internet access for remote MCPs and the first npm package download;
- an absolute project path for Filesystem;
- the ability to restart the client or begin a new session after configuration;
- user permission before installation, authorization, or changes to client
  configuration.

## Context7

### What It Is For

Context7 first resolves a package name to a canonical library ID, then retrieves
current documentation for that ID. It is useful when the behavior of React,
Next.js, TypeScript, Redux, TanStack, Axios, a package manager, or a build tool
may have changed.

The `current_library_docs` capability is optionally used by:

- `frontend-architecture-planner`;
- `frontend-bugfix-debugger`;
- `frontend-design-director`;
- `frontend-design-intelligence`;
- `frontend-layout-implementer`;
- `frontend-quality-reviewer`;
- `frontend-refactor-surgeon`;
- `greenfield-project-builder`;
- `project-context-adapter`;
- `project-onboarding-adapter`.

The absence of Context7 does not block these skills: official web documentation
for the library is an acceptable fallback.

### Authorization

Context7 must be authorized if the selected endpoint or client requires it. The
preferred option is OAuth through `https://mcp.context7.com/mcp/oauth`. If the
client uses an API key:

1. Create a key in the [Context7 dashboard](https://context7.com/dashboard).
2. Store it in an environment variable or the client's secure storage.
3. Do not put a real key in Markdown, `AGENTS.md`, `.mcp.json`, git, or public
   screenshots.

Official remote endpoint with an API key:

```text
URL: https://mcp.context7.com/mcp
Header: CONTEXT7_API_KEY: <YOUR_CONTEXT7_API_KEY>
```

The specific OAuth/API key method is documented separately for
[Claude](claude.md#claude-context7),
[Codex](codex-vscode.md#codex-context7), and
[Cursor](cursor.md#cursor-context7).

Source: [official Context7 documentation](https://context7.com/docs/resources/all-clients).

## Filesystem

### What It Is For

Filesystem provides reading, searching, metadata, and, only within an authorized
task, file changes. The server can see only the directories passed in its
arguments. Native client file tools can satisfy the same capability, so a
separate Filesystem MCP is not always required.

The `project_files` capability is required for core work by:

- `agent-rules-skill-author`;
- `frontend-architecture-planner`;
- `frontend-bugfix-debugger`;
- `frontend-layout-implementer`;
- `frontend-linter-manager`;
- `frontend-quality-reviewer`;
- `frontend-refactor-surgeon`;
- `mcp-toolchain-manager`;
- `pattern-library-manager`;
- `project-context-adapter`;
- `project-onboarding-adapter`.

It is required only when the scope calls for it by:

- `execution-plan-manager`;
- `frontend-design-director`;
- `frontend-design-intelligence`;
- `frontend-visual-qa`;
- `goal-planner`;
- `greenfield-project-builder`;
- `loop-workflow-planner`.

These dependencies apply to the capability, not necessarily to the specific
Filesystem MCP.

### Security

- Allow only the directory of the required project.
- Do not pass the drive root, the entire user profile, or a shared directory
  containing personal files.
- The presence of write tools is not permission to change files: the current
  task, sandbox, and approval policy still apply.

Source: [official Filesystem MCP](https://github.com/modelcontextprotocol/servers/blob/main/src/filesystem/README.md).

## MDN Docs

### What It Is For

MDN Docs provides current information about HTML, CSS, Web APIs,
accessibility, specifications, and Browser Compatibility Data.

The `web_platform_docs` capability is required when relevant to the scope by:

- `design-screenshot-spec`.

It is optionally used by:

- `frontend-architecture-planner`;
- `frontend-bugfix-debugger`;
- `frontend-design-director`;
- `frontend-design-intelligence`;
- `frontend-layout-implementer`;
- `frontend-quality-reviewer`;
- `frontend-refactor-surgeon`;
- `frontend-visual-qa`;
- `project-context-adapter`;
- `project-onboarding-adapter`.

The MDN MCP is experimental and may be withdrawn. Mozilla states that it stores
request data during the experiment. Do not send secrets or private code. The
`X-Moz-1st-Party-Data-Opt-Out: 1` header disables first-party analytics but does
not cancel the other data-processing terms.

Source: [MDN MCP server](https://developer.mozilla.org/en-US/mcp).

## OpenAI Developer Docs

### What It Is For

OpenAI Developer Docs searches official OpenAI documentation and returns the
matching pages. It is used for current questions about the OpenAI API, ChatGPT
Apps SDK, Codex, models, MCP, skills, plugins, sandbox, and configuration.

The server provides documentation only: it does not call the OpenAI API, check
an account, or require an OpenAI API key.

The `openai_platform_docs` capability is required when current OpenAI information
affects the task by:

- `agent-rules-skill-author`;
- `frontend-architecture-planner`;
- `frontend-bugfix-debugger`;
- `frontend-layout-implementer`;
- `frontend-quality-reviewer`;
- `frontend-refactor-surgeon`;
- `greenfield-project-builder`;
- `mcp-toolchain-manager`;
- `pattern-library-manager`;
- `project-context-adapter`;
- `project-onboarding-adapter`.

Source: [official OpenAI Docs MCP page](https://developers.openai.com/learn/docs-mcp).

## Playwright

### What It Is For

Playwright controls a real browser: it opens pages, retrieves accessibility
snapshots, interacts with elements, changes the viewport, captures screenshots,
and inspects console/network activity.

The `rendered_visual_evidence` capability is required by:

- `frontend-visual-qa`.

It is required when relevant to the scope by:

- `frontend-bugfix-debugger`;
- `frontend-design-director`;
- `frontend-layout-implementer`;
- `frontend-quality-reviewer`;
- `frontend-refactor-surgeon`.

Playwright is not a security boundary. Verify the URL and action, do not provide
credentials unnecessarily, and choose one-time permission instead of permanent
permission for a one-off check.

Source: [official Playwright MCP](https://github.com/microsoft/playwright-mcp).

## MCP Verification

A configuration entry or green toggle confirms only that a server is configured.
Actual availability is confirmed by a successful MCP tool call in the current
session.

After installation:

1. Restart the client or extension.
2. Begin a new session so that the tool registry refreshes.
3. Check the server list using the client controls.
4. Run the prompts below.

### Verify Filesystem

```text
Use the Filesystem MCP and verify how it works
```

Success: the server shows the restricted allowed path, returns a file list, and
reads `package.json` without writing.

### Verify Context7

```text
Use the Context7 MCP and verify how it works
```

Success: a library ID is returned first, followed by documentation for that ID.

### Verify MDN Docs

```text
Use the MDN MCP and verify how it works
```

Success: `search`, `get_doc`, and `get_compat` work, including Browser
Compatibility Data.

### Verify Playwright

```text
Use the Playwright MCP and verify how it works
```

Success: the browser opens, a link is found through the accessibility tree,
navigation and network activity are confirmed, and the page closes.

### Verify OpenAI Developer Docs

```text
Use the OpenAI Developer Docs MCP and verify how it works
```

Success: the server searches official OpenAI docs, retrieves a page, and returns
endpoints from the current specification.

## Readiness Criterion

An MCP is ready when it:

- is present and enabled in the client;
- loads after restart;
- provides the expected tools in a new session;
- successfully runs the functional prompt above.

If the server is displayed but its tools cannot be called, it is **configured
but not confirmed as available**. Check the endpoint, command, arguments,
environment variables, allowed path, authorization, network, and startup logs.

[↑ Back to the installation matrix](#installation-matrix) · [← All documentation](../README.md)
