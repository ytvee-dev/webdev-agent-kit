---
id: 'agents.common.prompt-intent-routing-rules'
title: 'Prompt Intent Routing Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/policy'
    - 'routing/task-scale'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/lightweight-routing-policy|Lightweight Routing Policy]]'
    - '[[AGENTS|Canonical Agent Policy]]'
    - '[[common/approved-patterns|Approved Patterns]]'
    - '[[common/anti-patterns|Common Anti-Patterns]]'
depends_on: []
---

# Prompt Intent Routing Rules

Purpose: choose the right workflow weight before selecting a skill chain.

## Core Rule

Do not apply the same workflow weight to every user prompt. Classify the prompt intent and task scale before invoking planning, checkpointing, project memory updates, MCP installation checks, deep project scans, or architecture workflows.

Start with the cheapest path that can answer the user. Escalate only when targeted evidence proves that a heavier workflow is needed.

A narrow lookup must stay fast. A narrow bugfix must stay lightweight. A large ambiguous request must be planned before implementation.

## Workflow Levels

Use the canonical task classification and skill map in `AGENTS.md`, then choose the lightest safe workflow:

| Level | Use when | Process boundary |
| --- | --- | --- |
| Fast Lookup | Narrow lookup or explanation with no requested change | Read the lookup policy, search narrowly, answer, stop |
| Lightweight Workflow | One clear bug, type error, styling adjustment, local refactor, or isolated edit | Inspect the affected owner, change directly, run the smallest relevant check |
| Standard Workflow | Multi-file work, unclear root cause, screenshot/spec implementation, or measurable retry | Use compact goal/slicing only when it improves execution; add the selected task skill |
| Deep Workflow | New project, architecture or stack migration, broad redesign, repeated failures, or resumable work | Define durable goal, plan, context budget, checkpoints, and approval gates |

## Escalation

Escalate only when targeted evidence shows one of these conditions:

- the apparent fix crosses unrelated owners or public boundaries;
- the root cause remains unclear after focused inspection;
- routing, architecture, state ownership, data flow, security, build behavior, or shared styling changes materially;
- verification disproves the current scope or requires bounded retry;
- the work needs multiple independently verifiable slices or durable stop/resume state;
- a new dependency, tool, framework, testing infrastructure, or broader approval is required.

## De-Escalation

De-escalate when a broad prompt resolves to one concrete surface. Do not create goals, plans, MCP audits, memory files, visual QA, or independent review solely because the wording sounds important.

Examples:

- locating a notification renderer is Fast Lookup;
- changing one button token is Lightweight;
- implementing a supplied screen across several owners is Standard;
- migrating the routing or styling architecture is Deep.

## Validation Gates

Before selecting Standard or Deep, confirm that Fast Lookup or Lightweight cannot safely complete the request.

Before finishing:

- keep reads and writes within the selected scope;
- create durable project artifacts only for genuinely resumable work;
- run the smallest relevant project verification;
- report escalation, skipped checks, or blockers honestly.
