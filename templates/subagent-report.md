---
id: "agents.templates.subagent-report"
title: "Subagent Evidence Report"
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

# Subagent Evidence Report

Use only for an authorized durable delegation. Write the full evidence locally;
return its path, status and a short verification/concern summary.

```text
Task packet path and hash:
Status: done | done-with-concerns | needs-context | blocked
Changed paths and base/head or working-tree snapshot:
AC IDs: observed result, evidence path, passed/failed/blocked:
Checks: command, exit status, covered state, evidence location:
Unrun or unavailable checks:
Attempts used and remaining shared budget:
Required concerns versus optional observations:
Exact missing fact or blocker, when present:
```

Append repair evidence referencing the original task and finding IDs. Do not
redefine criteria or report independent review of your own implementation.
A check that failed to import/collect is not proof its behavior assertion ran.
