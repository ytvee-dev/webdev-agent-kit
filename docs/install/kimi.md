---
id: 'agents.docs.install.kimi'
title: 'Install WebDev Agent Kit for Kimi Code'
doc_type: 'user-guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'docs/install'
    - 'client/kimi'
parent:
    - '[[docs/install/README|Installation Guides]]'
related:
    - '[[docs/install/gpt-model-routing]]'
    - '[[docs/install/first-run|First Run And Installation Checks]]'
    - '[[docs/install/upgrade|Upgrade And Rollback]]'
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
    - '[[docs/mcp/README|MCP for WebDev Agent Kit]]'
depends_on: []
---

# Install WebDev Agent Kit for Kimi Code

Complete the [first-run checks](first-run.md). Preserve existing installations
using [upgrade and rollback](upgrade.md).

## Project installation (recommended)

1. Download the [Kimi project package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-kimi.tar.gz).
2. Extract it into the project root: skills belong under `.agents/skills`, with
   policy, references and scripts alongside them inside `.agents/`.
3. Preserve existing host instructions, `.agents/project/` and `.agents/learning/`
   state. Keep private state excluded from Git.
4. Preview and merge the native startup pointer:

   ```sh
   python .agents/skills/project-onboarding-adapter/scripts/configure_kimi.py --project .
   python .agents/skills/project-onboarding-adapter/scripts/configure_kimi.py --project . --approve
   ```

5. Start a fresh Kimi Code session and invoke `/skill:project-context-adapter`.
   Inspect the project and adapt facts using `.agents/adapters/kimi.md`.
   Verify startup policy, supporting files and one read-only role handoff.

Kimi discovers project skills, but does not automatically read the project's
`.agents/AGENTS.md`. The helper adds a managed pointer in `.kimi-code/AGENTS.md`,
preserving existing text and backing it up before changes. The pointer contains
absolute local paths; keep it local or regenerate after moving the project.
Preview removal with `--remove`, then add `--approve` to remove only its block.
Do not install this working `.agents` directory as a user-wide plugin.

## Alternative: user-wide plugin

Choose this mode instead of the project runtime installation. Extract a fresh
release archive into a clean staging directory outside all host projects:

```text
/plugins install /absolute/path/to/clean-staging/.agents
/plugins reload
/skill:webdev-agent-kit:project-context-adapter
```

Kimi copies the entire source directory into its managed plugin directory,
including unrelated files. Never install from a working project's `.agents`:
it can contain private facts, databases, attachments and local modifications.
Use only a clean release payload. Reinstall from a new clean payload for upgrades.
Project facts and memory belong under the current host's `.agents/project/` and
`.agents/learning/`, never the managed plugin copy.

When migrating from project mode, back up the installation and reconcile vendor
skills/roles with the release manifest using the upgrade workflow. Retire only
verified vendor runtime copies and the managed startup pointer; preserve custom
skills, instructions, project facts and learning state. Do not delete `.agents`.
Check discovery after migration: local roles can shadow plugin updates and local
skills can coexist with namespaced plugin skills.

Both modes include nine native `wdk-*` roles with bounded tools and no nested
subagents. Roles inherit Kimi's model configuration; a configured secondary-model
pool controls subagent selection. Names such as light/deep do not switch models.
Preserve user model/permission choices. K3 needs account availability; this package
does not provision credentials or models. Verify a real handoff before claiming
that delegation works.

## MCP and client setup checklist

WebDev does not require every server below. Native Kimi file and shell tools are
sufficient for source work. For frontend work, add documentation access and one
working browser route when rendered verification is required. Reuse existing
connections; installing WebDev does not install or authorize these integrations.

### MCP servers by task

