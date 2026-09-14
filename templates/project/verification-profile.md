---
id: 'agents.templates.project.verification-profile'
title: 'Verification Profile Template'
doc_type: 'template'
layer: 'template'
status: 'active'
publishable: true
local_only: false
tags: []
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related: 
    - '[[common/project-fact-provenance-rules]]'
depends_on: []
---

# Verification Profile Template

Copy to local-only `project/verification-profile.md` with `publishable: false`
and `local_only: true`. Populate only discovered commands; remove unused rows.

## Provenance

- checked date and source revision:
- kit version and canonical target:
- OS and shell:
- source files inspected:
- refresh when: scripts, toolchain, client, sandbox, or relevant source changes

## Existing Commands

| Command and working directory | Script expansion / config source | Proves | Does not prove | Last result and evidence |
| --- | --- | --- | --- | --- |

Use `not-run` for discovery without execution. Record the exact command and
revision for a real result. Do not infer type checking from a bundler command.

## Verification Order

Name the smallest existing check for each affected surface. Preserve verified
project order and distinguish tests, types, lint, build, functional interactions,
and rendered comparisons. An absent test script is a fact, not an install task.

## Environment Blockers

| Command | Failure class and evidence | Approved fallback and attempt count | Remaining impact |
| --- | --- | --- | --- |

Windows shell and sandbox handling follows `common/windows-shell-sandbox-rules.md`.
A blocked command never becomes a passed check through a source-only fallback.

## Functional And Visual Evidence

Record the route, state, interaction, viewport when relevant, observed result,
and retained evidence location. List outstanding checks only when material.
