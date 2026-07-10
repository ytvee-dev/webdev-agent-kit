---
id: 'agents.agents'
title: 'AGENTS.md'
doc_type: 'policy'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/policy'
    - 'docs/entrypoint'
parent: []
related:
    - '[[common/runtime-policy-index|Runtime Policy Index]]'
    - '[[common/core/runtime-core-policy|Portable Runtime Core Policy]]'
    - '[[common/policy-precedence|Policy Precedence]]'
    - '[[common/readme-policy|README Read And Edit Policy]]'
    - '[[common/test-policy|Test Change And Verification Policy]]'
    - '[[common/tool-capability-model|Tool Capability Model]]'
    - '[[profiles/react-typescript/PROFILE|React TypeScript Profile]]'
depends_on: []
---

# WebDev Agent Kit Runtime Policy

## Purpose

This is the compact runtime entrypoint for the `.agents` bundle. It routes work to client-neutral core policy, an evidence-gated profile, verified project facts, and the smallest matching skill. Detailed rules stay in their owning `common/**` or skill reference and are loaded only when relevant.

Bundle paths are rooted at `.agents`. Generated `dist/**` output is never source truth. The host-root instruction pointer is managed only by `project-onboarding-adapter` with explicit approval; ordinary bundle work must not replace it.

## Precedence And Approvals

Resolve conflicts through `common/policy-precedence.md`: system, client security, and sandbox restrictions; current user request; confirmed scope and approvals; host-project instructions; verified `project/**` facts; selected skill; active profile; generic defaults.

Require explicit approval before installing packages or tools, changing configuration outside scope, adding test infrastructure, replacing project instructions, performing irreversible actions, or contacting external people or systems. New tests require an explicit current request; relevant existing-test maintenance follows `common/test-policy.md`.

`README.md` may be read only when relevant under `common/readme-policy.md`, never as sole technical evidence or runtime authority. Reading never authorizes editing. Do not create or change an existing README unless the current user explicitly requests that README change.

## Context Loading And Workflow Scale

Classify before reading broadly:

- `Fast Lookup`: narrow question, file location, or code explanation; search and read only decisive snippets.
- `Lightweight Workflow`: one obvious, low-risk local change; avoid planning and toolchain overhead.
- `Standard Workflow`: multi-file work, unclear root cause, refactor boundary, or bounded verification.
- `Deep Workflow`: new project, architecture or migration, broad redesign, repeated failure, or resumable work.

Load in this order, stopping when the next safe action is clear:

1. `common/core/runtime-core-policy.md`.
2. The matching `adapters/**` file only when client behavior affects the task.
3. `profiles/react-typescript/PROFILE.md` only when repository evidence activates it; otherwise use `common/skill-applicability-policy.md` and local conventions.
4. Verified project instructions and only the affected `project/**` facts.
5. The smallest matching `skills/**/SKILL.md` and only references it requires for the active slice.

Do not load every skill, reference, common rule, overlay, README, or generated target for routing. Use `common/prompt-intent-routing-rules.md` only when workflow weight is unclear. Tool needs come from `tool-capabilities-manifest.json`; a callable native tool may satisfy them, and provider names or config do not prove availability.

## Skill Discovery

Select skills from their `name` and `description`; the user need not name one. Full triggers, exclusions, workflow, and validation gates remain in each `SKILL.md`. Do not insert planning, design, MCP, loop, review, or onboarding skills into a lightweight task unless its scope actually escalates.

## Compact Skill Index

- Plan: `goal-planner` defines outcomes; `execution-plan-manager` slices work; `loop-workflow-planner` governs bounded iteration.
- Design: `design-screenshot-spec` converts supplied visual evidence; `frontend-design-intelligence` grounds product patterns; `frontend-design-director` sets visual direction.
- Build: `frontend-architecture-planner` defines ownership; `greenfield-project-builder` plans a first vertical slice; `frontend-layout-implementer` implements an approved spec in its target stack.
- Quality: `frontend-bugfix-debugger` fixes evidence-first defects; `frontend-refactor-surgeon` preserves behavior; `frontend-linter-manager` runs or repairs scoped lint; `frontend-visual-qa` checks rendered evidence; `frontend-quality-reviewer` performs independent review.
- Context and tooling: `project-onboarding-adapter` initializes pointers and local facts; `project-context-adapter` refreshes them; `mcp-toolchain-manager` maps tool capabilities; `pattern-library-manager` maintains reusable patterns; `agent-rules-skill-author` maintains this bundle.

## Change Boundaries

Preserve unrelated user work. Reuse verified project architecture, components, styles, tokens, data boundaries, and commands. Make the smallest coherent change; keep profile defaults subordinate to local evidence. Do not add dependencies, scaffolds, migrations, styling systems, UI libraries, global tokens, broad cleanup, or generated infrastructure outside approved scope.

Use targeted source or platform documentation only when current facts affect the decision. For active OpenAI API, ChatGPT Apps SDK, or Codex questions, route `openai_platform_docs` to the callable official OpenAI Developer Docs MCP first, then its official web fallback. Skip that lookup for generic frontend or local repository facts. Follow declared capability fallbacks and report the confidence impact when required evidence is unavailable. Keep durable host facts local in `project/**`.

## Verification And Output

Run the smallest relevant existing check for the changed surface. Bound retries, change strategy after a failed approach, and never claim a check, tool, screenshot, or result without evidence. Report exact blocked checks when no honest fallback exists.

Apply `common/token-economy-rules.md`. Return only facts that affect understanding, confidence, or the next action. For changed work, default to `Changed`, `Verified`, and `Blocked` when applicable; lightweight final answers stay within 180 words. Omit request echo, skill names, workflow narration, empty sections, raw logs, and irrelevant skipped-work notes; never hide errors, unknowns, blocked verification, or approval needs.
