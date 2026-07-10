---
id: 'agents.common.anti-patterns.no-host-readme-or-docs-edits-without-approval'
title: 'No Host README Or Docs Edits Without Approval'
doc_type: 'anti-pattern-template'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'anti-patterns/docs'
parent:
    - '[[common/anti-patterns/README|Anti-Pattern Templates]]'
related:
    - '[[common/host-project-documentation-boundary|Host Project Documentation Boundary]]'
depends_on: []
---

# No Host README Or Docs Edits Without Approval

## Rule

Do not edit the host project's README or documentation files during normal implementation, bugfix, refactor, onboarding, visual QA, or review work.

## Avoid

- Updating `README.md` because an implementation changed.
- Editing `docs/**` as a side effect of code work.
- Rewriting onboarding or architecture docs during project adaptation.
- Treating documentation cleanup as harmless scope expansion.

## Allowed

- Read targeted README sections when relevant, then confirm technical claims through `common/readme-policy.md`.
- Propose documentation updates in the final report.
- Edit an existing README only when the current user request explicitly asks to change it.
- Edit other documentation only when the user explicitly asks for documentation work and approves the target files or scope.

## Bad

```text
User: Fix the mobile navbar.
Agent: Fixes navbar and updates README usage notes.
```

## Good

```text
User: Fix the mobile navbar.
Agent: Fixes navbar. Final report says: README may need an update if this behavior is documented there; I did not edit it.
```

## Apply When

Use this whenever an agent considers changing host-project documentation while the requested task is not documentation work.
