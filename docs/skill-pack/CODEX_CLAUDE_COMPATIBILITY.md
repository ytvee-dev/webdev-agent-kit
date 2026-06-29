# Codex And Claude Compatibility Plan

Status: draft architecture plan addendum.
Scope: make future WebDev Assistant skills portable across OpenAI Codex and Anthropic Claude Code without weakening the original architecture.

## Compatibility Finding

The current bundle is Codex-first and `.agents`-first.

Evidence:

- Skills use `SKILL.md` with `name` and `description`, which is the shared core shape used by both Codex-style and Claude-style skills.
- Existing skills also include bundle graph metadata in `SKILL.md` frontmatter.
- Existing skills include Codex-specific `agents/openai.yaml` files.
- Existing authoring rules already distinguish `.agents`-compatible authoring from stricter portable OpenAI authoring.
- There is no dedicated Claude package manifest, Claude validation workflow, or Claude-specific distribution target yet.

Conclusion:

```text
The skill content is partially portable, but the package is not yet guaranteed to be equally compatible with Codex and Claude Code as a distributed skill pack.
```

## Compatibility Goal

WebDev Assistant should support two targets:

```text
Codex target
Claude Code target
```

Both targets must preserve the original concept:

```text
goal-aware frontend engineering
prompt intent routing
project memory
MCP/tooling discipline
official-doc source hierarchy
design intelligence
small-slice execution
verification
AI-slop filtering
```

The compatibility layer must not add UI component library skills or testing skills.

## Portable Skill Core

Every reusable skill should have a portable core that can be read by both agents.

Portable core requirements:

```text
SKILL.md
- YAML frontmatter with at least `name` and `description`
- concise trigger-oriented description
- plain Markdown workflow instructions
- relative links to references only when needed
- no host-project facts
- no agent-specific command assumptions in the main workflow
```

Recommended portable sections:

```text
Purpose
When To Use
When Not To Use
Required Context
Tool Contract
Workflow
Output Contract
Validation Gates
Trigger Evals
Reference Map
```

## Platform-Specific Metadata

Do not overload the portable core with platform-specific metadata.

### Codex Metadata

Codex-specific metadata belongs in:

```text
agents/openai.yaml
```

Use it for:

- display name;
- short description;
- default prompt;
- implicit invocation policy;
- MCP/tool dependencies.

### Claude Metadata

Claude compatibility needs an explicit target plan. Until a Claude-specific metadata convention is finalized for this repository, Claude-specific packaging must not be guessed inside production skills.

Future work must decide and document:

```text
- whether Claude uses the same source skill directories directly;
- whether a generated `dist/claude/**` package is needed;
- whether Claude-specific tool permissions or plugin metadata are needed;
- how Claude should handle Codex-only `agents/openai.yaml` files;
- which validation command or manual checklist proves Claude compatibility.
```

## Frontmatter Policy

The current bundle stores graph metadata inside `SKILL.md` frontmatter. That is useful for the `.agents` documentation graph but may reduce portability if another agent expects a narrower frontmatter contract.

Future compatibility work must choose one of two approaches:

### Option A: Single Source With Tolerated Extra Metadata

Keep current `SKILL.md` frontmatter with:

```text
name
description
graph metadata
```

Use this only if both target agents are validated to ignore unsupported frontmatter keys safely.

### Option B: Source + Generated Portable Builds

Keep rich source files for `.agents`, then generate clean portable distributions:

```text
dist/codex/skills/**
dist/claude/skills/**
```

Generated portable `SKILL.md` files should include only target-supported frontmatter and target-supported paths.

Preferred plan:

```text
Option B is safer for public distribution.
```

## Directory Strategy

Source of truth:

```text
.skills source or .agents/skills source
common/**
templates/**
references/**
```

Generated targets:

```text
dist/codex/**
dist/claude/**
```

Rules:

- never copy `project/**` into a distribution target;
- never include local-only overlays;
- never include host-project facts;
- keep target-specific metadata in target-specific locations;
- keep shared instruction content identical unless a target requires formatting changes.

## Compatibility Validation

Add future validation scripts:

```text
scripts/validate_codex_skill_pack.py
scripts/validate_claude_skill_pack.py
scripts/build_skill_targets.py
```

Validation must check:

```text
- every skill has `name` and `description`;
- descriptions are trigger-oriented and concise;
- portable `SKILL.md` files do not contain unsupported target metadata;
- Codex packages contain valid `agents/openai.yaml` when needed;
- Claude packages do not rely on Codex-only metadata;
- referenced files exist in the target package;
- `project/**` is absent from target packages;
- no non-English reusable instructions are present;
- hard exclusions remain enforced: no UI component library skills, no testing skills.
```

## Required Plan Changes

Add a compatibility phase before plugin packaging.

Suggested phase:

```text
Phase 8.5: Cross-Agent Compatibility Packaging
```

Goals:

```text
- define the portable skill core contract;
- define Codex target packaging;
- define Claude Code target packaging;
- decide whether to use single-source skills or generated `dist/**` targets;
- add compatibility validation scripts;
- update skill authoring rules so every new skill is checked against both targets;
- document which files are shared and which are platform-specific.
```

Candidate files:

```text
common/cross-agent-compatibility-rules.md
common/portable-skill-core-contract.md
scripts/build_skill_targets.py
scripts/validate_codex_skill_pack.py
scripts/validate_claude_skill_pack.py
dist/codex/**
dist/claude/**
```

Validation:

```text
- Codex target validates with Codex rules.
- Claude target validates with Claude rules or documented manual checklist.
- No target includes `project/**`.
- Target packages preserve prompt intent routing.
- Target packages preserve MCP/tooling policy without assuming unavailable tools.
- Target packages preserve hard exclusions for UI libraries and testing skills.
```

## Skill Authoring Rule Update

Future `agent-rules-skill-author` work must add this requirement:

```text
Before a skill is considered complete, verify that it can be emitted for both Codex and Claude targets or record why it is intentionally target-specific.
```

New skills must avoid:

```text
- Codex-only assumptions in shared workflow text;
- Claude-only assumptions in shared workflow text;
- tool names that exist only in one agent without a fallback;
- platform-specific install commands in portable core instructions;
- graph-only metadata as the only source of routing truth.
```

## Compatibility Work Order

Recommended order:

```text
1. Add cross-agent compatibility rules.
2. Define portable skill core contract.
3. Audit existing skills for shared vs Codex-only assumptions.
4. Decide single-source vs generated `dist/**` packaging.
5. Add Codex validation.
6. Add Claude validation or manual checklist.
7. Update `agent-rules-skill-author` so future skills are created with both targets in mind.
8. Only then package the public release.
```
