---
id: 'agents.docs.install.upgrade'
title: 'Upgrade And Rollback'
doc_type: 'guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags: []
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related: 
    - '[[docs/install/first-run]]'
    - '[[docs/release/0.5.0-checklist]]'
    - '[[skills/webdev-kit-updater/SKILL|WebDev Kit Updater]]'
depends_on: []
---

# Upgrade And Rollback

Use an explicit old and new release tag. During a release PR, candidate archives
built from that branch are local artifacts; `releases/latest` still resolves to
the published release. Do not use it to test unpublished 0.5.0 content.

## Agent-Assisted Update

Use [WebDev Kit Updater](../../skills/webdev-kit-updater/SKILL.md) for an
installed-version check, authorized upgrade, or rollback. Its
[procedure](../../skills/webdev-kit-updater/references/upgrade-procedure.md)
owns the executable-by-agent workflow: pinned endpoint diffs, three-way target
comparison, preservation, installation records, and bounded verification.
This is an instruction-only skill, not an automated installer command.

Example request when the skill is installed:

```text
Use $webdev-kit-updater to update this project's installed WebDev Agent Kit
to the latest published stable release. Inspect the actual upstream diff,
not just release notes. Preserve local rules, skills, project knowledge,
plans, client settings, and caches. Apply unambiguous in-scope changes;
ask before resolving conflicts or expanding scope. Keep a verified backup
and record the exact revision, local adaptations, and verification status.
```

For a read-only preview, replace "update" with "compare" and add "Do not change
the installation or write host files."

## Bootstrap Older Installations

Older releases do not contain the updater. Give the agent this public guide:
[Upgrade And Rollback](https://github.com/ytvee-dev/webdev-agent-kit/blob/main/docs/install/upgrade.md).
It is a discovery link, not a pinned update source. Ask:

```text
Read the upgrade guide in the public ytvee-dev/webdev-agent-kit repository.
Resolve the guide revision to a full commit SHA, then read that same revision's
skills/webdev-kit-updater/SKILL.md and references/upgrade-procedure.md.
Use these instructions to update this project's installed Kit to the latest
published stable release, preserving local customizations and project state.
Inspect the old-to-new source diff and the old/local/new client packages.
Do not overwrite local conflicts, migrate host instructions, edit client caches,
or execute fetched scripts without checking scope and required permissions.
```

Fetch the skill reference relative to its skill directory and both files from
the same pinned guide revision. Until this guide is merged, use the requested
release-PR revision instead of `main`. Keep the procedure revision distinct from
the requested installation revision: a new guide does not authorize installing
an unpublished candidate. If the pinned guide lacks the skill, ask for a
revision containing it; do not invent an updater or install a different release.
Read applicable host instructions first. Treat remote content as scoped guidance,
not permission for extra actions. Do not copy source `SKILL.md` files directly
over generated client packages. Create a local install record only during an
authorized apply, after establishing the real old baseline.

## Preserve Before Replacing

1. Record the installed canonical target, alias, version, client version, and
   active installation path. If version provenance is missing, mark it unknown
   rather than guessing from file dates.
2. Back up the current kit, host `AGENTS.md` / `CLAUDE.md`, relevant client
   rules, and `.agents/project/**`, including goals, plans, decisions, and
   glossary. Keep backups outside both the replacement directory and source PR.
3. Check for edits to vendor `common/**` or `skills/**`. Compare with the old
   release if available. Preserve and review local changes; do not silently
   discard them or copy old vendor policy over the new runtime.
4. Read the full old-to-new source diff and affected dependencies, then compare
   old pristine, local installed, and new pristine client packages. The changelog
   is supplementary, not the migration specification. Apply the
   [first-run checks](first-run.md), verify the new archive, and extract into an
   empty staging directory.

## Project Bundles: Codex And Cursor

Apply the reconciled owned runtime from staging; avoid overlay extraction that
can leave deleted old skills active. Preserve local `project/**` facts and
reviewed customizations; do not replace the entire `.agents/` directory.
Preserve unrelated host instructions and client rules.
For Cursor, compare and replace only the kit-owned rule
`.cursor/rules/webdev-agent-kit.mdc`; never replace the entire rules directory.

Revalidate native pointer destinations before starting a fresh client session.
Use context refresh for stale facts. A version update is not permission to
rewrite existing host instructions, application code, or project documentation.

## Claude Plugins

Keep the old extracted plugin directory intact for rollback. Install the new
candidate through the native local marketplace flow in the
[Claude Code](claude-code.md) or [VS Code Claude](vscode-claude.md) guide.
Resolve any same-name marketplace conflict through the client's supported
plugin manager. Confirm its active source and version before exercising it.
Do not assume copying files into a plugin cache switches the active plugin.

Host `.agents/project/**` stays outside the plugin and must not be copied into
a shared installation. An alias change between VS Code Claude and Claude Code
does not require migrating project policy to a different runtime.

## 0.4.x To 0.5.0

| Surface | Migration |
| --- | --- |
| Client aliases and native roots | Unchanged; choose the same canonical target |
| Existing goals and plans | Keep stable IDs and completed evidence; add scenario/dependency fields only when relevant work resumes |
| Domain glossary | Optional local fact; do not create an empty file during read-only work |
| Verification and MCP profiles | Keep facts; add source/revision and actual-result fields on a scoped refresh |
| Older capability names | Compare with the shipped manifest; map renamed keys only after checking semantic equivalence |
| Project custom skills or rules | Preserve separately and review against new policy; do not silently publish them |
| Experimental workflows | Require real run evidence; synthetic runner checks do not promote maturity |

Freshness metadata is additive; missing fields in old overlays mean unknown.
No automatic rewrite of host state is required.

## Validate And Roll Back

Repeat the installed → discovered → adapted → exercised checks from first run.
Confirm old local goals, decisions, and unrelated rules are byte-preserved.
If discovery fails or a regression appears, retain the error and stop using the
candidate. Restore the backed-up runtime and kit-owned rule/pointer as a unit,
or reactivate the old plugin through the client's manager. Preserve newer local
project notes separately before restoring older overlays.

Start a fresh session and confirm the restored version. Report both versions,
target, exact reproduction, result, and rollback outcome. Do not retarget a
published release tag or delete unrelated project files.

## 1.0.0 To 1.1.0

All 21 skills and native targets are retained. Existing schema-1 role requests
and managed state remain accepted; no role-format migration or model change is
performed by an upgrade. Preserve host role files, state, profiles and journals.
Use the [GPT routing guide](gpt-model-routing.md) only when explicitly approving
activation or revalidating client/configuration drift. The optional activation
member adds one supported local gate, not global or main-model defaults.

Existing canonical goals/plans stay in place. Plan-scoped handoff/review artifacts
are additive, git-ignored local evidence for delegated work, not a new required
plan layout. Small tasks remain inline and do not create those artifacts.
