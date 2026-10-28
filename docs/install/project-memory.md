---
id: 'agents.docs.install.project-memory'
title: 'Project Memory'
doc_type: 'install-guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/learning'
parent:
    - '[[CHANGELOG]]'
related:
    - '[[skills/agent-self-improvement/SKILL]]'
depends_on: []
---

# Project memory

The Kit remembers project experience by saving records and retrieving relevant
ones for later tasks. It does not train model weights. A correction can become a
candidate lesson; a useful lesson can later become a checked project rule.

## Project-local defaults and explicit choices

New state lives at `<project>/.agents/learning`; capture, telemetry and exchange
start off. `--state PATH` takes precedence over `AGENT_LEARNING_STATE`, then the
selected project. Both `--project ROOT` and `--project=ROOT` work from any directory.
If the old shared store contains this project's history, migrate explicitly with
`learning_project.py --project ROOT --legacy STATE`; the source is preserved.
Status prints the actual state/database path. Kit updates preserve this directory.

Ask the agent to save a correction to its learning database. It records structured
experience and reports IDs; it does not rewrite project rules or start analysis.
For long captured sessions, follow `context --limit 200` and its `next_cursor` via
`--cursor TOKEN`. `run` skips curated source IDs; `--reconsider` requests reanalysis.

During adaptation, choose Langfuse connection or decline. The agent offers saved
keys or opens the private credential file, waits, sets project tags and checks
readback. Disable tracing for one project with an explicit agent request; other
projects and local memory remain available. A stored choice survives updates.

Verify a private sync destination with `learning_memory.py configure --project ROOT
--repository OWNER/REPO`. Only add `--sync-on-finish yes` when completion-stage
upload is wanted; `no` disables it. Address configuration alone never uploads.
Conflicting legacy addresses must be resolved explicitly before snapshot exchange.

## Upgrade existing memory

Upgrade the Kit on every computer that exchanges the same project memory before
using v1.8 fields. The SQLite and package schema number remains 2. Older Kit
versions reject the added optional fields, so mixed-version writing is unsupported.
Existing records are preserved. An old `accepted` label does not guarantee that
its evidence meets the new checks.

Commands below use Python and paths relative to an installed `.agents` directory.
Run from the project root. On Windows use `py` instead of `python` if appropriate.
If your state directory is custom, put `--state PATH` before the subcommand.

```sh
python .agents/skills/agent-self-improvement/scripts/learning_memory.py check --project .
python .agents/skills/agent-self-improvement/scripts/learning_memory.py audit --project .
```

`check` verifies storage and references. `audit` lists evidence and provenance gaps,
application stages and reviewed episodes. It does not independently re-run old
commands or prove an agent learned a rule. Repair incomplete records with a new
revision and real evidence; do not invent missing measurements or session IDs.

## What the statuses mean

| Question | Record or field |
| --- | --- |
| Has this session been reviewed? | Episode `curation_state` and `curation_reason` |
| Is this a possible lesson? | Lesson `candidate` |
| What supports accepting it? | `acceptance_basis` and linked evidence/evaluation |
| Did an agent only retrieve it, use it, or check the result? | Application `stage` |
| Which wording was checked? | `lesson_versions`, such as `lesson-id@2` |
| Has it been added to installed instructions? | `incorporated_ref` and revision |
| Have relevant conditions changed? | `stale` until reviewed |
| Has another lesson replaced it? | `superseded` and `superseded_by` |

An explicit user requirement may be accepted directly. An agent's inferred rule
needs a separate held-out evaluation before acceptance. Technical evidence needs
a source version, the procedure used and the observed result. Filled fields are
not proof: the agent must inspect their sources. The detailed record fields are
in the [memory contract](../../skills/agent-self-improvement/references/project-memory.md).

## Find and use lessons

```sh
python .agents/skills/agent-self-improvement/scripts/learning_memory.py recall --project . --query "component proportions"
```

Recall returns up to ten supported requirements or lessons. It matches words in
content and `keywords`; it does not translate or use embeddings. Add aliases in
the language you use for requests and the language used by the code. An empty
result can mean missing aliases or evidence, not an empty database.

Keep useful lessons after application. Record failed applications too. Only omit
an incorporated lesson with `--covered-by REF@REVISION` after checking that exact
installed rule still covers it. Without this option it remains visible.

## Stop collection

```sh
python .agents/skills/agent-self-improvement/scripts/learning.py status --project .
python .agents/skills/agent-self-improvement/scripts/learning.py pause --project . --client codex --session SESSION_ID
python .agents/skills/agent-self-improvement/scripts/learning.py status --project .
```

Use the actual client/session IDs, not guessed values. Other sessions continue.
`resume` with the same arguments removes that pause without enabling a project
whose collection is off. Use `off --project .` to stop the whole project. Neither
operation removes earlier events, and an in-flight event may already be captured.

## Maintain the database

```sh
python .agents/skills/agent-self-improvement/scripts/learning.py retain --project . --days 30
```

This previews eligible raw events. Add `--apply` to delete them when you want the
cleanup. Thirty days is a starting choice, not an optimal size rule. No recurring
job is created. Evidence-linked events stay; incomplete provenance can pin an
entire session or project. Review that provenance before attempting more cleanup.

Retention preserves structured records, attachments, reports and backups. It does
not reclaim every byte or erase Git history. `purge` is a separate deletion command
and can remove structured memory; do not use it for routine log cleanup.

Manual GitHub push sends only missing record revisions; old packages are retained.
Pull reads the complete set because later packages may refer to earlier records.
A standalone offline export still contains full structured project history.
Raw transcripts, attachments and session pauses are not exchanged.
