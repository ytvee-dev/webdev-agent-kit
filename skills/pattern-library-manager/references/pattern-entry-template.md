---
id: 'agents.skills.pattern-library-manager.references.pattern-entry-template'
title: 'Pattern Entry Template'
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

# Pattern Entry Template

Use this shape for reusable anti-pattern entries.

```md
# Rule Name

## Rule

State the rule in one or two operational sentences.

## Avoid

Show the smallest bad example that demonstrates the risk.

## Prefer

Show the smallest good example that demonstrates the desired pattern.

## Allowed Exception

List concrete exceptions. Avoid broad phrases like "when needed".

## Apply When

Name the workflows or code surfaces where the rule applies.
```

For approved patterns in `common/approved-patterns.md`, keep entries shorter but still include the rule, example, and boundary when the rule is easy to misuse.
