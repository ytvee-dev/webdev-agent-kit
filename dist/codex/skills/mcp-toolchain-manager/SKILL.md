---
name: mcp-toolchain-manager
description: Use when frontend work needs MCP/tool capability detection, missing-tool reporting, official install source verification, approval-gated installation planning, or project/mcp-profile.md updates. Do not install tools, run package installs, or change configs without explicit user approval.
---

# MCP Toolchain Manager

## Purpose

Detect, explain, validate, and record MCP/tool capabilities needed by WebDev Assistant skills without turning tool setup into automatic or unsafe behavior.

This skill exists to keep MCP usage deliberate. It identifies which tools are required for the current workflow, which tools are already available, which tools are missing, what each missing tool unlocks, and what official source must be verified before installation is proposed.

## When To Use

Use this skill when:

- a selected skill declares MCP/tool dependencies;
- a task requires rendered UI verification, official documentation lookup, project context retrieval, visual references, GitHub metadata, or another external capability;
- the agent needs to audit available vs missing MCP servers;
- the user asks what MCP/tools are required for the skill pack;
- the user asks to install, configure, validate, or troubleshoot MCP tools;
- `project/mcp-profile.md` must be created or refreshed;
- a missing tool limitation must be reported before fallback behavior.

Use this skill in `Standard Workflow` or `Deep Workflow` when tool capability affects the current slice.

It may also be used in `Lightweight Workflow` only when the user directly asks about MCP/tool availability or when a missing already-required tool prevents a narrow task from being verified.

## When Not To Use

Do not use this skill just because a task exists.

Do not use this skill for:

- one small bug when no external tool is needed;
- one obvious type error;
- one small styling adjustment that does not require rendered verification;
- documentation-only edits unrelated to MCP/tooling;
- generic planning that does not depend on tool capabilities.

Do not install tools from this skill unless the user explicitly approved that installation in the current task context and the official source was verified.

Do not use this skill to implement frontend code, write tests, scaffold projects, create UI library setups, or access production systems.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when workflow level is unclear.
3. Read selected skill metadata and `agents/openai.yaml` files only for skills relevant to the current task.
4. Read `project/mcp-profile.md` when it exists and the task needs tool state.
5. Read `project/verification-profile.md` only when verification commands influence tool needs.
6. Do not read all skills, all YAML files, or `SUMMARY.md` during normal routing.

## Tool Contract

- May read skill metadata and `agents/openai.yaml` files for selected skills.
- May read or update `project/mcp-profile.md` when durable tool state is needed.
- May search official documentation only to verify installation sources or current tool docs.
- Must not install MCP servers without explicit user approval.
- Must not change Codex, Claude, MCP, shell, package manager, or project configuration without explicit user approval.
- Must not run package installs.
- Must not access production systems or secrets.
- Must not use Figma MCP unless the user explicitly requested a live Figma workflow and that workflow is outside the screenshot-only bundle boundary.

## Core MCP Categories

Expected core capabilities for the future full skill pack:

```text
filesystem_server
playwright
context7
mdn
openaiDeveloperDocs
```

Optional capabilities:

```text
github
figma
browser/devtools
visual-diff
design-reference
linear/jira
docs/search
```

Core does not mean always installed or always used. Use only what the current workflow needs.

## Workflow

1. Identify the active task and selected skill chain.
   - Use prompt intent routing first.
   - Do not expand a lightweight task into tool setup unless the user asked for tool setup or the missing tool blocks verification.

2. Collect required tool declarations.
   - Inspect only `agents/openai.yaml` files for selected skills.
   - Record declared required and optional tools.
   - Do not scan every skill unless onboarding or full toolchain audit is explicitly requested.

3. Determine tool need for the current slice.
   - Required for this slice.
   - Useful but optional.
   - Not needed.
   - Explicitly blocked.

4. Compare with available tools.
   - Available.
   - Missing.
   - Approved for install.
   - Installed.
   - Skipped.
   - Blocked.
   - Unknown.

5. Explain missing capability impact.
   - State what cannot be verified or automated without the tool.
   - State the fallback and confidence level when fallback is allowed.
   - Do not claim tool-based verification if the tool is missing.

6. Verify official install source when installation is relevant.
   Accepted sources:
   - official project documentation;
   - official package repository;
   - official vendor documentation;
   - trusted repository owned by the tool maintainer.

   Rejected sources:
   - random blog snippets;
   - search result summaries;
   - unverified package names;
   - unofficial forks;
   - generated guesses.

7. Ask approval before installation or configuration changes.
   The approval request must name:
   - tool/server name;
   - reason;
   - official source;
   - install/config action;
   - expected validation step;
   - risks or scope.

8. Record toolchain state.
   Update `project/mcp-profile.md` only when durable state is useful for the project.

9. Hand off.
   Return to the selected frontend skill with:
   - tools available now;
   - missing tools;
   - approved fallbacks;
   - verification limits.

## Project MCP Profile Output

When writing or updating `project/mcp-profile.md`, use these sections:

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

Tool entry shape:

```text
Tool
Status
Required By
Reason
Current Task Need
Official Source
Install Approved
Validation
Fallback
Notes
```

## Output Contract

Return a Toolchain Report with:

```text
Task
Workflow Level
Selected Skill Chain
Required Tools
Available Tools
Missing Tools
Optional Tools
Blocked Tools
Official Sources Verified
Approval Needed
Allowed Fallbacks
Confidence Impact
MCP Profile Update
Next Skill Or Next Step
```

## Validation Gates

Before finishing, verify:

- no tool was installed without explicit approval;
- no config was changed without explicit approval;
- no package install was performed;
- official sources are recorded for proposed installations;
- missing tool limitations are explicit;
- fallback confidence is honest;
- `project/mcp-profile.md` was updated only when durable state is useful;
- no UI component library or testing skill was introduced;
- no production systems or secrets were accessed.

## Trigger Evals

Should trigger:

- "Check which MCP servers this skill pack needs."
- "Do we have Playwright MCP available for visual QA?"
- "Set up the MCP tools, but show me the official install sources first."
- "Update project/mcp-profile.md after onboarding."
- "This skill requires context7 and MDN; tell me what is missing."

Should not trigger:

- "Fix this TypeScript error."
- "Change this button color."
- "Implement this component from the already written spec."
- "Write a goal contract."
- "Create an execution plan."

## Reference Map

- `AGENTS.md` - canonical policy, routing, tool rules, and documentation rules.
- `common/prompt-intent-routing-rules.md` - workflow weight selection and escalation/de-escalation rules.
- `project/mcp-profile.md` - optional local-only durable MCP/tool capability cache.
- `project/verification-profile.md` - local verification command facts when tool need depends on project checks.
- `skills/*/agents/openai.yaml` - selected skill tool declarations.
