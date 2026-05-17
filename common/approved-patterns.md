---
id: 'agents.common.approved-patterns'
title: 'Approved Patterns'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/policy'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[SUMMARY|Agent Documentation Summary]]'
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
depends_on:
    []
---

# Approved Patterns

Purpose: record bundle-wide implementation patterns that are safe to reuse
across multiple host projects.

Use `.agents/project/approved-patterns.md` only for host-repo additions,
exceptions, and concrete local examples.

## Keep host entry files thin

- Keep route files, app entry files, and other top-level composition files thin.
- Move reusable logic into helpers, feature modules, selectors, or shared UI
  modules instead of burying it in entrypoint files.

## Keep interactivity close to the consumer

- Push client-only behavior to the closest component that actually needs it.
- Keep broader shells, layouts, and route composition free of client-only logic
  unless the whole boundary truly depends on it.

## Prefer the nearest established styling system

- Follow the styling system already established in the edited area.
- Reuse existing tokens, variables, and primitives before introducing new local
  values or a new styling stack.

## Keep configuration adjacent to ownership

- Keep reusable copy, links, metadata, route config, and feature config
  adjacent to the component, route, or module that owns them.
- Prefer explicit config objects or neighboring modules over hidden inline
  literals deep inside render logic.

## Trust internal contracts after validation

- Once a value is already guaranteed by types, validated boundaries, or clear
  control flow, use that contract directly.
- Add new guards only at true boundaries or where inspected call paths do not
  actually guarantee the value.
