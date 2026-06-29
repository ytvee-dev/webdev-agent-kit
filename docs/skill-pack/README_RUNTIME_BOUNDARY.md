# README Runtime Boundary

Status: draft architecture plan addendum.
Scope: keep repository README files out of agent runtime flow.

## Core Rule

`README.md` is a human-facing repository description, installation guide, and usage overview only.

It must not participate in agent runtime routing, context gathering, skill selection, skill execution, verification, or project memory.

## Agent Runtime Policy

Agents must not read `README.md` during normal runtime unless the user explicitly asks to:

```text
edit README.md
audit README.md
summarize README.md
update human-facing repository documentation
```

## Reason

README files are written for humans. They often contain marketing copy, installation examples, historical notes, or simplified explanations. Using them as agent runtime context can create stale assumptions, duplicate routing rules, and hidden conflicts with `AGENTS.md`, `common/**`, `skills/**`, and `project/**`.

## Source Of Truth Split

```text
AGENTS.md -> canonical agent policy and routing
skills/** -> task-specific runtime instructions
common/** -> reusable runtime rules
project/** -> local-only host-project facts
SUMMARY.md -> manual human catalog only
README.md -> classic human-facing repository README only
```

## Required Plan Changes

Future work must preserve this boundary:

```text
- do not list README.md as runtime required context;
- do not route through README.md;
- do not use README.md as project memory;
- do not use README.md to infer stack, commands, or conventions unless the user explicitly asks to inspect README.md;
- keep README.md synchronized only for human-facing documentation when user-facing workflow changes;
- keep AGENTS.md as the only canonical runtime entrypoint.
```

## Validation

When changing routing, skills, or common rules, verify:

```text
- README.md is not listed in Required Context;
- README.md is not used in runtime pipelines;
- README.md is not required for skill invocation;
- README.md remains human-facing and readable as a classic repository README;
- AGENTS.md, skills/**, common/**, and project/** contain the actual agent runtime rules.
```

## Relation To Current Architecture

This addendum extends `IMPLEMENTATION_PLAN.md` and `OPERATING_MODEL.md`.

The architectural intent is:

```text
README.md describes the skill pack for people.
AGENTS.md and skills/** operate the skill pack for agents.
```
