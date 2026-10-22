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

MCP (Model Context Protocol) connects an agent to external tools, such as library
documentation or a browser. Install only the servers you need. Built-in client
tools can often do the same job.

Choose your client below, follow the server's setup steps, then run the
[MCP checks](#mcp-verification). A server is confirmed working when one of its
tools returns a useful result in your current session.

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

Use it when a task depends on a library's current API. If Context7 is unavailable,
the agent can read that library's official web documentation instead.

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

Most coding tasks need file access. Use the client's built-in file tools if they
already provide the access you need; a separate Filesystem server is optional.

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

Source: [official OpenAI Docs MCP page](https://developers.openai.com/learn/docs-mcp).

## Playwright

### What It Is For

Playwright controls a real browser: it opens pages, retrieves accessibility
snapshots, interacts with elements, changes the viewport, captures screenshots,
and inspects console/network activity.

Use it to check the rendered page and interactions. It is optional when your
client already has a browser tool that can perform the same checks.

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
Use Filesystem MCP to list the allowed project directory and read package.json.
Do not write files.
```

Success: the server shows the restricted allowed path, returns a file list, and
reads `package.json` without writing.

### Verify Context7

```text
Use Context7 to find documentation for the installed React version.
Resolve the library ID, retrieve a relevant page and report the source.
```

Success: a library ID is returned first, followed by documentation for that ID.

### Verify MDN Docs

```text
Use MDN MCP to find CSS grid documentation and its browser compatibility.
```

Success: the server returns the requested documentation and compatibility data.

### Verify Playwright

```text
Use Playwright MCP to open https://example.com, read its heading and close
the page. Do not submit forms or change browser settings.
```

Success: the browser opens the page, returns its actual heading and closes it.

### Verify OpenAI Developer Docs

```text
Use OpenAI Developer Docs MCP to find and read the Codex MCP setup guide.
Return the official source link.
```

Success: the server finds the official guide and reads its content.

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
