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

- [Who It Is For](#who-it-is-for)
- [What Changes After Installation](#what-changes-after-installation)
- [Supported Clients](#supported-clients)
- [Quick Start](#quick-start)
- [Verifying the Installation](#verifying-the-installation)
- [Practical Scenarios](#practical-scenarios)
- [Core Skills](#core-skills)
- [Architecture](#architecture)
- [Project Validation](#project-validation)
- [Contributing](#contributing)
- [README Boundary](#readme-boundary)
- [License](#license)

## Who It Is For

WebDev Agent Kit is an open-source set of local rules. You continue using the
familiar Codex, Claude Code, or Cursor, while connecting them to a shared
standard for working with projects.

WebDev Agent Kit is intended for frontend developers and teams that use AI
coding agents in React and Next.js projects and want to:

- preserve the existing architecture and local conventions;
- keep small tasks small;
- avoid broad rewrites and unapproved dependencies;
- receive verification proportional to the change;
- use the same baseline rules across different coding agents;
- see real results and blockers instead of confident assumptions.

The stack profile supports React, Next.js, TypeScript, and the existing CSS
Modules, Redux, TanStack, and Axios in the project. General planning, review,
visual verification, and tooling workflows may apply more broadly, but the kit
does not transfer React rules to another stack by analogy.

## What Changes After Installation

The agent receives a local decision-making system that:

- classifies the task and selects the smallest applicable workflow;
- reads only the context required for the next safe action;
- prefers facts from source files, configuration, and CI over general advice;
- requests permission before installing packages, changing infrastructure, or
  taking other actions outside the task;
- performs the smallest meaningful verification of the changed surface;
- separates related failures from existing ones and honestly reports unavailable
  checks.

The kit does not guarantee error-free model behavior. It makes the expected
behavior, boundaries, and result verification explicit and auditable.

## Supported Clients

Download the package for your client from the latest GitHub Release:

| Client | Contract | Download |
| --- | --- | --- |
| Codex | Project bundle | [Codex package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-codex.tar.gz) |
| Claude Code | Native plugin | [Claude Code package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-claude-code.tar.gz) |
| Cursor | Project bundle + native rule | [Cursor package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-cursor.tar.gz) |
| VS Code — Codex | Codex contract alias | [VS Code Codex package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-vs-code-codex.tar.gz) |
| VS Code — Claude | Claude Code contract alias | [VS Code Claude package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-vs-code-claude.tar.gz) |

For each archive, the same release includes a checksum in `SHA256SUMS`. The
stable and versioned names of one target contain identical bytes.

## Quick Start

Detailed installation instructions will be provided as videos:

- [Codex — installation video coming soon](docs/install/codex.md)
- [Claude Code — installation video coming soon](docs/install/claude-code.md)
- [Cursor — installation video coming soon](docs/install/cursor.md)
- [VS Code Codex — installation video coming soon](docs/install/vscode-codex.md)
- [VS Code Claude — installation video coming soon](docs/install/vscode-claude.md)

The consolidated installation index is available in
[Installation Guides](docs/install/README.md).

## Verifying the Installation

Use this read-only smoke prompt:

```text
Verify the WebDev Agent Kit installation.
Do not change the source code.
Show the detected client, stack, available capabilities,
local rules, and unavailable checks.
```

The response should contain facts about the detected target, confirmed stack,
available tool capabilities, local overlays, and verification constraints. A
missing tool must be reported as unavailable rather than presented as
successfully used.

## Practical Scenarios

### Small CSS Change

The kit directs the agent to make a local change and verify the affected
surface. A decorative change should not automatically trigger an architecture
plan, full build, development server, and browser QA.

### Fixing a Frontend Bug

The workflow first requires gathering evidence and forming one testable
hypothesis, then fixing the smallest root cause and separating related failures
from existing ones. An example request is available in
[bugfix-refactor-review.md](examples/bugfix-refactor-review.md).

### Building an Interface from Screenshots

Screenshots and inspect notes are first converted into an implementation spec.
The kit then applies visual direction, architecture, implementation, lint,
rendered visual QA, and review only where they are actually needed. The full
pipeline is shown in
[screenshot-to-frontend.md](examples/screenshot-to-frontend.md).

## Core Skills

The bundle includes a client-neutral runtime core, an evidence-gated
React/TypeScript profile, thin client adapters, and 19 task skills.

| Task | Primary workflow |
| --- | --- |
| Adapt the kit to a project | `project-onboarding-adapter` |
| Refresh local context | `project-context-adapter` |
| Define a goal and plan | `goal-planner`, `execution-plan-manager` |
| Plan a bounded loop | `loop-workflow-planner` |
| Convert screenshots into a spec | `design-screenshot-spec` |
| Establish visual direction | `frontend-design-intelligence`, `frontend-design-director` |
| Design and implement UI | `frontend-architecture-planner`, `frontend-layout-implementer` |
| Fix a defect | `frontend-bugfix-debugger` |
| Perform a safe refactor | `frontend-refactor-surgeon` |
| Check lint and UI | `frontend-linter-manager`, `frontend-visual-qa` |
| Conduct an independent review | `frontend-quality-reviewer` |
| Manage the capability model | `mcp-toolchain-manager` |
| Evolve the bundle itself | `agent-rules-skill-author` |

The tool model is based on capabilities, not provider names. A skill may require
`project_files`, `current_library_docs`, `rendered_visual_evidence`, or another
capability; it may be provided by an MCP server, native tool, connector, or
approved fallback. The presence of a package or configuration does not prove
that a tool is available.

## Architecture

```text
AGENTS.md                         compact runtime entrypoint
common/core/                     portable client-neutral core
profiles/react-typescript/       evidence-gated stack defaults
adapters/                        Codex, Claude Code, and Cursor differences
skills/                          19 task workflows
templates/                       goal, plan, loop, and project contracts
schemas/                         machine-readable source contracts
evals/                           static behavior fixtures
scripts/                         validation, packaging, and release tooling
docs/                            human-facing guides
```

`bundle-manifest.json` is the machine-readable source of target contracts.
Generated `dist/**` is build output, not source truth. Project-local facts are
stored in `.agents/project/**` in the installed project and are not published in
the reusable bundle.

## Project Validation

Primary commands:

```bash
python scripts/validate_source_bundle.py
python scripts/check_readme_boundary.py
python scripts/check_links.py
python scripts/validate_install_guides.py
python scripts/validate_skill_pack.py
```

CI separately checks Markdown, YAML, Python, schemas, graph links, tool
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

Before opening a pull request, run the checks relevant to the changed layer and
provide the exact commands and results. Changes to the runtime core, scripts,
packaging, and approval boundaries require stricter review than documentation
fixes and examples.

## README Boundary

This README is a user-facing guide. It is not runtime policy, routing input,
source truth for the skill inventory or target layout, or project context for
agents. Runtime rules live in `AGENTS.md`, `common/**`, `skills/**`,
`templates/**`, and local `project/**` overlays.

Agents may read the relevant README sections when the task concerns project
intent, installation, onboarding, an audit, or documentation drift. README is
not sufficient technical proof. Runtime results, source code, configuration,
CI, package scripts, and lockfiles have higher priority.

Reading does not authorize editing. An existing README must not be edited unless
the current user explicitly requests that README change. Authorized edits must
remain user-facing documentation, and their technical claims must be verified
against stronger evidence. The full contract is documented in the
[README read and edit policy](common/readme-policy.md).

## License

WebDev Agent Kit is distributed under the Apache-2.0 license. See
[LICENSE](LICENSE).
