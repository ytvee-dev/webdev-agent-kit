---
id: "agents.skills.frontend-quality-reviewer.references.review-handoffs"
title: "Exact Review Handoffs"
doc_type: "skill-reference"
layer: "skill"
status: "active"
publishable: true
local_only: false
tags: []
parent:
  - "[[skills/frontend-quality-reviewer/SKILL]]"
related:
  - "[[common/independent-review-rules]]"
  - "[[common/subagent-handoff-rules]]"
depends_on: []
---

# Exact Review Handoffs

Load only for delegated reviews of durable work or material repair loops.
Use the canonical plan's criteria, a self-contained task brief and evidence
report under `common/subagent-handoff-rules.md`. Compact inline review needs no
artifact ceremony.

## Capture The Actual Surface

Record the task BASE before implementation, not `HEAD~1`: a task may span several
commits. When Python 3.11+ and Git already exist, from the host root run:

```sh
python .agents/skills/frontend-quality-reviewer/scripts/review_package.py \
  --root . --plan .agents/project/active-plan.md --base RECORDED_BASE --head HEAD
```

The helper returns an artifact path and SHA-256; pass that reference, not the
whole diff, to the reviewer. It writes only git-ignored local run storage and
never commits, runs tests, invokes models, or marks criteria complete. No ignored
storage means blocked packaging; request a scoped ignore change rather than
leaking evidence into source control. Placeholder revisions must be replaced.

For uncommitted work, add `--worktree` and explicit repeatable `--path` arguments
for the owned files/directories. This captures staged, unstaged and untracked
changes, including deletions, with file hashes. Committed capture deliberately
excludes working changes. Select the mode honestly; committed-only evidence
cannot clear an uncommitted fix. Paths must be literal repository-relative paths.
The helper rejects unsafe paths, reversed ranges, nonregular untracked files,
concurrent changes detected during capture, and oversized packages.

Without the helper use existing native tools to save the exact range/diff and
snapshot metadata to a unique local file. Do not install tools or require a
commit merely to obtain evidence. Inspect relevant surrounding code when the
snapshot alone cannot establish a requirement. A diff is not test evidence.

## Two Judgments, Not Mandatory Duplicate Reviewers

An applicable review records both criterion compliance and changed-code quality
in one pass. A separate role name is not context isolation. Do not rerun an
unchanged expensive check solely for ceremony; inspect its matching evidence.
Rerun when its state/environment changed, evidence is missing, or a concrete
counterexample needs reproduction within approved scope.

After a repair, pass the prior findings, repaired diff and updated evidence.
Judge each existing finding addressed/not-addressed; inspect new breakage caused
by the repair. Reopen surrounding scope only for a demonstrated dependency,
shared interface, security or user-outcome risk and state why. Unrelated style
preferences do not extend the loop. For committed fixes use the previously
reviewed HEAD as the new BASE. For uncommitted fixes retain the earlier package
and compare snapshots; do not mislabel the full accumulated diff as fix-only.

Keep `F-###`, `AC-###`, and `S-###` identities unchanged. Apply the existing shared
retry limit. A failed required criterion remains failed/blocked at the cap;
a documented optional deferral is not permission to report full acceptance.
