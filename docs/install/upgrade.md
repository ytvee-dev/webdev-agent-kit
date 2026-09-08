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
depends_on: []
---

# Upgrade And Rollback

Use an explicit old and new release tag. During a release PR, candidate archives
built from that branch are local artifacts; `releases/latest` still resolves to
the published release. Do not use it to test unpublished 0.5.0 content.

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
4. Read the changelog and [first-run checks](first-run.md). Verify the new
   archive and extract into an empty staging directory.

## Project Bundles: Codex And Cursor

Replace the owned kit runtime from staging; avoid overlay extraction that can
leave deleted old skills active. Restore only local `project/**` facts and
reviewed customizations. Preserve unrelated host instructions and client rules.
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