| Server | When to configure it | Setup and acceptance |
| --- | --- | --- |
| [Context7](https://context7.com/docs/installation) | Recommended for current React, Next.js and dependency documentation; official web docs remain a fallback | HTTP endpoint `https://mcp.context7.com/mcp`; complete the provider's authentication. Resolve a library used by the project and retrieve documentation for its installed version. |
| [Playwright MCP](https://playwright.dev/mcp/installation) | Browser checks when not using a working Kimi native browser route | Local stdio server, Node.js 20+ and a browser runtime. Open the local app, perform one scoped interaction and capture a screenshot. Package/browser downloads may be needed at first use. |
| [GitHub MCP](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md) | Repository metadata, issues and PR workflows when no suitable authenticated connector or CLI exists | HTTP endpoint `https://api.githubcopilot.com/mcp/`; configure supported authentication and repository access. Verify by reading the intended repository or PR before any requested write. |
| [Figma MCP](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/) | Reading an actual Figma design source | Remote endpoint `https://mcp.figma.com/mcp`, subject to Figma's supported-client catalog, account access and authentication. Confirm Kimi client eligibility first; do not assume that using Kimi inside VS Code grants it another extension's access. If unavailable, use supplied exports or an approved browser inspection route. |

No extra filesystem MCP is needed when Kimi's native file tools work. A visual
comparison service is optional; screenshot inspection remains available without
one. Langfuse monitoring and local learning capture are separate opt-in features,
not prerequisites for coding or browser QA; see the
[monitoring setup](../../skills/project-onboarding-adapter/references/langfuse-installation.md)
and the capture section below.

### Where to configure MCP

In **Kimi Code CLI**, use `/mcp-config` to add a server and `/mcp` to inspect its
status. Configuration is project-scoped in `.kimi-code/mcp.json`, or user-scoped
in `$KIMI_CODE_HOME/mcp.json` (default `~/.kimi-code/mcp.json`). A project entry
with the same name overrides the user entry. Merge entries; preserve existing
servers. Review project commands/URLs before trusting the workspace.

In **Kimi for VS Code**, open Kimi's gear menu → **MCP Servers**. The documented
presets include Context7, Playwright and GitHub. Use the connection test and
authorization controls; configuring another VS Code agent's MCP does not prove
that Kimi sees the server.

Example CLI configuration for Context7 and the optional Playwright route:

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp"
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

Remove the Playwright entry if using another browser route. This example contains
no credentials: complete OAuth with `/mcp-config login SERVER_NAME` when the
server supports it, or configure its documented token outside committed files.
Kimi supports `bearerTokenEnvVar` for bearer tokens. On Windows, ensure Node/npm
are on the PATH of the process launching Kimi; restart after changing PATH.
Create a new session after adding servers, then verify actual callable tools.

Sources: [Kimi MCP configuration](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/mcp.html)
and [Kimi for VS Code setup](https://www.kimi.com/code/docs/en/kimi-code-for-vscode/customization.html).

### Choose the browser or desktop route

These Kimi features are distinct from installing a generic MCP server. Pick the
route that can reach the target app; do not enable all routes by default.

| Route | Enable or configure | Use it for |
| --- | --- | --- |
| Kimi Code Desktop built-in browser | Open a Browser tab in the right panel; start the app and use the actual URL/port printed by its dev server | Local page interaction, screenshots and responsive checks. No separate Playwright MCP is required if the native tools work. |
| Kimi Browser Extension / WebBridge | Install the official plugin through `/plugins` → Official, or Desktop Settings → Plugins; also install the Chrome or Edge extension, then start a new session | Your real browser and its existing signed-in sessions. Confirm the intended browser is connected. |
| Playwright MCP | Configure the server above and verify its browser starts | A separate browser automation route for CLI or VS Code. Its session need not share your normal browser's login state. |
| Kimi Computer Use | Install the official platform plugin and complete its OS setup | Desktop application interactions when the task requires them; not a prerequisite for ordinary web development. |

On **macOS**, Computer Use needs Accessibility and Screen Recording permissions
and the Kimi Code switch under Connect local agents, followed by a restart.
On **Windows**, the documented installation command is:

```text
/plugins install https://cdn.kimi.com/kimi-computer-use-windows/latest/kimi-cu-win-plugin.zip
```

Restart Kimi afterwards. Windows requires an interactive x64 desktop on Windows
10 1903+ or Windows 11. Actions may temporarily take over the mouse and keyboard;
the target app and controller need matching privilege levels. Normal web QA does
not require running either as administrator.

Sources: [built-in browser](https://www.kimi.com/code/docs/en/kimi-code-desktop/built-in-browser.html),
[official browser and computer plugins](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/plugins.html),
and [Desktop settings](https://www.kimi.com/code/docs/en/kimi-code-desktop/settings-and-extensions.html).

### Additional Kimi settings and verification

1. Authenticate Kimi and select an available model with tool use; screenshot
   analysis also requires image input support. Use `/model` in CLI or Desktop
   Model Providers. Do not enable an unsupported model capability just by editing
   a flag.
2. Keep normal permission prompts and workspace trust. WebDev does not require
   YOLO mode, global trust bypasses or blanket MCP approval. Enable only the tools
   needed for the task. No experimental tool-loading switch is required.
3. Keep subagents on the inherited model, or deliberately configure an existing
   alias through `/secondary-model`. Model selection does not grant browser
   tools. Current packaged `wdk-*` roles have bounded file/shell allowlists;
   perform browser QA in the main session unless a role's access was separately
   configured and verified. The learning evaluator deliberately has no tools.
4. Verify documentation retrieval and one browser scenario in a fresh session:
   open the real local URL, inspect the page, exercise a reversible interaction,
   check the visible result, and capture desktop/mobile evidence when relevant.
   For Computer Use, separately verify one harmless action in the intended app.
5. Record the client surface, provider, configuration scope, observed checks and
   unavailable capabilities in host-local `.agents/project/client-profile.md`
   and `.agents/project/mcp-profile.md`. Configuration alone is not a passed check.

These steps document setup; they do not certify the current WebDev Kimi
integration. Native browser routing and delegated browser access still need live
acceptance. Source-only checks must not be reported as rendered QA.

Model settings: [Kimi configuration](https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files.html).

## Optional experience capture

From the project root, replace `SKILL` below with the absolute installed path to
`skills/agent-self-improvement` (the managed plugin copy when using plugin mode).
Python 3.11 or newer is required for the TOML installer.

```sh
python SKILL/scripts/install_kimi_hooks.py --project .
python SKILL/scripts/install_kimi_hooks.py --project . --approve
python SKILL/scripts/learning.py on --project .
```

Installation preserves existing configuration, writes a backup on changes and
filters the global hooks to this exact project. Use `--config PATH` for an
explicit Kimi config. Restart the Kimi session after hook changes. To disable
recording run `learning.py off --project .`; to remove these project's hooks
run `install_kimi_hooks.py --project . --remove --approve`.
Use TOML array-of-table declarations for hooks for existing nonempty hook arrays; inline arrays must
be converted manually. On Windows use paths without shell metacharacters
(`&`, `%`, `!`, parentheses and similar characters). Ordinary spaces are supported.
Capture includes text prompt parts, successful tool output and failed tool errors.
Image/binary prompt parts are excluded. Kimi truncates successful tool output at
2000 characters; boundary-sized output is marked potentially truncated. Current
Stop events contain no final assistant text and are marked missing. Transcripts
and attachment bytes are not read automatically.

## Proposals and evaluation

After reviewing a project-memory run and its diagnosis:

```sh
python SKILL/scripts/learning_cycle.py propose --run RUN_ID --project . --repo . --engine kimi --kimi-model MODEL_ALIAS
python SKILL/scripts/learning_benchmark.py --repo . --proposal PROPOSAL --cases CASES --engine kimi --kimi-model MODEL_ALIAS
```

Use an already installed and authenticated Kimi Code v2. No model credentials
are created by the Kit. Select an alias shown by Kimi `/model`; if omitted,
`config.toml`'s `default_model` is used, which can differ from a TUI session's
selection. Both A/B arms pass the same alias explicitly and reject configuration
changes during evaluation. Recorded provenance is configured identity, not
provider-observed identity. The evaluator has no tools or subagents and sends only
the supplied text to the selected provider. Visual attachments remain metadata.
Review the proposal, run independent held-out cases and explicitly approve
application through the existing learning workflow. Text assertions do not
replace real coding behavior checks.

## Acceptance before publication

Verify on an authenticated installation: skill and policy discovery, one
read-only subagent, capture on/off and project isolation, a reviewed proposal,
and baseline/candidate evaluation on the same model. Repeat the installer on
Windows with paths containing spaces. Structural checks and synthetic payloads
must never be described as a live Kimi pass.

[Official skill documentation](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)

[All installation guides](README.md)
