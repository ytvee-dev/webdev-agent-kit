---
id: 'agents.common.tool-capability-model'
title: 'Tool Capability Model'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'agents/tooling'
    - 'mcp/capabilities'
parent:
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
related:
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
depends_on: []
---

# Tool Capability Model

Purpose: define tool requirements by capability before naming a specific MCP server, host connector, native file tool, or command-line fallback.

## Capability First

A skill declares the capability it needs. The host client satisfies that capability through one of the available providers.

Use this vocabulary in runtime rules, toolchain reports, and `project/mcp-profile.md`:

- `project_files` - read and, when approved, write project files.
- `current_library_docs` - fetch current React, Next.js, Redux, TanStack, Axios, TypeScript, package-manager, or build-tool documentation.
- `web_platform_docs` - fetch current HTML, CSS, Web API, accessibility, and browser compatibility documentation.
- `rendered_visual_evidence` - open a local app, inspect rendered UI, resize viewports, capture screenshots, and report browser-visible state.
- `codex_platform_docs` - fetch current Codex, AGENTS.md, skills, plugin, MCP, sandbox, or config documentation.
- `client_platform_docs` - fetch current Claude Code, Cursor, VS Code, or other host-client documentation when adaptation depends on client behavior.
- `repo_metadata` - inspect repository, PR, issue, review, label, release, and CI metadata.
- `design_reference_files` - read user-supplied screenshots, exported assets, copied inspect values, and local visual references.
- `live_design_source` - inspect live design-tool files. This capability is blocked for the default screenshot-only bundle flow.

## Provider Mapping

Map each capability to providers in this order:

1. Configured MCP server or native host tool already available in the current agent session.
2. Existing host connector or native client capability.
3. Targeted shell fallback only when the fallback is allowed by the current task and policy.
4. Blocked, with explicit confidence impact, when no honest fallback exists.

Do not treat a provider name as proof that the capability is available. Availability means the tool is callable in the current session or is recorded as validated in local-only project facts.

## Required Report Shape

When a capability affects the task, report:

```text
Capability:
Needed by:
Preferred provider:
Available provider:
Status: available | missing | blocked | fallback-used | unknown
Fallback:
Confidence impact:
Approval needed:
Validation:
```

## Rules

- Do not require a specific MCP server when the client already provides an equivalent native capability.
- Do not claim tool-based verification from a package dependency, lockfile entry, running local server, or config file alone.
- Do not install or configure tools to satisfy a capability without explicit user approval and a verified official source.
- Do not use Figma or live design-tool providers as fallback for this bundle's screenshot-only design flow.
- Keep durable host-client and MCP facts in `project/mcp-profile.md`, not in reusable bundle rules.
