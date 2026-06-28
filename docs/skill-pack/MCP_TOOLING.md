# MCP And Tooling Architecture

Status: draft architecture.
Scope: tool selection, MCP dependencies, safe installation workflow, and tool usage policy for future WebDev Assistant skills.

## Purpose

The skill pack must use tools deliberately. Tools and MCP servers are not decoration. They are selected only when they unlock the current workflow, reduce guessing, improve verification, or provide authoritative documentation.

## Core Principles

- Use available tools before guessing.
- Do not install tools without explicit user approval.
- Verify official installation sources before installing MCP servers.
- Record installed, missing, blocked, and skipped tools in project memory.
- Use only the tools required for the selected slice.
- Prefer rendered evidence for UI work.
- Keep humans in the loop for operations that mutate systems, install software, or access sensitive data.

## Tool Categories

### Core Tools

These tools form the expected baseline for the future skill pack.

```text
filesystem_server
```

Purpose:

- read and edit project files;
- inspect `.agents/**`;
- inspect source files;
- maintain project overlays;
- manage templates and progress files.

```text
playwright
```

Purpose:

- open local frontend apps;
- inspect runtime and console errors;
- capture rendered screenshots;
- verify desktop, tablet, and mobile viewports;
- exercise interactions and states;
- support visual QA evidence.

```text
context7
```

Purpose:

- fetch current framework, library, CLI, and tooling documentation;
- resolve framework-specific implementation questions;
- reduce stale best-practice assumptions.

```text
mdn
```

Purpose:

- check HTML, CSS, Web APIs, browser behavior, compatibility, and accessibility-adjacent platform facts.

```text
openaiDeveloperDocs
```

Purpose:

- verify current Codex skills, plugins, AGENTS.md, MCP integration, and agent workflow behavior.

### Optional Tools

Optional tools are activated only when a task requires them.

```text
github
```

Use for:

- repository and PR context;
- issue triage;
- PR review;
- CI metadata when available;
- publishing branches when explicitly requested.

```text
figma
```

Use only when:

- live Figma workflow is explicitly requested;
- the server is already available or approved for installation;
- the task requires design-tool access;
- the user understands that live design-tool access is being used.

Default design intake should still support screenshots, exported assets, copied inspect values, and written specs.

```text
browser/devtools
```

Use for:

- runtime debugging beyond Playwright;
- inspecting computed styles;
- network issues;
- CSS specificity diagnosis.

```text
visual-diff
```

Use for:

- comparing implementation screenshots against references;
- measuring visual drift;
- recording evidence for visual QA.

```text
design-reference
```

Use for:

- managing supplied design screenshots;
- referencing assets;
- retrieving accepted visual baselines.

```text
linear/jira
```

Use only when project planning, tickets, or acceptance criteria live in external issue trackers.

```text
docs/search
```

Use only when project-specific internal documentation is connected and relevant.

## Skill Dependency Policy

Each skill should declare expected tools in `agents/openai.yaml` when the dependency improves invocation or user experience.

Example:

```yaml
interface:
  display_name: "Frontend Visual QA"
  short_description: "Verify rendered frontend UI"
  default_prompt: "Use $frontend-visual-qa to verify rendered UI against the requested goal and visual references."

policy:
  allow_implicit_invocation: true

dependencies:
  tools:
    - type: "mcp"
      value: "playwright"
      description: "Open local apps, inspect console errors, capture screenshots, and test viewports."
    - type: "mcp"
      value: "mdn"
      description: "Check current HTML, CSS, accessibility, and browser behavior."
```

## MCP Toolchain Manager

Future skill:

```text
mcp-toolchain-manager
```

Purpose:

```text
Detect required tools, compare them with available tools, verify official installation sources, request approval before installation, validate installed tools, and record the toolchain state.
```

## Toolchain Workflow

```text
1. Detect
   Inspect available MCP servers and local tooling.

2. Need
   Determine which tools are required for the selected skill and current slice.

3. Justify
   Explain what workflow each missing tool unlocks.

4. Verify Source
   Locate and record the official installation source.

5. Ask Approval
   Request explicit user approval before installation or configuration changes.

6. Install
   Install only the approved tools.

7. Validate
   Confirm the tool is callable and works for the expected workflow.

8. Record
   Update `project/mcp-profile.md`.

9. Use Minimally
   Invoke only the tool calls needed for the current slice.
```

