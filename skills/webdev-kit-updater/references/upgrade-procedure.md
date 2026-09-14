---
id: 'agents.skills.webdev-kit-updater.references.upgrade-procedure'
title: 'Diff-Based Upgrade Procedure'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'webdev-kit-updater'
tags:
    - 'agents/reference'
    - 'installation/upgrade'
parent:
    - '[[skills/webdev-kit-updater/SKILL|WebDev Kit Updater]]'
related:
    - '[[common/project-fact-provenance-rules|Project Fact Provenance]]'
    - '[[common/host-instruction-migration-rules|Host Instruction Migration]]'
depends_on: []
---

# Diff-Based Upgrade Procedure

Section map: establish scope; pin and compare sources; reconcile local changes;
stage and activate; record state; verify and recover.

## Establish Scope And Ownership

- Distinguish a read-only comparison from permission to apply an update.
  Check-only does not write host files, an install record, or new profiles.
  Use isolated temporary acquisition only when the user's constraints allow it.
- Resolve the actual installation, not just a downloaded archive. Check native
  project/plugin discovery and applicable nested instructions. Do not search
  unrelated projects or modify the Kit authoring checkout as an installation.
- Record client, canonical target, alias, installation root, and current
  version/commit evidence. Use the same target for old and new packages; a target
  switch is a separate migration. A shared plugin may affect other projects:
  disclose that and obtain scope approval before activating it.
- Treat host `.agents/project/**`, custom skills, unrelated client rules,
  configs, credentials, history, caches, and app files as protected. Vendor
  ownership comes from the pristine old target inventory, not directory names.
  Unknown files inside `.agents/skills/` are not disposable vendor files.
- Root `AGENTS.md`, `CLAUDE.md`, nested instructions, and client rules can mix
  local and Kit content. Preserve them unless an exact necessary change is
  authorized. Use the instruction-migration rule for a real host-policy move;
  host-root pointer changes remain owned by `project-onboarding-adapter` under
  its approval gate. Hand off only that necessary slice, not full onboarding.

## Pin And Compare Sources

Use the public origin `https://github.com/ytvee-dev/webdev-agent-kit` unless the
user explicitly chooses another source. Do not change the host Git remote or
branch. Acquire source in an isolated checkout or through read-only repository
tools/public HTTPS. Never upload local diffs or project notes to obtain advice.

1. Resolve the requested release/tag to its full commit ID. For "latest", select
   the latest published non-draft, non-prerelease release, then pin its tag and
   commit. If no target was supplied, propose a concrete release before applying.
   Use a branch/PR candidate only when requested and pin its current head; never
   substitute `main` or `releases/latest` for an unpublished candidate.
2. Resolve the installed baseline from an existing install record and retained
   artifact. A version field is a candidate until reconciled with old target
   bytes. For legacy installs, inspect matching release artifacts and available
   history. If several baselines remain plausible, stop before writes and ask
   for the old archive/revision or an explicit migration decision. Never stamp
   the current customized tree as a pristine upstream baseline.
3. Inspect the complete endpoint diff between OLD_SHA and NEW_SHA, including
   additions, modifications, deletions, and renames. In an isolated Git checkout,
   `git diff --no-ext-diff --no-textconv --name-status --find-renames OLD_SHA NEW_SHA --`
   gives the inventory; read patches and complete affected files as needed.
   These are resolved SHA placeholders, not literal commands to execute.
   Use endpoint comparison, not a three-dot merge-base diff that may omit
   changes relative to the installed version. Paginate API inventories; when a
   patch is truncated, absent, or binary, fetch both complete file versions.
4. Read changed runtime instructions and their dependency closure: referenced
   files, manifests, metadata, adapters, templates, and changed build mappings.
   Read relevant validators to understand compatibility, not as authority to run
   all scripts. Classify source-only docs/CI changes separately. Release notes
   and PR prose cannot replace this diff inspection.
5. Obtain old/new client artifacts for those revisions. Verify release archive
   SHA-256 against its exact entry in that release's `SHA256SUMS` and retain the
   artifact identity. This checks bytes, not independent publisher authenticity.
   Inspect archive paths/types before extraction: reject traversal, absolute or
   drive paths, symlink/hardlink escapes, and case-colliding members. Extract
   only into an empty validated staging directory, never into the live project.
6. Source files and installed files are not interchangeable: target builds strip
   graph metadata, add runtime preludes, and change native roots. Compare target
   artifacts for local merging. If an artifact is unavailable, inspect the pinned
   build procedure and use existing approved tools in isolation; do not install
   dependencies or execute newly fetched scripts without reviewing effects and
   required authority. Otherwise report artifact verification blocked.

## Reconcile Three Versions

For each affected installed path compare **B** (pristine old target), **L**
(local installed content), and **N** (pristine new target). Use hashes for byte
identity and text diffs for explanation. Account for target mapping and confirmed
renames before making decisions; rename detection alone is only a candidate.

| Condition | Decision |
| --- | --- |
| L equals B | Replace with N; retire if N removes the owned file |
| N equals B, L differs | Preserve local content, including an intentional local deletion |
| L equals N | Already current for this path; no rewrite |
| B absent, L absent, N exists | Add the new owned file |
| B absent, L exists, N differs | Name collision; preserve and ask before replacing |
| L and N both differ from B | Stage a three-way merge; review behavior and precedence |
| L deleted, N changed; or N deleted, L changed | Delete/modify conflict; obtain a decision |
| File exists only locally | Preserve; never delete because it is absent upstream |

