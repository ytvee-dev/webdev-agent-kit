---
id: 'agents.docs.release.learning-capture-audit'
title: 'Capture And Snapshot Consistency Audit'
doc_type: 'audit-report'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/learning'
    - 'release-management'
parent:
    - '[[CHANGELOG]]'
related:
    - '[[docs/install/project-memory]]'
    - '[[skills/agent-self-improvement/SKILL]]'
depends_on: []
---

# Capture and snapshot consistency audit

## Boundary And Method

Base: released v1.9.0. Scope: Kit source only; installed STEM/ASI are unchanged.
Publication of these changes as v1.9.1 was separately authorized on 2026-10-29. Historical 1.9.0 reports and
source inventories describe that release and are not rewritten as new results.

The audit combines cross-repository searches of runtime policies, skills,
adapters, installation/update guidance and executable helpers with source graph,
precedence, context-budget, routing, planning and generated-target validators.
Focused semantic review follows each learning stage through its instructions,
CLI, state, consent, error paths and tests. Passing these checks is not proof that
all natural-language instructions are contradiction-free or every client works.

## Findings And Resolutions

| Finding / conflicting sources | Consequence | Resolution / evidence |
| --- | --- | --- |
| Collection contract said state was outside repositories; memory contract used project state | Different storage expectations | One documented precedence: explicit state, environment, project default; resolver/CLI tests |
| Manual-write example forced the default directory | Existing external history could be bypassed | Example uses resolved state; external-store live trial and regression |
| Workflow, run binding, tagging and exchange hard-coded project state while CLI accepted overrides | Different stages read different databases | Shared resolver throughout; external analysis/restore and two-project tests |
| Installed hooks did not persist an explicitly selected external store | Later client could fall back to another database | Installer records resolved state in owned hook commands; subprocess test without environment override |
| Finish always enqueued, although upload could be disabled | Refusal still produced snapshots | Consent gates creation and delivery; refusal/no-change completion tests |
| Snapshot setup described address configuration separately from completion consent | Accepting storage did not establish the requested behavior | Onboarding explicitly offers after-each-learning snapshots and saves enabled/declined choice |
| Snapshot queue also included telemetry archives | Snapshot consent exported a larger dataset | Structured memory/history only; archive exclusion test |
| Outbox paths lacked repository identity | Address changes could redirect older data | Repository and folder bound to each job; unknown/old destinations remain blocked |
| Repeated finish could regenerate a different snapshot | A completed cycle lost its original snapshot association | Durable per-run hash link, unchanged on retry |
| Hook failures were silent; missing IDs used content hashes | Undetected drops and false deduplication | Content-free health, bounded input/time, synthetic-ID limitations, actual receipt metadata |
| Capture/status initialized unknown state before checking opt-in | An unconfigured hook could create a new store | Read-only unconfigured result, with no automatic initialization |
| No completion storage-pressure report | Unbounded growth went unnoticed | Raw/structured counts, SQLite+WAL and separate artifact sizes; consent-only cleanup proposal |
| Project names with spaces produced rejected remote paths | Valid projects could not send snapshots | Safe new folder names retain stable IDs; existing unsafe destinations are not silently rewritten |
| Git-tree uploads assumed an existing first commit | Empty private repositories could never receive a first snapshot | Bounded Contents-API bootstrap with exact readback regression |
| Record wrote an exchange dirty marker even without completion | Recording and exchange were unnecessarily coupled | Record notification has no filesystem or network side effects |
| Updater protection named only the default learning directory | Alternate installed-store locations were underspecified | Explicitly protect resolved state and migration/lock files |

## Preserved Contracts

Manual record, capture, semantic curation, improvement and tracing remain separate.
Explicitly requested learning alone may perform the approved completion upload;
there is no timer or background worker. Retry occurs on the next requested
completion or explicit sync, not an unattended loop. Prior explicit refusal and
legacy unconfirmed addresses never authorize automatic snapshots.

Each completed run, including no-change, retains its completion receipt and
reflection independently of upload success. Snapshots are recoverable JSON
structured memory and processing history; they are not copies of raw SQLite.
Recovery imports historical receipts for review and never reapplies rules.

Storage defaults are 50,000 raw events or 250 MiB SQLite plus WAL. Cleanup asks
permission and previews old processed raw events only; all source references and
structured history remain protected. Because reviewed events can also be retained
as evidence, the safe eligible count can be zero. No protection is weakened just
to reduce size. Existing broad explicit raw-retention commands remain available;
the completion recommendation uses the stricter processed-only preview.

Native trust remains a client decision. Source policy precedence, model-output
rules, explicit skill application gates and Kit transfer boundaries are preserved.
Existing manual unevaluated-application overrides are explicit exceptional paths,
not evidence of automatic certification or a waiver granted by this change.

## Best-Practice Basis

- [OpenTelemetry data minimization](https://opentelemetry.io/docs/security/handling-sensitive-data/): minimize fields and avoid persisting secrets in diagnostics.
- [OpenTelemetry resilience](https://opentelemetry.io/docs/collector/resiliency/): bound queues, expose failed delivery and distinguish persistence from remote acknowledgement. This implementation deliberately excludes background retries.
- [Langfuse masking](https://langfuse.com/docs/observability/features/masking): sanitize before export; local capture and remote tracing remain separate integrations.
- [Langfuse sampling](https://langfuse.com/docs/observability/features/sampling): trace sampling is a separate vendor capability, not applied to local learning events in this change.
- [SQLite backup guidance](https://www.sqlite.org/backup.html): consistent snapshots require a database transaction/API, not copying a live database file. Existing JSON snapshots use a read transaction.

## Verification And Limits

Local validation: 104 learning/helper tests passed; Ruff, Markdown (244 files),
local links and strict schemas passed. Source/portable-target validation passed;
12 candidate archives for six distributions were rebuilt and validated. These
archives are local candidates, not a new published version.

Regression tests cover state precedence, project isolation, legacy-store
compatibility, capture deduplication/metadata, blocked/oversized hooks, explicit
hook-state persistence, snapshot refusal, no-change completion, stable retry links,
destination changes, empty repositories, archive exclusion, restoration and
storage-pressure protection. Existing baseline/candidate, curation, telemetry and
lost-response regressions remain in the suite.

Live scenario artifacts remain outside the source tree. The candidate refusal
scenario was compared with the same read-only scenario on v1.9.0. The baseline
correctly reported unconditional local snapshots and absent thresholds; the
candidate scenario was read-only: the agent followed the selected snapshot/cleanup contract
and changed no files. The candidate explicit-state memory scenario executed
initialization, three-record insertion, integrity/audit and ID readback, as shown
in the captured tool trace. It did not edit rules. The outer audit process could
not independently reopen the sandbox-created state because Windows denied access;
therefore persistence verification is trace-observed, not independently certified.
The runner's changed-file list omitted that inaccessible subtree and is not proof
that no database was created. Do not weaken filesystem protections to inspect it.

Native client hook delivery and real private-repository upload are not certified
by subprocess tests or injected APIs. No personal learning repository, Langfuse
account, credentials or production traces were used. Real remote delivery remains
unverified. The selected live scenarios do not establish general improvement in
agent behavior or model weights. Later hook/queue hardening has regression coverage; the retained live trials
are not certification of every final helper revision. CI and PR checks identify
the final tested commit.
