---
name: architecture-from-spec
description: Use only when the user provides a specification, technical assignment, or large refactor brief and wants planning-only, source-backed React/frontend architecture guidance for the current project or a new React/Next.js project. Produce an implementation-ready plan, not edits. Do not use for ordinary feature/refactor implementation, `.agents` onboarding, or agent-rules authoring.
id: 'agents.skills.architecture-from-spec.skill'
title: 'Architecture From Spec'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'architecture-from-spec'
tags:
    - 'agents/skill-package'
    - 'architecture/spec'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/architecture-from-spec/references/frontend-architecture|Frontend Architecture]]'
    - '[[skills/architecture-from-spec/references/spec-extraction|Spec Extraction]]'
    - '[[skills/webapp-task-protocol/SKILL|Webapp Task Protocol]]'
    - '[[skills/nextjs-app-router/SKILL|Nextjs App Router]]'
    - '[[skills/react-component-workflow/SKILL|React Component Workflow]]'
    - '[[skills/react-state-workflow/SKILL|React State Workflow]]'
    - '[[skills/boundary-input-validation/SKILL|Boundary Input Validation]]'
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Architecture From Spec

## Purpose

Turn a user specification into React/frontend architecture guidance without
guessing missing requirements or starting implementation.

The deliverable of this skill is architecture guidance or an implementation-ready
plan. "Implementation-ready" means ready for a later execution step; this skill
does not initiate edits by itself and it does not replace execution skills.

## When to use

- The user provides a specification, technical assignment, or large refactor
  brief and asks for React/frontend architecture, planning, decomposition,
  decision guidance, or an implementation plan.
- The user wants to choose an architecture path before implementation starts.
- The user needs a structured decision record for routing, state, boundaries,
  validation, security, styling, or verification.

## When not to use

- Normal feature, bugfix, or refactor implementation in the current repo. Use
  `webapp-task-protocol` and the relevant execution skills.
- Prompts that ask to implement a Next.js or React feature now, even when they
  mention architecture. Route those through `webapp-task-protocol`; use this
  skill only if the user asks for a plan first.
- Project adaptation, `.agents` onboarding, or project-context initialization.
  Use `project-onboarding-adapter`.
- Agent rules, skill authoring, `AGENTS.md`, or `.agents` policy work. Use
  `agent-rules-skill-author`.
- Narrow execution design questions that are already resolved by the repo's
  existing architecture and only need implementation.

## Required context

1. Read `AGENTS.md`.
2. Read `.agents/project/stack-profile.md` and the relevant framework path index
   when the request targets the current repo.
3. Extract explicit requirements, constraints, non-goals, and unknowns from the
   user specification.
4. Use official docs or configured docs MCP only when the recommendation depends
   on current React, Next.js, tooling, deployment, or external API behavior.
5. Read `references/spec-extraction.md` before locking the architecture shape.
6. Read `references/frontend-architecture.md` before presenting the final
   recommendation.

## Workflow

1. Confirm that the requested deliverable is architecture guidance or an
   implementation-ready plan, not immediate edits.
2. Separate mandatory requirements from preferences and unknowns.
3. Inspect the current repo when the work targets an existing project.
4. Use official docs and primary sources to verify architecture-sensitive advice.
5. Read `references/frontend-architecture.md` for React-specific decision
   points.
6. Propose one recommended architecture path that fits the stated constraints.
7. Offer bounded alternatives only when they materially change tradeoffs.
8. Ask the user whenever a missing requirement would change the architecture.
9. Stop after the guidance deliverable. Hand off later edits to execution skills
   only when the user explicitly asks for implementation.

## Output contract

The response should provide:

- one recommended architecture path
- bounded alternatives only when they change real tradeoffs
- unresolved questions that materially change the decision
- verification and risk implications for the proposed architecture
- explicit non-goals or deferred execution details that belong to later
  implementation skills
- execution handoff notes naming the skills that should own later route,
  component, state, validation, security, styling, or verification work

## Core rules

- Do not invent missing architecture constraints.
- Do not start implementation from this skill alone unless the user later asks
  for execution through the appropriate execution skill chain.
- Do not force a single rigid folder structure when the user wants flexibility.
- Keep rationale source-backed and current.
- Distinguish clearly between required-by-spec decisions and recommended
  best-practice decisions.
- Keep execution ownership explicit: route actual repo changes later through
  `webapp-task-protocol`, `nextjs-app-router`, `react-component-workflow`,
  `react-state-workflow`, and related implementation skills.
- Cover routing boundaries, state ownership, component boundaries, validation,
  security, styling/design-system impact, and verification when they affect the
  architecture.

## Reference map

- `references/spec-extraction.md`
- `references/frontend-architecture.md`
