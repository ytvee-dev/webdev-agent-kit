---
id: 'agents.skills.agent-self-improvement.references.langfuse-evidence'
title: 'Optional Langfuse Evidence'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'agent-self-improvement'
tags:
    - 'agents/skill-package'
    - 'agents/reference'
parent:
    - '[[skills/agent-self-improvement/SKILL|Agent Self Improvement]]'
related: []
depends_on:
    - '[[skills/agent-self-improvement/SKILL|Agent Self Improvement]]'
---

# Optional Langfuse Evidence

## Section Map

- Scope and selection: database projects, event dates and exact correlation.
- Availability: bounded queries and database-only fallback.
- Incorporating evidence: typed sources and duplicate-event handling.
- Mandatory usage markers: verified SQLite completion records.

## Scope And Selection

The learning database is the primary source. Langfuse may supplement selected
database records; it must not determine which unrelated projects to learn from.
Use this procedure before proposing changes when a learning request authorizes
analysis of the project's recorded experience. It does not enable capture, sync,
instrumentation, new accounts, credentials or subscriptions.

1. Resolve the local project binding and portable memory project ID. Select the
   eligible lesson/requirement versions and their linked episodes first. Check
   existing processing receipts; do not reopen used work merely to fetch logs.
2. Derive the dates from the actual events in those episodes: source-event
   timestamps, evidence `observed_at`, or verified session start/end. Do not use
   lesson creation/import/review dates as a substitute for event dates. Record
   the timezone. Convert calendar days to inclusive-start/exclusive-end UTC
   windows. Keep disjoint dates separate rather than fetching intervening days.
3. Resolve the application project's identity in Langfuse using a verified
   repository/root-path/project metadata value or an exact recorded session/trace
   mapping. A Langfuse account/project can contain many application repositories;
   the connector's project scope alone does not identify the learning project.
   Never equate matching dates, a model name or a similar task title with project
   identity. Keep each authorized learning project in a separate evidence batch.
4. Discover callable Langfuse read tools and their current schemas. With the
   observations connector, inspect filter/field schemas; if a metadata key is
   unknown, inspect only minimal IDs and metadata within the selected date window.
   Then apply the discovered exact project filter and session/trace filter when
   available. Do not retrieve full inputs/outputs from all projects to find a match.
5. Respect the connector's range and pagination limits. The inspected observations
   tool currently requires explicit bounds of at most 336 elapsed hours per
   request; discover limits again when tools change. Follow cursors within the
   authorized scope, deduplicate observation IDs and state any incomplete coverage.
   Fetch detailed payloads only for relevant observations. Verify returned project
   identity, timestamps and episode/session linkage before using any observation.

If event dates or project correlation cannot be established from available
evidence, skip Langfuse for that batch and continue from the database. Never
widen the project/date scope to compensate for an empty or uncertain match.

## Availability And Database-Only Fallback

Langfuse is optional. If no connector is available, authentication/access fails,
the service is unavailable, quota/rate limits are reported, or a correctly scoped
query returns no observations, continue learning using database evidence only.
Do not block the learning cycle, demand account upgrades or retry the same failed
request in a loop. At most one retry is appropriate for a transient failure; do
not retry confirmed quota/auth/permission failures during the same run.

Distinguish these observations in the learning report:

- `available`: matched observations were inspected; list the actual coverage.
- `partial`: some relevant observations are available, but coverage is incomplete.
- `not_connected`: no callable connector is available.
- `empty`: the scoped query returned no observations; the cause is unknown.
- `quota_exceeded`: the service explicitly reported a quota/monthly limit.
- `unavailable`: access or service failure; describe the observed error safely.
- `unmatched`: event dates or project/session identity could not be established.

An empty response may be consistent with exhausted monthly account limits, but
must not be presented as proof of that cause. Missing logs do not prove success,
absence of errors or absence of activity. Falling back changes evidence coverage,
not acceptance criteria: defer lessons if the database also lacks adequate support.
Partial matched evidence may be used with its limitations; unrelated logs may not.

## Incorporating Evidence

The orchestrating agent performs the optional connector reads. The Python
collector, hooks and `learning_cycle.py auto` do not acquire an implicit network
dependency or call MCP themselves. Before `propose`, curate relevant inspected
observations into existing typed project-memory evidence and link them to the
selected episodes/findings/lessons. Database-only CLI runs remain supported.

Use trace/observation IDs or accessible links in `source_ref`, the event time in
`observed_at`, and a short redacted factual summary. Preserve source revision,
procedure and actual result where required. Classify actual tool executions as
`command`/`test` only when the payload supports that classification; model prose
remains `agent_report`. A telemetry ERROR level alone is not a causal diagnosis,
and DEFAULT level does not prove a tool succeeded. Never fabricate missing fields
or accept a lesson just because telemetry exists.

The same event captured in the database and Langfuse is one observation, not two
independent episodes. Retain correlation and contradictory evidence. Do not copy
raw account-wide traces, credentials or unrelated project payloads into memory,
skills, reports or model prompts. Record collection availability and coverage in
the reviewed episode/check notes and final report using existing fields.

## Mandatory Usage Markers

After the approved learning change is actually applied, `complete_processing`
must persist `outcome=applied` with `details.used=true`, `used_at`, proposal link,
record/rule fingerprints and checks in the local SQLite decision journal. This
requirement is identical for Langfuse-enriched and database-only runs. Read back
the receipt before reporting completion. A failed receipt write means recovery
is pending, even if files were written; repeat approved apply to recover it.

Only linked work records receive the marker. Unselected/context-only records,
pending proposals, failed attempts and deferred lessons must not be marked used.
`no_change` is an explained processing decision, not a falsely claimed applied
lesson. Keep immutable record history and knowledge acceptance separate. Used
markers are per project, target rules and record version, not a permanent global
ban on reconsidering changed evidence. Project snapshots include these receipts
under the authorized exchange workflow. A receipt from another project never
marks this project's work used or grants permission to change its instructions.
