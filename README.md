<p align="center">
  <img src="https://res.cloudinary.com/duyqvi0ig/image/upload/v1783949530/webdev-agent-kit-badge_ei4113.png" alt="WebDev Agent Kit" width="900">
</p>

<h1 align="center">WebDev Agent Kit</h1>

<p align="center">
  <strong>A cross-platform frontend kit for Codex, Claude Code, and Cursor.</strong><br>
  WebDev Agent Kit helps AI coding agents work predictably and safely with existing frontend projects.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Skills-19-0ea5e9?style=flat-square" alt="Skills: 19">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache--2.0-blue?style=flat-square" alt="License: Apache-2.0"></a>
</p>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Who This Kit Is For](#who-this-kit-is-for)
- [What Changes After Installation](#what-changes-after-installation)
- [Supported Clients](#supported-clients)
- [Quick Start](#quick-start)
- [Adapting the Kit to a Project](#adapting-the-kit-to-a-project)
- [Smart Context Cache and Token Savings](#smart-context-cache-and-token-savings)
- [Verifying the Installation](#verifying-the-installation)
- [Practical Scenarios](#practical-scenarios)
  - [A Small CSS Change](#a-small-css-change)
  - [Fixing a Frontend Bug](#fixing-a-frontend-bug)
  - [Building an Interface from Screenshots](#building-an-interface-from-screenshots)
- [Core Skills](#core-skills)
- [Architecture](#architecture)
- [Project Validation](#project-validation)
- [Contributing](#contributing)
- [License](#license)

## Who This Kit Is For

WebDev Agent Kit is an open-source set of local rules. You continue using your
usual Codex, Claude Code, or Cursor client while connecting it to a shared
standard for working with projects.

WebDev Agent Kit is intended for frontend developers and teams that use AI
coding agents in React and Next.js projects and want to:

- preserve the existing architecture and local conventions;
- keep small tasks small;
- avoid broad rewrites and unapproved dependencies;
- receive verification proportional to the change;
- use the same baseline rules across different coding agents;
- see actual results and blockers instead of confident assumptions.

The stack profile supports React, Next.js, TypeScript, and CSS Modules, Redux,
TanStack, and Axios when they are already used in the project. General planning,
review, visual verification, and tooling workflows can apply more broadly, but
the kit does not transfer React rules to another stack by analogy.

## What Changes After Installation

The agent receives a local decision-making system that:

- classifies the task and selects the minimum necessary workflow;
- reads only the context needed for the next safe action;
- prefers facts from source files, configuration, and CI over general recommendations;
- asks for permission before installing packages, changing infrastructure, or taking other actions outside the task;
- performs the minimum meaningful verification of the changed area;
- separates related failures from existing ones and reports unavailable checks honestly.

The kit does not guarantee error-free model behavior. It makes expected
behavior, boundaries, and result verification explicit and testable.

## Supported Clients

Download the package for your client from the latest GitHub Release:

| Client | Contract | Download |
| --- | --- | --- |
| Codex | Project bundle | [Codex bundle](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-codex.tar.gz) |
| Claude Code | Native plugin via local marketplace | [Claude Code bundle](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-claude-code.tar.gz) |
| Cursor | Project bundle + native rule | [Cursor bundle](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-cursor.tar.gz) |
| VS Code — Codex | Codex contract alias | [VS Code Codex bundle](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-vs-code-codex.tar.gz) |
| VS Code — Claude | Claude Code contract alias | [VS Code Claude bundle](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-vs-code-claude.tar.gz) |

The same release includes a checksum for each archive in `SHA256SUMS`.
The stable and versioned names for the same target contain identical bytes.

## Quick Start

Installation instructions are available for all supported clients:

- [Codex](docs/install/codex.md)
- [Claude Code](docs/install/claude-code.md)
- [Cursor](docs/install/cursor.md)
- [VS Code Codex](docs/install/vscode-codex.md)
- [VS Code Claude Code](docs/install/vscode-claude.md)

Video guides are available only for:

- [Cursor — text and video guide](docs/install/cursor.md)
- [VS Code Codex — text and video guide](docs/install/vscode-codex.md)

All materials are collected in the [documentation index](docs/README.md). The
[installation guide index](docs/install/README.md) and [MCP guide](docs/mcp/README.md)
are also available separately.

## Adapting the Kit to a Project

For Codex and Cursor targets, after installation open the project root in the
coding agent and send this request once:

```text
Adapt this .agents kit to my project and create AGENTS.md in the root
```

Claude Code targets use the native plugin installed through the local
marketplace; the `.agents` adaptation flow in this section applies only to
Codex and Cursor.

The onboarding process detects the active client, project structure, framework,
routes, styling system, verification commands, and available tool capabilities.
It then creates or updates the local `.agents/project/**` profiles and path
indexes for the detected stack, architecture, styles, verification, design
references, client, and tool capabilities.

React and Next.js projects receive stack-specific path indexes. Other frontend
stacks receive a bounded profile that records the detected boundary and keeps
only applicable framework-neutral workflows.

Onboarding keeps the native instruction pointer small and does not overwrite
existing project instructions without permission. It does not create application
source files or automatically install packages, MCP servers, frameworks, or
other tools.

For the best adaptation result:

1. Add the repository-aware prompt from the
   [custom instructions](https://github.com/ytvee-dev/webdev-agent-kit/wiki/Custom-instructions)
   to the personal or user instructions of your coding client. Keep local project
   instructions enabled: the user prompt supplements them and requires the agent
   to discover and follow the repository's own rules.
2. Ask the agent to inspect tool capabilities in the current session and confirm
   recommended MCP servers or equivalent native tools. Configuration alone does
   not prove that a server is available: the capability must be callable or
   previously verified for the project.

Recommended integrations depend on the project and active task:

| Capability | Recommended provider | When it is useful |
| --- | --- | --- |
| Current framework and library documentation | Context7 MCP | Questions about React, Next.js, TypeScript, packages, CLIs, and build tools |
| Visual evidence from the rendered interface | Browser or Playwright MCP | Opening a local application, checking responsive states, and capturing screenshots |
| Next.js runtime diagnostics | Next DevTools MCP | Only for compatible Next.js projects |

The kit continues to work without MCP servers. Native file tools and targeted
shell commands support onboarding, planning, source changes, code review, and
existing lint, typecheck, build, or test commands. Official web documentation
can replace documentation MCPs. Without a callable browser provider, rendered
visual QA, viewport checks, and screenshot evidence are unavailable; the agent
can perform only source review and must report lower confidence. Without Next
DevTools MCP, Next.js runtime verification is unavailable, but normal source and
project-command work remains possible. Missing optional tools should be reported
honestly and skipped or replaced with a fallback, not installed automatically.

Detailed instructions for recommended MCPs and verification prompts are in the
[MCP guide](docs/mcp/README.md).

## Smart Context Cache and Token Savings

The context cache is a set of verified project profiles and path indexes, not a
build cache or model-response cache. Onboarding creates the initial context, and
subsequent tasks consult the relevant overlays before searching the repository
broadly. The agent receives direct paths to known routes, components, styles,
patterns, verification commands, and tool capabilities.

When project facts change, the context workflow updates only the affected
profiles and indexes. For example, after changing routes, components, styles,
verification commands, documentation variants, or tool capabilities, use:

```text
Update the project context after this layout change.
```

Token use is reduced by selecting the minimum necessary workflow, starting from
cached paths, searching narrowly, loading only the relevant skill and required
references, and stopping after enough evidence is available for the next safe
action. Reports remain evidence-based and omit irrelevant logs, repeated output,
and process narration while preserving commands, errors, check results, risks,
and blockers.

For long-running or resumable work, compact summaries preserve the goal,
constraints, acceptance criteria, decisions, affected files and checks, results,
blockers, and the exact next step. Optional loop memory organizes persistent
progress as `Tried`, `Verified`, and `Open`, so another session can continue
without reconstructing the context again.

Cached facts remain local and never override current source files, configuration,
CI, or actual verification results. Stale facts must be updated. The kit does
not promise a fixed token-savings percentage; it reduces waste by avoiding
unnecessary context and repeated repository scans.

## Verifying the Installation

Use this read-only smoke prompt:

```text
Verify the WebDev Agent Kit installation.
Do not change source code.
Show the detected client, stack, available capabilities,
local rules, and unavailable checks.
```

The response should contain facts about the detected target, confirmed stack,
available tool capabilities, local overlays, and verification limits. A missing
tool must be reported as unavailable, not presented as successfully used.

## Practical Scenarios

### A Small CSS Change

The kit directs the agent toward a local change and verification of the affected
area. A decorative change should not automatically trigger an architecture plan,
a full build, a development server, and browser QA.

### Fixing a Frontend Bug

The workflow first requires gathering evidence and stating one testable
hypothesis, then fixing the smallest root cause and separating related failures
from existing ones. An example prompt is in
[bugfix-refactor-review.md](examples/bugfix-refactor-review.md).

### Building an Interface from Screenshots

Screenshots and inspect notes are first converted into an implementation
specification. The kit then applies visual direction, architecture,
implementation, lint, rendered-interface visual QA, and review only where they
are actually needed. The complete workflow is shown in
[screenshot-to-frontend.md](examples/screenshot-to-frontend.md).

## Core Skills

The kit includes a client-neutral runtime core, an evidence-activated
React/TypeScript profile, thin client adapters, and 19 task skills.

| Task | Primary workflow |
| --- | --- |
| Adapt the kit to a project | `project-onboarding-adapter` |
| Update local context | `project-context-adapter` |
| Define a goal and plan | `goal-planner`, `execution-plan-manager` |
| Plan a bounded loop | `loop-workflow-planner` |
| Convert screenshots into a specification | `design-screenshot-spec` |
| Define visual direction | `frontend-design-intelligence`, `frontend-design-director` |
| Design and implement UI | `frontend-architecture-planner`, `frontend-layout-implementer` |
| Fix a defect | `frontend-bugfix-debugger` |
| Perform a safe refactor | `frontend-refactor-surgeon` |
| Verify lint and UI | `frontend-linter-manager`, `frontend-visual-qa` |
| Perform an independent review | `frontend-quality-reviewer` |
| Manage the capability model | `mcp-toolchain-manager` |
| Evolve the kit itself | `agent-rules-skill-author` |

The tool model is based on capabilities, not provider names. A skill can require
`project_files`, `current_library_docs`, `rendered_visual_evidence`, or another
capability; an MCP server, native tool, connector, or approved fallback can
provide it. The presence of a package or configuration does not prove that a
tool is available.

## Architecture

```text
AGENTS.md                         compact runtime entrypoint
common/core/                     portable client-neutral core
profiles/react-typescript/       evidence-activated stack defaults
adapters/                        Codex, Claude Code, and Cursor differences
skills/                          19 task workflows
templates/                       goal, plan, loop, and project contracts
schemas/                         machine-readable source contracts
evals/                           static behavior fixtures
scripts/                         validation, packaging, and release tooling
docs/                            user guides
```

`bundle-manifest.json` is the machine-readable source of truth for target
contracts. Generated `dist/**` is build output, not source truth. Local project
facts live in `.agents/project/**` in the installed project and are not published
in the reusable bundle.

Detailed user documentation starts with the
[main index](docs/README.md), and technical target contracts are described in
the [architecture document](docs/architecture/runtime-target-contracts.md).

## Project Validation

Core commands:

```bash
python scripts/validate_source_bundle.py
python scripts/check_readme_boundary.py
python scripts/check_links.py
python scripts/validate_install_guides.py
python scripts/validate_skill_pack.py
```

CI separately verifies Markdown, YAML, Python, schemas, graph links, tool
capabilities, runtime layers, context budgets, generated targets, and release
archives.

## Contributing

Reproducible cases of incorrect agent behavior, compatibility reports,
negative-trigger evals, documentation improvements, and archive checks in real
projects are especially useful.

- [Contributing Guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Governance](GOVERNANCE.md)
- [Support](SUPPORT.md)
- [Roadmap](ROADMAP.md)
- [Security Policy](SECURITY.md)

Before opening a pull request, run the checks appropriate to the changed layer
and provide the exact commands and results. Changes to the runtime core, scripts,
packaging, and permission boundaries require stricter review than documentation
and example changes.

## License

WebDev Agent Kit is licensed under Apache-2.0. See [LICENSE](LICENSE).
