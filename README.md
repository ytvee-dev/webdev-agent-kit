<p align="center">
  <img src="https://res.cloudinary.com/duyqvi0ig/image/upload/v1783949530/webdev-agent-kit-badge_ei4113.png" alt="WebDev Agent Kit" width="900">
</p>

<h1 align="center">WebDev Agent Kit</h1>

<p align="center">
  Rules and skills for frontend work in Codex, Claude Code, and Cursor.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Skills-23-0ea5e9?style=flat-square" alt="Skills: 23">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache--2.0-blue?style=flat-square" alt="License: Apache-2.0"></a>
</p>

WebDev Agent Kit gives your coding agent instructions for working with an existing
project: where to look, how to plan a change, what to preserve, and what to check.
You keep using your usual client and model. The Kit is a collection of instructions
and helper scripts, not a separate coding app.

## Contents

- [What it does](#what-it-does)
- [Install](#install)
- [Choose models and tools](#choose-models-and-tools)
- [Adapt it to your project](#adapt-it-to-your-project)
- [Check the setup](#check-the-setup)
- [Project context and memory](#project-context-and-memory)
- [Subagents](#subagents)
- [Example requests](#example-requests)
- [Skills](#skills)
- [Repository layout](#repository-layout)
- [Checks for maintainers](#checks-for-maintainers)
- [Support and license](#support-and-license)

## What it does

The Kit tells the agent to:

- follow the project's existing architecture, components and styles;
- keep a small fix small;
- check source code and configuration before making assumptions;
- ask before installing dependencies or doing work outside your request;
- run checks relevant to the change and report failures or checks it could not run.

Its stack-specific rules cover React, Next.js, TypeScript and CSS Modules, plus
Redux, TanStack and Axios when the project already uses them. Planning, code
review and screenshot analysis can also apply to other stacks.

These instructions help define expected behavior. They cannot guarantee that a
model will follow every rule or produce correct code.

## Install

Choose the guide for your client. Download links in the guides point to the
latest **published** release; an open release PR may contain newer changes.

| Client | How it is installed | Guide |
| --- | --- | --- |
| Codex | Files in the project's `.agents/` directory | [Codex](docs/install/codex.md) |
| Claude Code | Plugin installed through a local marketplace | [Claude Code](docs/install/claude-code.md) |
| Cursor | `.agents/` directory and a Cursor rule | [Cursor](docs/install/cursor.md) |
| VS Code — Codex | Same package layout as Codex | [VS Code Codex](docs/install/vscode-codex.md) |
| VS Code — Claude | Same plugin as Claude Code | [VS Code Claude](docs/install/vscode-claude.md) |
| OpenCode on Windows | Installer using the Codex bundle and a recorder plugin | [OpenCode](docs/install/opencode.md) |

Each release provides `SHA256SUMS` so you can check downloaded files. For an
existing installation, follow [upgrade and rollback](docs/install/upgrade.md)
to preserve project context, settings and local changes.

Installation recordings are available in the [Cursor](docs/install/cursor.md)
and [VS Code Codex](docs/install/vscode-codex.md) guides.

## Choose models and tools

The [model and capability guide](docs/install/model-capability-guide.md) compares
starting choices from OpenAI, Anthropic and Google. It explains what you need for
MCP, hooks, browser control, Computer Use, search, image analysis and subagents.

A model and its tools are separate choices. A model that understands screenshots
still needs a client that can take screenshots and perform actions. Installing
the Kit does not install or enable those tools.

For common integrations, see the [MCP setup guide](docs/mcp/README.md). MCP
(Model Context Protocol) lets an agent use tools provided by another service.
You do not need an MCP server when your client already provides the required tool.

## Adapt it to your project

For Codex or Cursor, open the project root and send:

```text
Adapt this .agents kit to my project and create AGENTS.md in the root.
Preserve existing project instructions, settings, caches and saved experience.
```

For Claude Code, use the [plugin adaptation guide](docs/install/claude-agents.md).

During adaptation, the agent checks the stack, project paths, styles, commands
and available tools. It saves those facts in `.agents/project/` for future tasks.
If existing project instructions need to be merged, it shows the proposed change.
Adaptation does not create application code or install libraries and MCP servers.

You can also select a [frontend or designer role](docs/install/roles.md) for the
conversation. This changes the task focus; it does not select a model.

Full Codex adaptation includes setup of missing local subagent roles when the
client supports them. To exclude that step, say:

```text
Update project facts only. Do not change model configuration.
```

Experience recording is a separate choice. Adaptation preserves an existing
opt-in or opt-out and asks if the choice is unknown. Adding a sync repository
does not, by itself, enable recording. See [project context and memory](#project-context-and-memory).

## Check the setup

Ask:

```text
Verify the WebDev Agent Kit installation without changing it.
Report the client, Kit version, project stack, loaded skills and available tools.
For hooks and subagents, distinguish configured settings from an observed run.
List anything you could not verify.
```

A file on disk or a green connection indicator does not prove that a tool works.
The agent should say which checks it actually ran. For example, without a
browser it can review source code, but cannot confirm how the page renders.

## Project context and memory

The Kit stores two kinds of information locally:

- **Project context:** paths, conventions, commands and tool settings in
  `.agents/project/`. This helps the agent find relevant files in later tasks.
- **Experience records:** optional saved task context, findings, corrections and
  proposed lessons. Records belong to a project and do not change model weights.

To refresh project context after changes, ask:

```text
Update the project context after these changes.
```

Cached facts must be checked against current code when they become outdated.
They can reduce repeated searches; the Kit does not promise a fixed token saving.

Experience capture is off by default. Hooks are client event handlers that record
prompts, tool results and responses when capture is enabled. Installing them,
enabling recording and approving them in the client are separate steps. Actual
events are needed to confirm that recording works.

During adaptation, you can provide a private GitHub repository for manual exchange
of structured records. Full conversations and attachments are not uploaded by
that exchange. Sync happens only when requested. See the
[recording setup](skills/agent-self-improvement/assets/integrations/INTEGRATIONS.md)
and [project memory reference](skills/agent-self-improvement/references/project-memory.md)
for details.

## Subagents

Subagents handle a specific part of a task, such as a file lookup or code review.
Small tasks can stay with the main agent.

Claude Code includes nine roles for lookup, implementation, debugging,
architecture and review. They inherit your selected model unless you configure
supported overrides. See [Claude roles](docs/install/claude-agents.md).

Codex adaptation selects role models from those available in your client and
preserves existing working settings. Writing a role file is only setup; a real
invocation confirms whether the client loads it and uses the expected model.
See [Codex model routing](docs/install/gpt-model-routing.md).

## Example requests

**Small edit:** “Center the Retry button below the error text.” The agent should
make the local change and check the affected files.

**Bugfix:** “The dashboard is blank on mobile. Reproduce the problem and fix it.”
See [bugfix, refactor and review examples](examples/bugfix-refactor-review.md).

**Build from a screenshot:** “Implement this pricing page in the existing app.
Match the supplied desktop and mobile screenshots.” See the
[screenshot example](examples/screenshot-to-frontend.md).

**Report a Kit problem:** “Create an issue in the WebDev repository for this bug.”
The agent checks for duplicates and prepares a report with relevant context and
verification results. It needs an authenticated GitHub tool to publish the issue.

## Skills

The release candidate contains 23 skills. These are the main groups:

| Task | Skills |
| --- | --- |
| Set up or update the Kit | `project-onboarding-adapter`, `webdev-kit-updater` |
| Keep project context current | `project-context-adapter`, `pattern-library-manager` |
| Plan work | `goal-planner`, `execution-plan-manager`, `loop-workflow-planner` |
| Understand and explore a design | `design-screenshot-spec`, `frontend-design-intelligence`, `frontend-design-director`, `frontend-prototype-explorer` |
| Build an interface | `frontend-architecture-planner`, `greenfield-project-builder`, `frontend-layout-implementer` |
| Fix or refactor code | `frontend-bugfix-debugger`, `frontend-refactor-surgeon` |
| Check code and UI | `frontend-linter-manager`, `frontend-visual-qa`, `frontend-quality-reviewer` |
| Configure tools | `mcp-toolchain-manager` |
| Maintain Kit instructions | `agent-rules-skill-author` |
| Save experience or report feedback | `agent-self-improvement`, `webdev-feedback` |

The [design-system pilot](docs/architecture/design-system-pilot.md) is an optional
experiment for comparing components and tokens in a real project. It does not
automatically synchronize Figma and code.

## Repository layout

| Path | Contents |
| --- | --- |
| `AGENTS.md`, `common/` | Shared agent instructions |
| `profiles/`, `adapters/` | Stack and client differences |
| `skills/` | Task instructions and helper scripts |
| `agents/claude-code/` | Claude subagent definitions |
| `templates/` | Reusable plans and project records |
| `schemas/`, `evals/` | Data formats and evaluation cases |
| `scripts/` | Validation, build and release tools |
| `docs/` | User and maintainer guides |

`bundle-manifest.json` defines package contents. Build output goes to `dist/`.
Project-specific facts stay in the installed project's `.agents/project/` and
are not included in shared release packages.

## Checks for maintainers

```bash
python scripts/validate_skill_pack.py
```

This runs the source, package and archive checks. CI also runs Markdown, YAML
and Python lint. See [Maintenance](MAINTENANCE.md) for checks by change type.

## Support and license

Start with the [documentation index](docs/README.md) or [support guide](SUPPORT.md).
The project owner manages development and releases. Plans are in the
[roadmap](ROADMAP.md); private vulnerability reporting is in [Security](SECURITY.md).

Licensed under [Apache-2.0](LICENSE).
