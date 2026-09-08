---
id: 'agents.common.host-instruction-migration-rules'
title: 'Host Instruction Migration'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags: []
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[templates/project/instruction-migration]]'
    - '[[common/client-adaptation-policy]]'
depends_on: []
---

# Host Instruction Migration

Use during explicitly requested onboarding or instruction migration. An ordinary
code task never rewrites the host entrypoint.

## Missing Entrypoint

For a project-bundle target, approved onboarding creates the minimal native
pointer when absent and verifies its destination exists. A native Claude plugin
does not need an AGENTS pointer; follow its adapter for separately installed
shared policy.

## Existing Entrypoint

1. Read the entire instruction file being migrated; a pointer snippet cannot
   establish what would be lost. Inventory every rule, scope, relative link,
   command, and precedence condition.
2. Map instructions to local `project/host-instructions.md`. Keep original
   normative wording and scope. Put verified descriptive stack, styling,
   verification, and path facts in their owning profiles; do not turn an
   unverified claim into a confirmed fact.
3. Keep a verbatim local backup and a migration map showing original section,
   destination, and preserved meaning. Use `templates/project/instruction-migration.md`.
   Keep nested instruction scopes nested; do not promote their rules globally.
4. Fix relocated relative links so they resolve to the original destinations.
   Never copy host rules into reusable `common/**`, `skills/**`, or source
   policy. Record contradictory instructions explicitly; do not silently drop
   or resolve them by guessing.
5. If the current request explicitly authorizes migration and replacement, use
   that authorization; do not ask again. Otherwise present the concrete map and
   proposed pointer diff before replacing existing instructions.
6. Write and validate the local destinations before replacing the root with the
   canonical minimal pointer. Verify the shipped core loads
   `project/host-instructions.md` before task-specific defaults.
7. Confirm every inventoried rule is reachable, all relative links resolve,
   unrelated files are unchanged, and a repeat migration is a no-op. If coverage
   is incomplete, preserve the original root and report the unresolved mapping.

This is a local policy migration, not authorization to change app code, install
dependencies, rewrite host docs, or expand access. Restore the backed-up
entrypoint if reachability or preservation cannot be established.
