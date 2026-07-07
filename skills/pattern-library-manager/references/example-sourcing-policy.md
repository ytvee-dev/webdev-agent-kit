---
id: 'agents.skills.pattern-library-manager.references.example-sourcing-policy'
title: 'Example Sourcing Policy'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'pattern-library-manager'
tags:
    - 'agents/skill-package'
    - 'agents/reference'
    - 'agents/patterns'
parent:
    - '[[skills/pattern-library-manager/SKILL|Pattern Library Manager]]'
related: []
depends_on:
    - '[[skills/pattern-library-manager/SKILL|Pattern Library Manager]]'
---

# Example Sourcing Policy

## Preferred Sources

Use examples in this order:

1. User-provided examples approved for reusable documentation.
2. Existing reusable bundle examples.
3. Official documentation or trusted maintainer sources used only to understand the pattern.
4. Short original examples written by the agent and proposed for user approval when the example shape matters.

## Rules

- Do not copy long third-party code into the bundle.
- Do not copy private host-project code into publishable common rules.
- Do not invent project-specific paths, types, or domain names as if they were reusable facts.
- Keep examples short and focused on one rule.
- Use neutral sample names unless the user approved a domain-specific example for reusable docs.

## Approval

Ask the user to approve examples before committing them when:

- the example comes from private project code;
- the example is based on external material;
- the rule is subjective and the example defines the practical boundary;
- the example introduces a new reusable style convention.

## Report

Final reports must say whether examples were supplied by the user, adapted from official understanding, or written as original examples.
