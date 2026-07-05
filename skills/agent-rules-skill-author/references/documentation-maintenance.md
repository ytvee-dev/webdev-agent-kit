---
id: 'agents.skills.agent-rules-skill-author.references.documentation-maintenance'
title: 'Documentation Maintenance Workflow'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'agent-rules-skill-author'
tags:
    - 'agents/skill-package'
    - 'agents/authoring'
    - 'agents/reference'
parent:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
related:
    []
depends_on:
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
---

# Documentation Maintenance Workflow

Use this workflow when the task changes `.agents/`, a skill package, repo agent policy, or explicit user-facing documentation.

## Layer Boundary

- `AGENTS.md`, `common/**`, `skills/**`, manifests, validators, templates, and examples are agent-maintenance sources.
- `.agents/README.md` is human-facing documentation.
- Keep README edits separate from routing, runtime policy, and skill validation work.

## Workflow

1. Identify the requested documentation change and target layer.
2. Read `AGENTS.md`, the affected source files, and the owning skill or common rule.
3. Update bundle manifests when the skill inventory or published source shape changes.
4. Update graph links after any rename, move, or new reference.
5. Keep host-project facts in `.agents/project/**`.
6. Validate changed skill packages.
7. Search changed docs for stale skill names and prohibited Figma or Jam routing.
8. Report changed files, validation results, and any human-facing README edits separately.
