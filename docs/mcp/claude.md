---
id: 'agents.docs.mcp.claude'
title: 'Install MCP in Claude Clients'
doc_type: 'user-guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/mcp'
    - 'client/claude-code'
parent:
    - '[[docs/mcp/README|MCP for WebDev Agent Kit]]'
related:
    - '[[docs/install/claude-code|Install for Claude Code]]'
    - '[[docs/install/vscode-claude|Install for VS Code Claude Code]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
depends_on: []
---

# Install MCP in Claude Clients

[← All MCPs](README.md) · [Install for Claude Code](../install/claude-code.md) · [Install for VS Code](../install/vscode-claude.md)

This guide covers installation for the Claude Code CLI, the official Claude Code
extension for VS Code, the **Code** tab in Claude Desktop, and regular Claude
Desktop chat on Windows. MCP purposes, skill relationships, and common tests are
in the [general MCP guide](README.md).

## Claude Clients

The Claude Code CLI, VS Code extension, and **Code** tab in Claude Desktop use
the same engine and shared configuration:

- `~/.claude.json` — personal local/user MCPs;
- `.mcp.json` in the project root — shared project configuration;
- `CLAUDE.md` and Claude Code settings.

Therefore, a server added once through `claude mcp add` is available in all
three Claude Code clients within the selected `scope`.

