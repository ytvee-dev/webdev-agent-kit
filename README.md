# WebDev Agent Kit

A project-local operating kit for frontend coding agents.

WebDev Agent Kit helps AI coding agents plan, implement, debug, refactor, review, and visually verify frontend work without broad rewrites, unapproved packages, fake verification, over-testing small tasks, or generic UI output.

Built for frontend projects that use React, Next.js, TypeScript, CSS Modules, Redux, TanStack, and Axios.

## Download

Choose the package for your client from the latest GitHub release:

| Client | Download |
| --- | --- |
| Codex | [Download Codex package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-codex.tar.gz) |
| Claude Code | [Download Claude Code package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-claude-code.tar.gz) |
| Cursor | [Download Cursor package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-cursor.tar.gz) |
| VS Code — Codex | [Download VS Code Codex package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-vs-code-codex.tar.gz) |
| VS Code — Claude | [Download VS Code Claude package](https://github.com/ytvee-dev/webdev-agent-kit/releases/latest/download/webdev-agent-kit-vs-code-claude.tar.gz) |

Checksums are published as `SHA256SUMS` in the same release.

Each runtime archive extracts to a top-level `.agents/` directory.

## What It Is

WebDev Agent Kit is not a UI library, component library, starter template, scaffolder, or test framework. It is a local instruction system that gives coding agents a safer operating model for frontend development.

Use it when you want your coding agent to:

- understand the current frontend project before changing it;
- choose the right workflow for the task;
- keep small tasks small;
- avoid unapproved packages, tooling changes, and broad rewrites;
- use MCP/tools only when their declared capabilities are available;
- verify changes with real evidence and proportional effort;
- preserve project-specific conventions across repeated work.

## README Boundary

This README is a human-facing guide only. It is not runtime policy, not routing context, not skill inventory, and not project context for agents.

Runtime policy lives in:

```text
AGENTS.md
common/**
skills/**
templates/**
project/** local overlays inside installed projects
```

Agents must not read, inspect, cite, route from, or edit a host project's README during runtime work. If the user asks about README content or edits, ask for the relevant excerpt or desired replacement text and propose human-facing copy from that provided material only.

## Quick Start

### 1. Install a client package

Download the matching package above and extract it from the root of your frontend project. The archive creates `.agents/` automatically.

Expected shape after extraction:

```text
your-project/
├── AGENTS.md or CLAUDE.md
└── .agents/
    ├── AGENTS.md
    ├── LICENSE
    ├── common/
    ├── skills/
    ├── templates/
    └── tool-capabilities-manifest.json
```

Runtime archives intentionally exclude human-facing project files such as `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, and `examples/`.

### 2. Add the native root pointer

Codex, VS Code Codex, and Cursor use a small root `AGENTS.md`:

```md
# AGENTS.md

Use the project-local agent policy in `.agents/AGENTS.md`.
```

Claude Code and VS Code Claude use a small root `CLAUDE.md`:

```md
# CLAUDE.md

Use the project-local agent policy in `.agents/AGENTS.md`.
```

Do not duplicate the full `.agents/AGENTS.md` policy into the root pointer.

### 3. Ask the agent to adapt

```text
адаптируйся
```

or:

```text
Adapt this .agents bundle to the current frontend project.
```

Expected onboarding result:

- the agent detects the client and frontend stack;
- creates or refreshes local-only `.agents/project/**` overlays when approved;
- records client facts in `project/client-profile.md`;
- records tool capability facts in `project/mcp-profile.md`;
- does not create app source files;
- does not install packages or MCP servers;
- does not edit host README or docs without explicit documentation approval.

## Installation Guides

Russian draft installation guides are tracked in the repository and can be copied to the GitHub Wiki:

- [Codex](docs/install/ru-codex.md)
- [Claude Code](docs/install/ru-claude-code.md)
- [Cursor](docs/install/ru-cursor.md)
- [VS Code Codex](docs/install/ru-vscode-codex.md)
- [VS Code Claude](docs/install/ru-vscode-claude.md)

## Main Workflows

| User need | Primary skill | Notes |
| --- | --- | --- |
| Adapt the kit to a project | `project-onboarding-adapter` | Creates or refreshes local-only project overlays when approved. |
| Refresh stale project context | `project-context-adapter` | Updates only affected `.agents/project/**` facts. |
| Define a goal before work | `goal-planner` | Standard/deep work only. Not for tiny fixes. |
| Split work into slices | `execution-plan-manager` | Adds context budget, verification per slice, stop/resume state. |
| Plan bounded iteration | `loop-workflow-planner` | Required for measurable retry loops and independent review contracts. |
| Convert screenshots into spec | `design-screenshot-spec` | Screenshot/inspect/assets only. No live Figma workflow. |
| Ground design choices | `frontend-design-intelligence` | Product category, page pattern, design dials, anti-patterns. |
| Define visual direction | `frontend-design-director` | Design Direction Contract before implementation. |
| Plan frontend architecture | `frontend-architecture-planner` | React/Next target-stack architecture decisions. |
| Implement approved UI spec | `frontend-layout-implementer` | React/Next implementation with existing project conventions. |
| Fix frontend defects | `frontend-bugfix-debugger` | Evidence-first, one hypothesis, smallest fix. |
| Refactor safely | `frontend-refactor-surgeon` | Behavior-preserving refactors only. |
| Run lint verification | `frontend-linter-manager` | Uses existing lint command; no setup without approval. |
| Verify rendered UI | `frontend-visual-qa` | Rendered evidence only when visual QA is in scope. |
| Review frontend quality | `frontend-quality-reviewer` | Evidence-backed verdict and severity labels. |
| Manage MCP/tool capability | `mcp-toolchain-manager` | Missing tools, official sources, approval gates. |
| Maintain reusable patterns | `pattern-library-manager` | Adds or tightens approved patterns and anti-patterns with examples. |
| Maintain the kit | `agent-rules-skill-author` | Skills, rules, manifests, validators, and packaging. |
| Plan new frontend project | `greenfield-project-builder` | Deep workflow; approval gates before scaffolding. |

## Tool And MCP Model

The kit is capability-first, not server-name-first.

A skill declares a capability such as:

```text
project_files
current_library_docs
web_platform_docs
rendered_visual_evidence
repo_metadata
```

The current client may satisfy that capability through MCP, native tools, a connector, or a targeted fallback.

Rules:

- use declared MCP/tools when they are available;
- do not pretend a missing tool is available;
- do not infer MCP availability from package files, lockfiles, local dependencies, open ports, or a running app;
- do not install or configure MCP servers without explicit approval and verified official sources;
- report blocked checks and confidence impact when falling back.

## Verification Model

Verification should be proportional to the change.

Small CSS-only background, color, border-color, or decorative mask changes should not trigger full repository lint, typecheck, dev server startup, route discovery, or browser QA by default.

Rendered visual QA is used only when browser evidence is explicitly required, the task is a visual implementation/review, or repeated visual failure justifies escalation.

On Windows, PowerShell `.ps1` package-manager blocks and sandbox access errors must be classified separately from code failures. Agents may use one equivalent `.cmd` fallback or one approved out-of-sandbox attempt when available, then must stop and report blocked verification instead of repeating the same command class.

## Important Anti-Patterns

The bundle blocks common frontend-agent failure modes:

- broad rewrites from narrow requests;
- unnecessary planning for tiny fixes;
- fake verification claims;
- generic SaaS UI defaults;
- unapproved package installation;
- unapproved MCP installation;
- unapproved Figma MCP usage;
- creating or editing component, function, unit, integration, E2E, or visual regression tests by default;
- repeating npm, build, dev-server, browser, Vite, esbuild, SWC, or Playwright commands after the same Windows shell or sandbox blocker;
- moving server communication, domain workflow, or data processing into Redux by default;
- parallel lifecycle booleans instead of one typed status discriminant;
- `useCallback` without a proven identity-sensitive consumer;
- editing host README or docs as implementation scope creep.

## Release Targets

The release workflow builds and publishes stable and versioned artifacts for:

- Codex;
- Claude Code;
- Cursor;
- VS Code Codex;
- VS Code Claude.

Every release artifact extracts to `.agents/` and excludes human-facing docs and examples from the runtime package.

The workflow also keeps legacy `dist/codex` and `dist/claude` generated targets for current validators.

## Maintenance

### Validate the source bundle

```bash
python scripts/validate_source_bundle.py
```

### Validate README boundary

```bash
python scripts/check_readme_boundary.py
```

### Check Markdown links

```bash
python scripts/check_links.py
```

### Build portable targets

```bash
python scripts/build_skill_targets.py
```

### Validate the full skill pack

```bash
python scripts/validate_skill_pack.py
```

### Release

Push the approved next SemVer tag:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

The release workflow builds and publishes the client packages listed in the Download section.

## Contributing

Contributions should keep README, `AGENTS.md`, `bundle-manifest.json`, `.codex-plugin/plugin.json`, skills, references, validators, and release targets aligned.

Do not publish host-project facts from `.agents/project/**` into the reusable bundle.

Do not patch generated `dist/**` output directly. Update source files, then regenerate distribution output through the repository release process.

## License

Apache-2.0. See [LICENSE](LICENSE).
