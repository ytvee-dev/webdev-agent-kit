---
id: 'agents.common.project-fact-provenance-rules'
title: 'Project Fact Provenance'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags: []
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related: 
    - '[[templates/project/verification-profile]]'
    - '[[common/mcp-availability-detection-rules]]'
depends_on: []
---

# Project Fact Provenance

Cache project facts as evidence with a scope, not as permanent permission or
proof that a check passed. Load this rule during onboarding, context refresh,
or when a decision depends on a stale or disputed overlay.

## Record And Refresh

- For consequential facts, record the source path or user confirmation, date,
  checked revision when available, and the condition that invalidates the fact.
- Preserve project-specific styles, routing, design-system APIs, and required
  engineering documents. Record exact document paths and applicable tasks
  when host instructions designate them; reading never authorizes editing.
- Confirm component APIs against the installed package version. A neighboring
  design-system checkout is a reference, not proof of the installed API or an
  authorized runtime import.
- Refresh only facts affected by changed source, scripts, client, kit version,
  or tools. Do not mark untouched historical entries as freshly verified.
- An old overlay that conflicts with current source or session tools is stale.
  Keep useful context, replace the contradicted fact during authorized refresh,
  and record unknown when the current evidence is insufficient.
- Project-only review routes, product exclusions, and component preferences
  remain local. Do not turn them into reusable kit restrictions.

## Verification Commands

Use `templates/project/verification-profile.md` to record each existing
command's expansion, working directory, covered checks, exclusions, and last
actual result. A discovered command starts as `not-run`. A successful build
does not imply type checking, tests, or rendered behavior: inspect its script
chain and configuration before claiming that coverage.

For example, `vite build` alone does not type-check; `tsc -b && vite build`
includes a separate compiler check. An unknown script chain remains unknown.
Use the existing scoped type-check command when required; do not add scripts or
dependencies to make the profile look complete.

## Capability Freshness

Distinguish configured, discoverable, callable in this session, and successfully
used for a specific check. A registry entry supports availability, not a claim
that a screenshot or verification succeeded. A previous-session success needs
current availability confirmation when the task requires that capability.

Do not run a browser or start an app just to populate onboarding fields.
Record `not-run` or `unknown` and the missing evidence. Current sandbox failures
override historical availability; use the existing bounded fallback rules.
