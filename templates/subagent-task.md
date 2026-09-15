---
id: "agents.templates.subagent-task"
title: "Subagent Task Packet"
doc_type: "template"
layer: "template"
status: "active"
publishable: true
local_only: false
tags: []
parent:
  - "[[common/subagent-handoff-rules]]"
related: []
depends_on: []
---

# Subagent Task Packet

Use only for an authorized durable delegation. Copy to a git-ignored local run
folder, not application source. Fill from the canonical plan; no new criteria.

```text
Plan path and revision/hash:
Repository/worktree identity:
Slice ID and AC IDs (or exact criterion for compact work):
Outcome and explicit non-goals:
Owned paths:
Binding global constraints (exact values):
Consumes / produces (exact interfaces):
Decisive evidence and decision references:
Selected skill and required references:
Available tools and approved executor:
Verification command or observation and expected result:
Remaining shared attempts and escalation boundary:
Report path:
```

An unresolved required field is missing context, not permission to guess. Exact
requirements live here once; the dispatch passes this path and only necessary
cross-slice context. Never include credentials or the parent conversation.
