---
name: architecture-from-spec
description: Use when the user provides a specification, technical assignment, or large refactor brief and wants source-backed React/frontend architecture guidance for the current project or a new React/Next.js project. Extract requirements first, then propose one recommended architecture path plus bounded alternatives without inventing missing constraints.
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
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Architecture From Spec

## Purpose

Turn a user specification into React/frontend architecture guidance without
guessing missing requirements.

## Required context

1. Read `AGENTS.md`.
2. Read `.agents/project/stack-profile.md` and the relevant framework path index
   when the request targets the current repo.
3. Extract explicit requirements, constraints, non-goals, and unknowns from the
   user specification.
4. Use official docs or configured docs MCP only when the recommendation depends
   on current React, Next.js, tooling, deployment, or external API behavior.

## Workflow

1. Separate mandatory requirements from preferences and unknowns.
2. Inspect the current repo when the work targets an existing project.
3. Use official docs and primary sources to verify architecture-sensitive advice.
4. Read `references/frontend-architecture.md` for React-specific decision
   points.
5. Propose one recommended architecture path that fits the stated constraints.
6. Offer bounded alternatives only when they materially change tradeoffs.
7. Ask the user whenever a missing requirement would change the architecture.

## Core rules

- Do not invent missing architecture constraints.
- Do not force a single rigid folder structure when the user wants flexibility.
- Keep rationale source-backed and current.
- Distinguish clearly between required-by-spec decisions and recommended
  best-practice decisions.
- Cover routing boundaries, state ownership, component boundaries, validation,
  security, styling/design-system impact, and verification when they affect the
  architecture.

## Reference map

- `references/spec-extraction.md`
- `references/frontend-architecture.md`
