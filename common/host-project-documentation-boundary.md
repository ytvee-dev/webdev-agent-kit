---
id: 'agents.common.host-project-documentation-boundary'
title: 'Host Project Documentation Boundary'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/policy'
parent:
    - '[[common/anti-patterns|Common Anti-Patterns]]'
related:
    - '[[common/documentation-maintenance|Documentation Maintenance]]'
depends_on: []
---

# Host Project Documentation Boundary

Purpose: prevent ordinary agent work from silently expanding into host-project documentation edits.

## Rule

During normal product, code, onboarding, context refresh, bugfix, refactor, visual QA, or review work, do not edit the host project's documentation files.

Host-project documentation includes:

- host root `README.md`;
- `docs/**`;
- architecture decision records;
- onboarding docs;
- product docs;
- deployment docs;
- API docs;
- public changelogs;
- design docs;
- wiki-exported docs.

## Allowed Behavior

- Propose documentation updates in the final report.
- Edit documentation only when the user explicitly asks for documentation work and approves the target files or scope.
- For this reusable kit's own README, treat it as human-facing documentation and edit it only when the user explicitly asks for public kit documentation work.

## Forbidden Behavior

- Do not update host `README.md` because implementation changed.
- Do not edit `docs/**` as a side effect of code work.
- Do not rewrite onboarding or architecture docs during project adaptation.
- Do not treat documentation cleanup as harmless scope expansion.

## Validation Gates

- Documentation edits require explicit user validation.
- Host documentation must not be used as a source for runtime routing or project facts unless the user specifically provides an excerpt.
- Final reports should state when useful documentation changes were proposed but not applied.
