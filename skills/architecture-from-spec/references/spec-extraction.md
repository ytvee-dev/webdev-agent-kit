---
id: 'agents.skills.architecture-from-spec.references.spec-extraction'
title: 'Spec Extraction'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'architecture-from-spec'
tags:
    - 'agents/skill-package'
    - 'architecture/spec'
    - 'agents/reference'
parent:
    - '[[skills/architecture-from-spec/SKILL|Architecture From Spec]]'
related:
    []
depends_on:
    - '[[skills/architecture-from-spec/SKILL|Architecture From Spec]]'
---

# Spec Extraction

Use this reference to extract architecture-relevant facts from a specification
before recommending a solution.

## Extraction checklist

- Goal and success criteria:
  state the user-visible or developer-visible outcome, acceptance criteria,
  launch threshold, and any quality bar such as performance, accessibility, SEO,
  security, maintainability, or delivery speed.
- Audience and workflow:
  identify primary users, operators, authors, admins, frequency of use, critical
  paths, collaboration needs, and failure or recovery flows that affect state,
  routing, data loading, or permissions.
- Scope and non-goals:
  list required capabilities, explicitly excluded work, deferred phases, and
  places where the spec intentionally avoids product or implementation detail.
- Hard constraints:
  framework, hosting, team policy, packages, deadlines, auth, performance,
  compliance, browser support, accessibility, internationalization, design
  system, migration, data residency, or platform constraints.
- Unknowns that materially change architecture:
  deployment model, data ownership, integration boundaries, multi-tenant needs,
  theming, permissions, offline support, or scale assumptions
- Repo facts versus user preferences:
  separate what already exists in the current codebase from what the user is
  merely open to changing
- Boundary inputs:
  identify route params, search params, forms, uploaded files, external APIs,
  persisted content, cookies, local storage, and public entry points that require
  validation in the later execution plan.
- Execution ownership:
  mark which future work belongs to routing, component composition, shared
  state, validation, security, styling, project-context refresh, or verification
  skills.

## Rules

- Extract explicit requirements first.
- Separate hard constraints from preferences.
- Label extracted facts as `spec says`, `repo says`, `user preference`,
  `assumption`, or `unknown`.
- Mark assumptions explicitly instead of letting them disappear into the
  recommendation.
- Ask the user instead of guessing whenever a missing constraint would change
  the recommendation.
