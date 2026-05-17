---
name: architecture-from-spec
description: Use when the user provides a specification, technical assignment, or large refactor brief and wants source-backed React or Next.js architecture guidance for the current project or a new project. Extract requirements first, then propose one recommended architecture path plus bounded alternatives without inventing missing constraints.
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
    - '[[skills/architecture-from-spec/references/source-map|Source Map]]'
    - '[[skills/architecture-from-spec/references/spec-extraction|Spec Extraction]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Architecture From Spec

## Purpose

Turn a user specification into source-backed architecture guidance without
guessing missing requirements.

## Required context

1. Read `AGENTS.md`.
2. Read `.agents/project/stack-profile.md` and the relevant framework path index
   when the request targets the current repo.
3. Extract explicit requirements, constraints, non-goals, and unknowns from the
   user specification.
4. Use official or primary-source documentation when architecture guidance
   depends on current framework behavior.

## Workflow

1. Separate mandatory requirements from preferences and unknowns.
2. Inspect the current repo when the work targets an existing project.
3. Use official docs and primary sources to verify architecture-sensitive advice.
4. Propose one recommended architecture path that fits the stated constraints.
5. Offer bounded alternatives only when they materially change tradeoffs.
6. Ask the user whenever a missing requirement would change the architecture.

## Core rules

- Do not invent missing architecture constraints.
- Do not force a single rigid folder structure when the user wants flexibility.
- Keep rationale source-backed and current.
- Distinguish clearly between required-by-spec decisions and recommended
  best-practice decisions.

## Reference map

- `references/spec-extraction.md`
- `references/source-map.md`