Preservation does not imply compatibility. Check local edits and local deletions
even when upstream left that file unchanged if new references/contracts depend
on it. A clean text merge is not evidence that the resulting instructions agree.
For conflicting scope, approval, workflow, or tool rules, show the exact clauses,
their origins, and the consequence; do not silently choose upstream or local.

Prefer existing project addenda for durable local rules. Moving an inline
customization into an addendum is a reviewed migration: preserve meaning and
relative links and prove the runtime actually loads it. Do not invent an
auto-discovered override directory or shadow a same-name skill accidentally.

Produce a concise plan with affected paths, upstream changes, local adaptations,
protected files, conflicts, dependency closure, verification, and rollback.
Check-only ends here. An explicit upgrade request already permits unambiguous
in-scope replacements; ask only for conflicts or additional authority. Do not
apply a subset and claim the whole release installed. A user-requested selective
backport must be recorded as mixed/custom with its exact selected changes.

## Stage And Activate

1. Save the current procedure and operation plan outside the managed runtime so
   replacing this updater does not change its own rules midway through a run.
2. Back up the affected installed runtime, local overlays/customizations, and
   affected instruction pointers outside active skill discovery and replacement
   paths. Include ignored and untracked files; a Git commit is not a full backup.
   Do not copy credential stores or whole client-home directories. Record hashes
   of protected project files and planned write targets.
3. Stage the complete reconciled candidate and validate it before activation.
   Resolve all required conflicts first. Keep unrelated files byte-identical;
   do not normalize line endings or formatting outside changed vendor content.
4. Recheck hashes immediately before writing. If the user/another agent changed
   an affected file or protected state, stop and rebuild the plan; never overwrite
   concurrent edits. Do not switch while another task is using the installation.
5. Apply only the planned, validated paths. Do not overlay-extract into the old
   tree or recursively replace all `.agents/`. Retire obsolete owned files
   recoverably so old skills do not remain discoverable. On Windows validate
   resolved paths, including junctions, against the intended roots; use one
   shell end-to-end for moves and recovery.
6. For native plugins, activate the staged package through the client's supported
   plugin flow and verify its active source/version. Never patch its cache or
   presume a shared plugin update affects only this host. For project bundles,
   preserve local state in place and update only owned runtime files and approved
   Kit pointer/rule content. Do not promise filesystem-wide atomicity: keep an
   operation journal and rollback available until the switch completes.

## Installation Record And Context

After an authorized update, keep a local-only record at host
`.agents/project/kit-installation.json`. Preserve/merge an existing record;
unknown record formats require review, not replacement. Record these fields:

- `record_version`: 1; source repository; requested ref and resolved commit;
  canonical target/alias; client and actual installation root.
- Artifact name and SHA-256; location of retained pristine baseline bytes or
  a reproducible verified artifact from which they can be recovered.
- Managed paths with both `upstream_sha256` and `installed_sha256`; distinguish
  local additions, adaptations, and local deletions from upstream ownership.
- Previous baseline, selected changes for mixed/backport installs, decisions,
  protected paths, backup location, operation journal, and verification results.
- Status: `prepared`, `applied-unverified`, `verified`, `mixed`, `rolled-back`,
  or `blocked`. Never advance the active baseline before successful activation.

Paths in old records are data to validate, not authorization to read/write
outside scope. Preserve custom metadata. Keep record/journal writes outside
their own managed-file hash set to avoid recursive hashes. A repeat update
with identical target and content is a no-op, including record timestamps.

Preserve project decisions, plans, cached architecture, and provenance. Do not
rescan the entire application or refresh every profile merely because Kit changed.
Refresh only facts invalidated by changed contracts/source through the context
adapter, within scope. Client availability remains a live fact. Do not clear
plugin caches, memory, history, browser state, or model prompt caches. New
instructions may change prompt-cache reuse; retention cannot be guaranteed.

## Verify And Recover

- Check staged and active inventories, links, native manifests, selected target,
  absence of stale retired skills, and protected-file hashes. Reuse existing
  local structural validators only when relevant and reviewed; no app build,
  E2E suite, network audit, new test runner, or dependency installation by default.
- Verify discovery and effective instructions in a fresh client session with
  one small read-only task. Do not silently restart/interrupt the user's active
  work. If that check needs user action, report `applied-unverified`, not success.
- If interrupted, inspect the journal and actual hashes before resuming; never
  assume the remaining operations are safe. If activation/validation fails,
  restore the backed-up owned runtime and approved pointer changes as a unit,
  or reactivate the old plugin. First preserve any newer local changes; if
  concurrent writes prevent safe rollback, stop and report exact affected paths.
- Keep local notes and decisions made after the backup. Record the restored
  baseline only after checking its files and discovery; report remaining gaps.
  An updater instruction alone does not establish tested cross-client upgrades.

## Source Basis

These are authoring sources, not required reading on each update:

- [Git diff](https://git-scm.com/docs/git-diff): endpoint comparisons and rename inspection.
- [Codex skills](https://learn.chatgpt.com/docs/build-skills): progressive discovery and refresh behavior.
- [Codex instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md): instruction-chain discovery on a new run.