> Regular Claude Desktop chat is a separate surface. Its local
> `%APPDATA%\Claude\claude_desktop_config.json` is not shared with Claude Code.
> Separate configuration for regular chat is described in the
> [regular Claude Desktop chat](#regular-claude-desktop-chat) section.

### How to Open the Console

#### Claude Code CLI

1. Open PowerShell or Windows Terminal.
2. Go to the project root:

   ```powershell
   cd "C:\full\path\to\project"
   ```

3. Start an interactive session if needed:

   ```powershell
   claude
   ```

You can run `claude mcp add` commands without entering an interactive session.

#### Claude Code Extension for VS Code

1. Open the project in VS Code.
2. Select **Terminal → New Terminal** or press ``Ctrl+` ``.
3. Make sure the terminal is open at the project root.
4. Run the same `claude mcp add` commands shown below.
5. Use `/mcp` in the Claude Code panel to manage connections.

#### Claude Desktop — Code Tab

1. Open Claude Desktop and select the **Code** tab.
2. Create a session with the **Local** environment.
3. Select the project directory.
4. Press ``Ctrl+` `` to open the integrated terminal.
5. Run the same `claude mcp add` commands.

### How to Select a Scope

| Scope | Where it works | Where it is stored | Recommendation |
| --- | --- | --- | --- |
| `user` | In all of the user's local projects | `~/.claude.json` | Documentation and Playwright |
| `local` | Only for you in the current project | `~/.claude.json`, inside the project entry | Filesystem with a specific path |
| `project` | In the current project for the team | `.mcp.json` | Only for safe shared configuration without secrets |

The commands below use `user` for portable servers and `local` for Filesystem.
All Claude CLI options appear before the MCP name, and `--` separates the name
from the STDIO server command.

## Claude: Context7

### Shared Installation for Claude Code Clients

Add the remote OAuth endpoint once:

```powershell
claude mcp add --transport http --scope user context7 https://mcp.context7.com/mcp/oauth
```

Then open Claude Code in any of the three clients and enter:

```text
/mcp
```

Select `context7`, choose the authorization action, and complete sign-in in the
browser. After returning, verify the **connected** status.

If OAuth is unavailable, create an API key in the
[Context7 dashboard](https://context7.com/dashboard) and use the fallback:

```powershell
claude mcp add --transport http --scope user --header "CONTEXT7_API_KEY: <YOUR_CONTEXT7_API_KEY>" context7 https://mcp.context7.com/mcp
```

The command containing the key may remain in terminal history. OAuth is
preferred; do not commit the key or put it in documentation.

Verification:

```powershell
claude mcp get context7
```

## Claude: Filesystem

Filesystem is bound to an allowed directory, so add it from the required project
root with the `local` scope:

```powershell
cd "C:\full\path\to\project"
claude mcp add --transport stdio --scope local filesystem -- cmd /c npx -y @modelcontextprotocol/server-filesystem "C:\full\path\to\project"
```

Allow only the project directory, not the drive root or the entire user profile.
Repeat the command with the appropriate path for another project.

Verification:

```powershell
claude mcp get filesystem
```

## Claude: MDN

Add the remote MDN MCP for all Claude Code projects:

```powershell
claude mcp add --transport http --scope user --header "X-Moz-1st-Party-Data-Opt-Out: 1" mdn https://mcp.mdn.mozilla.net/
```

The header disables first-party analytics. The MDN MCP remains experimental;
do not send secrets or private code through it.

Verification:

```powershell
claude mcp get mdn
```

## Claude: OpenAI Docs

Add the official documentation-only server:

```powershell
claude mcp add --transport http --scope user openai-docs https://developers.openai.com/mcp
```

An OpenAI API key is not required.

Verification:

```powershell
claude mcp get openai-docs
```

## Claude: Playwright

Add local Playwright for all Claude Code projects:

```powershell
claude mcp add --transport stdio --scope user playwright -- npx.cmd -y "@playwright/mcp@latest"
```

Playwright controls a browser. Approve only expected URLs and actions.

Verification:

```powershell
claude mcp get playwright
```

## Verify Claude Code

After installing the servers:

```powershell
claude mcp list
```

Then:

1. Restart the Claude Code surface or begin a new session.
2. Enter `/mcp`.
3. Make sure the servers have **connected** status and show tools.
4. Complete OAuth for Context7 if authorization is still pending.
5. Run the prompts from the [general MCP verification section](README.md#mcp-verification).

If a server does not connect, start Claude Code with MCP debug output:

```powershell
claude --debug mcp
```

Official information about commands, scopes, and `/mcp`:
[Claude Code MCP](https://code.claude.com/docs/en/mcp).

## Regular Claude Desktop Chat

This section applies to regular Claude Desktop chat, not the **Code** tab.
Regular chat does not use MCPs added through `claude mcp add`.

### Remote MCPs: Context7, MDN, and OpenAI Docs

Add remote MCPs as custom connectors:

1. Open Claude Desktop.
2. Go to **Settings → Connectors**. In some versions, the path is called
   **Customize → Connectors**.
3. Select the option to add a custom connector.
4. Enter a name and URL:

   | Name | URL | Authorization |
   | --- | --- | --- |
   | `context7` | `https://mcp.context7.com/mcp/oauth` | Complete OAuth sign-in |
   | `mdn` | `https://mcp.mdn.mozilla.net/` | Not required; add the opt-out header if the UI supports it |
   | `openai-docs` | `https://developers.openai.com/mcp` | Not required |

5. Confirm browser access for Context7.
6. In a new chat, select **+ → Connectors** and enable the required tools.

Remote connections are configured through the Claude account and may be
available in other Claude clients, but this is a separate mechanism from local
Claude Code configuration.

### Local MCPs: Filesystem and Playwright

The preferred route is Desktop Extensions:

1. Open **Settings → Extensions**.
2. Select **Browse extensions**.
3. If the required extension is available and verified, select **Install**.
4. Specify the allowed path or other parameters in the extension UI.

If no ready-made Desktop Extension is available, use the manual config:

1. Open **Settings → Developer → Edit Config**.
2. The following file opens:

   ```text
   %APPDATA%\Claude\claude_desktop_config.json
   ```

3. Merge the entries with the existing `mcpServers`:

   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "cmd",
         "args": [
           "/c",
           "npx",
           "-y",
           "@modelcontextprotocol/server-filesystem",
           "C:\\full\\path\\to\\project"
         ]
       },
       "playwright": {
         "command": "npx.cmd",
         "args": [
           "-y",
           "@playwright/mcp@latest"
         ]
       }
     }
   }
   ```

4. Quit Claude Desktop completely, including its system tray process, and start
   it again.
5. In the chat, select **+ → Connectors** and check the tools that appeared.

Do not add remote URLs to `claude_desktop_config.json`: for regular Desktop
chat, remote servers are configured through Connectors.

Sources:

- [Claude Code in Desktop and shared configuration](https://code.claude.com/docs/en/desktop);
- [Claude Code in VS Code](https://code.claude.com/docs/en/ide-integrations);
- [local MCPs in Claude Desktop](https://modelcontextprotocol.io/docs/develop/connect-local-servers);
- [custom remote connections](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).

[↑ Back to the MCP list](README.md#installation-matrix) · [← All documentation](../README.md)
