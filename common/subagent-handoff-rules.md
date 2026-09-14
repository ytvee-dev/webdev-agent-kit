---
id: "agents.common.subagent-handoff-rules"
title: "Subagent Handoff Rules"
doc_type: "common-rule"
layer: "common"
status: "active"
publishable: true
local_only: false
tags: []
parent:
  - "[[AGENTS]]"
related:
  - "[[common/codex-model-routing-policy]]"
  - "[[common/independent-review-rules]]"
  - "[[templates/subagent-task]]"
  - "[[templates/subagent-report]]"
depends_on: []
---

# Subagent Handoff Rules

Apply only when existing routing and risk rules justify actual delegation.
A small edit stays inline; this rule never mandates agents, plans, or reviews.

## Task Packet

Pass the smallest self-contained assignment, using
`templates/subagent-task.md` when a durable handoff is needed. Preserve the
canonical plan's `S-###` and `AC-###`; include exact global constraints and
interfaces consumed/produced, owned files, decisive evidence, available tools,
verification and the remaining shared attempt budget. Reference the source plan
and its revision/hash. Do not send the full plan or parent transcript by default.
The worker may request a missing fact; it must not invent an interface.

Keep existing canonical planning files. Store briefs, reports and review
packages only in local, git-ignored `project/runs/<plan-id>/`; scope the ID to
the repository/worktree and canonical plan path. Never mix another plan's files.
The review helper derives its namespace from that path. Reuse the returned
namespace for related task artifacts. No automatic migration of older plans.
Use native file tools if a helper is unavailable; do not install a runtime.

## Dispatch And Return

Only the coordinator dispatches; one writer owns each path. Batch independent
same-shape mechanical edits with shared constraints and verification into one
assignment when that reduces overhead. Do not batch unrelated risky interfaces.
Choose an approved adequate role per action, not by skill name or token price.

Use `templates/subagent-report.md` for durable work. The return status is
`done`, `done-with-concerns`, `needs-context`, or `blocked`, with evidence and a
report path. None alone marks an acceptance criterion verified. Missing context
calls for a targeted fact, environment denial for a blocker, and demonstrated
reasoning mismatch for an approved escalation. Neither a new worker nor a new
model resets the retry budget. Reuse a worker for a scoped repair when supported;
otherwise pass its report and open findings to a fresh one.

## Review And Recovery

Pass the brief, report and exact review surface to an actually isolated reviewer
when `common/independent-review-rules.md` requires independence. Include binding
constraints without telling the reviewer which conclusions to reach. Evidence
must match the reviewed revision or working-tree snapshot; a previously green
check is reusable only for the unchanged covered state and environment.

Use `skills/frontend-quality-reviewer/references/review-handoffs.md` for packages
and scoped re-review. Record decisions, unresolved findings, evidence locations
and next action in the canonical progress state before switching tasks. On
resume reconcile that state with Git and actual file hashes; never trust a
checkbox after a rollback. Preserve completion and evidence pointers after
finishing. Do not delete all traces of a run or mark failed criteria verified
because the attempt budget ended.
