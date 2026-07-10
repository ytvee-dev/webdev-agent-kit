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
    - '[[common/readme-policy|README Read And Edit Policy]]'
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

- Read targeted README sections when relevant under `common/readme-policy.md`.
- Use README claims to locate higher evidence, not as sufficient technical proof.
- Propose documentation updates in the final report.
- Edit an existing README only when the current user request explicitly asks to change that README.
- Edit other documentation only when the user explicitly asks for documentation work and approves the target files or scope.

## Forbidden Behavior

- Do not update host `README.md` because implementation changed.
- Do not treat reading or auditing README as permission to edit it.
- Do not edit `docs/**` as a side effect of code work.
- Do not rewrite onboarding or architecture docs during project adaptation.
- Do not treat documentation cleanup as harmless scope expansion.

## Validation Gates

- Documentation edits require explicit user validation.
- README technical claims must be confirmed through higher evidence when available.
- README/code or README/config drift must be reported instead of silently edited.
- Final reports should state when useful documentation changes were proposed but not applied.