## Project MCP Profile

Target file:

```text
project/mcp-profile.md
```

Required sections:

```text
Required For Skill Pack
Required For Current Task
Available
Missing
Optional
Approved For Install
Installed
Skipped
Blocked
Official Install Sources
Validation Results
Last Updated
```

Example entry:

```text
Tool: playwright
Status: available | missing | approved | installed | blocked
Required By: frontend-visual-qa
Reason: rendered browser verification and screenshots
Official Source: <official source URL>
Install Approved: yes | no | not requested
Validation: pass | fail | not tested
```

## Official Source Requirement

Before installing a tool or MCP server, the agent must identify the official installation source.

Accepted sources:

- official project documentation;
- official package repository;
- official vendor documentation;
- trusted repository owned by the tool maintainer.

Rejected sources:

- random blog snippets;
- unverified package names;
- package install commands from search result summaries;
- unofficial forks;
- outdated copy-paste commands;
- generated guesses.

## Human-In-The-Loop Policy

MCP tools can be model-controlled. The skill pack must preserve human oversight for sensitive operations.

Require approval before:

- tool installation;
- configuration changes;
- filesystem destructive operations;
- package installation;
- production access;
- writing to external services;
- reading secret-bearing files;
- opening live design tools when not already approved.

## Tool Use By Skill

### `project-onboarding-adapter`

Required:

```text
filesystem_server
context7
mdn
openaiDeveloperDocs
```

Optional:

```text
github
playwright
```

### `greenfield-project-builder`

Required:

```text
filesystem_server
context7
mdn
openaiDeveloperDocs
```

Optional:

```text
playwright
github
```

### `frontend-design-director`

Required:

```text
filesystem_server
mdn
context7
```

Optional:

```text
playwright
figma
visual-diff
design-reference
```

### `design-screenshot-spec`

Required:

```text
filesystem_server
```

Optional:

```text
design-reference
visual-diff
figma
```

### `frontend-layout-implementer`

Required:

```text
filesystem_server
context7
mdn
```

Optional:

```text
playwright
visual-diff
```

### `frontend-architecture-planner`

Required:

```text
filesystem_server
context7
mdn
```

Optional:

```text
github
openaiDeveloperDocs
```

### `frontend-bugfix-debugger`

Required:

```text
filesystem_server
context7
mdn
```

Optional:

```text
playwright
browser/devtools
github
```

### `frontend-refactor-surgeon`

Required:

```text
filesystem_server
context7
```

Optional:

```text
playwright
github
```

### `frontend-visual-qa`

Required:

```text
playwright
filesystem_server
mdn
```

Optional:

```text
visual-diff
browser/devtools
design-reference
```

### `frontend-quality-reviewer`

Required:

```text
filesystem_server
context7
mdn
```

Optional:

```text
playwright
visual-diff
github
```

## Fallback Policy

If a required tool is missing:

1. Report the missing capability.
2. Explain impact on confidence.
3. Offer installation only after official source verification.
4. Use a fallback only when the selected skill allows it.
5. Mark output confidence accordingly.

Examples:

```text
Playwright missing -> visual QA can only be manual/static and must not claim rendered verification.
MDN missing -> web platform claims must be based on local knowledge or deferred.
context7 missing -> framework-specific claims must be checked against local project code or official docs by another available route.
```

## Tool Slop Rules

Do not:

- install every recommended MCP server;
- use live Figma when screenshots are sufficient;
- start browser verification for documentation-only work;
- read GitHub PR metadata for a local-only component task;
- use web/docs lookup for stable facts already present in project overlays;
- hide missing tool limitations;
- claim a tool-based check ran when it did not.

## Validation Gate

After tool setup or changes:

```text
- project/mcp-profile.md is updated.
- each required tool is marked available, missing, skipped, blocked, or approved.
- official source is recorded for every proposed installation.
- no tool was installed without explicit approval.
- selected skills declare accurate tool dependencies.
```
