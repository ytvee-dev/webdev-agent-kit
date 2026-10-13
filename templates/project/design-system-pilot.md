---
id: 'agents.templates.project.design-system-pilot'
title: 'Draft Design System Pilot Contract'
doc_type: 'template'
layer: 'template'
status: 'draft'
publishable: true
local_only: false
tags:
    - 'agents/template'
    - 'frontend/design'
parent:
    - '[[docs/architecture/design-system-pilot]]'
related:
    - '[[templates/project/design-system-feedback]]'
depends_on: []
---

# Draft Design System Pilot Contract

**DRAFT — opt-in field experiment; not a verified workflow or synchronization
engine.** Do not activate or write this template during ordinary onboarding,
role selection, screenshot intake or a plugin update. For an explicitly requested
pilot, copy to the host `.agents/project/design-system-pilot.md`, set
`publishable: false` and `local_only: true`, and keep real project facts there.
Never edit a template inside the installed plugin cache as project state.

## Pilot Scope And Authority

- Owner and authorized task:
- Mode: inventory only / proposed mapping / approved one-component change:
- Included component family, variants, states and viewports:
- Excluded files, libraries, consumers and operations:
- Source references and revisions: code package/version, Figma file/node/version:
- Authority by concern: behavior, component API, tokens/modes, visual appearance:
- Conflicts requiring an owner decision; current decision and evidence:
- Available read/write capabilities and restrictions actually observed:
- Verification tools, expected outcome, retry limit and rollback boundary:

## Component Contract

| Concern | Observed source | Proposed mapping | Evidence / gap |
| --- | --- | --- | --- |
| Purpose and reusable family | | | |
| Anatomy, slots and nested parts | | | |
| Figma component/instance and code export | | | |
| Typed properties/events/defaults | | | |
| Variants and independent state dimensions | | | |
| Disabled/loading/error/focus behavior | | | |
| Keyboard and accessibility semantics | | | |
| Tokens, modes, effects and assets | | | |
| Long/localized content and constrained width | | | |
| Existing story IDs and consumers | | | |
| Unsupported combinations | | | |

Names or similar screenshots do not prove component identity. Inspect installed
exports and real instances. A hover/focus visual state does not automatically
become a public prop. Absent behavior and responsive states remain proposals.

## Token And Effect Mapping

| Semantic purpose | Figma ID/name/type | Alias and mode | Resolved value/unit | Code token and consumer | Authority / evidence / conflict |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Check alias targets, cycles, types, unit conversions, modes and actual consumers.
Preserve bindings and composite typography/effect semantics; equal literal
values alone do not establish a shared token. Never invent missing exact values
from screenshots or rewrite a frozen registry without approved scope.

## One-Component Change Proposal

1. Identify exact destination files/nodes and all affected instances/consumers.
2. Record proposed operations and dependencies, retained IDs/APIs/overrides,
   expected differences, acceptance evidence and allowed write scope.
3. Resolve source conflicts before dependent writes. Inventory is read-only;
   it does not authorize library publication, mass migration or new tooling.
4. If authorized and supported, implement one bounded component change and inspect
   actual state after each operation. A partial failure requires fresh inspection,
   not blind replay or a claim of atomic rollback.
5. Verify visual/structural results, tokens, overrides, API and relevant keyboard,
   focus and content behavior. Use existing Storybook only when present/in scope;
   no automatic setup or replacement of real components with mock demos.
6. Record pass/fail/blocked per criterion and owner feedback before expansion.

## Field Decision

- Result: untested / tested with gaps / accepted for this project / rejected:
- Retained source and rendered evidence:
- Failed assumptions and counterexamples:
- Local rule correction and reproduction:
- Reusable change candidate for the next Kit release:
- Owner decision before any wider rollout:
