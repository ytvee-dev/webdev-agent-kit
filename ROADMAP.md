---
id: 'agents.roadmap'
title: 'WebDev Agent Kit Roadmap'
doc_type: 'roadmap'
layer: 'bundle'
status: 'active'
publishable: true
local_only: false
tags:
    - 'community/roadmap'
    - 'planning/public'
parent: []
related:
    - '[[docs/install/first-run]]'
    - '[[docs/install/upgrade]]'
    - '[[docs/architecture/field-evidence]]'
    - '[[docs/architecture/reproducible-workflows]]'
    - '[[README|WebDev Agent Kit]]'
    - '[[GOVERNANCE|Project Governance]]'
    - '[[CHANGELOG|WebDev Agent Kit Changelog]]'
depends_on: []
---

# Roadmap

This roadmap communicates direction, not a delivery promise. Priorities may
change when user evidence, client behavior, security constraints, or maintainer
capacity changes. Accepted work is tracked in GitHub Issues and completed work
is recorded in `CHANGELOG.md`.

## Current

- Prepare `0.5.0` while retaining the `0.4.x` target contracts and local plans.
- Validate first-run and upgrade guidance against real client installations;
  [first-run checks](docs/install/first-run.md) and
  [upgrade/rollback](docs/install/upgrade.md) are implemented in the release candidate.
- Exercise the public [reproducible workflows](docs/architecture/reproducible-workflows.md)
  for scoped fixes, screenshots, review, migration, and verification boundaries.
- Collect actual agent-behavior and client-compatibility runs through the expanded
  issue forms. [Field evidence](docs/architecture/field-evidence.md) currently
  contains two configuration snapshots, not cross-client behavior passes.
- Keep Codex, Claude Code, Cursor, and VS Code aliases aligned with their
  canonical contracts; installation and archive validation remain release gates.

## Next

- Expand live behavior evidence without weakening deterministic static evals.
  The runner records provenance; completed adapters still require human assessment.
- Confirm upgrade and rollback across published versions with retained local
  overlays, host instruction migration, and native client discovery evidence.
- Add focused React and Next.js workflows only when repeated user runs show a
  distinct gap. Two React/Vite configurations do not meet that threshold.
- Exercise Windows shell/sandbox fixtures on actual Windows clients. Synthetic
  log replays and Windows archive-path rejection are contributor checks, not
  proof of real sandbox compatibility.
- Refine community patterns and anti-patterns from public, reproducible cases,
  preserving failures and near misses alongside successful runs.

## Exploring

- Evidence-gated profiles for Vue, Svelte, or Astro.
- A discoverable registry for community-maintained skills and profiles.
- Private team policy packs layered over the open core.
- Centralized version visibility and compatibility reporting.
- Additional host adapters when their native contracts can be validated.

Items in **Exploring** are not accepted features. New stacks, clients, skills,
dependencies, and services still require the proposal and approval process in
`GOVERNANCE.md`.
