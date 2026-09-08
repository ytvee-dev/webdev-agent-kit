---
id: 'agents.docs.architecture.field-evidence'
title: 'Field Evidence And Contributor Reports'
doc_type: 'guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags: []
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[docs/architecture/behavior-evaluation]]'
    - '[[docs/architecture/reproducible-workflows]]'
depends_on: []
---

# Field Evidence And Contributor Reports

## Evidence Reviewed For 0.5.0

Two maintainer-supplied project documentation snapshots were reviewed. Both
describe React/Vite projects used with Codex, including Windows shell context.
They are configuration and project-convention evidence, not retained agent
transcripts or independent client compatibility passes. Source project names,
paths, repository routes, and raw private files are omitted.

| Observation in supplied documentation | Generalized action | Public reproduction |
| --- | --- | --- |
| One project uses plain CSS; another uses CSS Modules and an installed design system | Preserve verified local conventions and installed APIs | `onboarding-existing`, design-system trigger fixture |
| Client and MCP profiles have different validation dates and discovery detail | Record source/session freshness; separate availability from successful use | `stale-browser-profile` |
| A verification profile attributes type checking to a Vite build without retaining command-chain evidence | Record command expansion and exact coverage; leave results not-run until executed | `refresh-build-coverage` |
| A project designates a specific engineering document and feature-level rules | Preserve scope and read-only references in local overlays | `migrate-instructions` |
| Local review transport and product/UI restrictions differ from reusable policy | Keep team-specific constraints local | Instruction migration coverage map |

The build observation identifies an unsupported claim in documentation, not a
reproduced source-project build failure. Vite's
[TypeScript documentation](https://vite.dev/guide/features.html#typescript)
confirms that transpilation alone does not establish type safety.

The fixture prompts are original, sanitized reconstructions. They are publicly
reproducible inputs; they do not count as live successes or failures. Windows
log cases are synthetic replays. No real Windows or other-client run is inferred
from these snapshots. These two React/Vite configurations do not establish a
distinct Next.js workflow gap.

## Report A Case

Use the behavior or compatibility issue form. Include:

- exact kit tag/commit and archive/checksum when relevant;
- client surface and version, canonical target/alias, model, OS, and shell;
- evidence kind: observed agent run, observed installation, configuration
  snapshot, or synthetic replay;
- minimal prompt, supplied context, actual tools and sandbox restrictions;
- expected and selected skill, including a near-miss prompt that should not route;
- exact command/error, changed files, outcome, and sanitized evidence;
- repeat count, failures as well as successes, and whether a fresh session was used.

Installation reports distinguish package extraction, native discovery, project
adaptation, and exercised behavior. A checksum failure is reportable; do not
claim it passed merely to submit a report. Do not paste secrets, private source,
customer data, or full local profiles. Public sharing must be authorized.

## Turn A Report Into A Regression

1. Triage the evidence kind and affected contract. Label unsupported facts
   unknown. Separate environment blocks from source defects and agent mistakes.
2. Reduce to public synthetic inputs that preserve the failure condition.
3. Add positive and near-miss cases to the owning static eval file; keep all
   existing schema, policy, routing, and context-budget gates.
4. Add a live scenario when actual behavior needs assessment. Use `files`
   only for safe workspace-local fixtures; the runner rejects path traversal
   and any fixture write into installed policy.
5. Run static validation and synthetic mechanics. Then run a fresh real client
   when available and assess the trace against its rubric separately.
6. Promote a reusable pattern only when repeated independent evidence supports
   its boundary. Keep local preferences in project overlays; retain failures,
   uncertainty, and counterexamples.

For Windows, retain the original `.ps1` error, the one `.cmd` fallback result,
and any approved sandbox fallback separately. A successful build plus failed
dev-server startup cannot become a rendered pass.

For archives, run `python scripts/validate_release_archive.py --build-fixtures`.
It checks extracted native contracts and preservation of host instructions,
local plan state, and unrelated Cursor rules. Negative inventories cover unsafe
Windows names, traversal, collisions, links, private overlays, and wrong roots.

## Current Coverage Limit

Deterministic fixture/schema validation and synthetic runner success are release
gates. Actual behavior across supported clients remains an evidence-collection
task; report counts from configuration snapshots must not promote skill maturity.
Use the governance criteria for stability, with client/model-specific traces
and independent projects. No global success percentage is claimed here.
