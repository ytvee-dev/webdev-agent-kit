---
id: 'agents.skills.boundary-input-validation.references.no-new-deps-policy'
title: 'No New Dependencies Policy'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'boundary-input-validation'
tags:
    - 'agents/skill-package'
    - 'frontend/validation'
    - 'agents/reference'
parent:
    - '[[skills/boundary-input-validation/SKILL|Boundary Input Validation]]'
related:
    []
depends_on:
    - '[[skills/boundary-input-validation/SKILL|Boundary Input Validation]]'
---

# No New Dependencies Policy

- Start by checking `package.json`, existing helpers, and existing call sites.
- Prefer built-in language/runtime features and existing repo utilities first.
- If a package truly appears necessary, confirm that it is not already installed
  and request user approval before any install.
- Do not introduce schema validation libraries unless the user explicitly
  approves them.
