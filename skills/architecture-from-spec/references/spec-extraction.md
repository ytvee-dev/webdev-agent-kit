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

- Extract explicit requirements first.
- Separate hard constraints from preferences.
- Note missing decisions that would change architecture, such as deployment
  model, data ownership, auth, theming, or package policy.
- Ask the user instead of guessing whenever a missing constraint would change
  the recommendation.
