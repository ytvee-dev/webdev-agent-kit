---
id: "agents.docs.architecture.behavior-evaluation"
title: "Live Behavior Evaluation"
doc_type: "guide"
layer: "docs"
status: "active"
publishable: true
local_only: false
tags: []
parent:
  - "[[AGENTS|Canonical Agent Policy]]"
related:
  - "[[docs/architecture/field-evidence]]"
  - "[[docs/architecture/reproducible-workflows]]"
  - "[[docs/release/0.5.0-checklist]]"
depends_on: []
---

# Live Behavior Evaluation

This experimental harness separates scenario validity, runner execution, and
human-assessed agent behavior. A zero adapter exit code is not a behavior pass.
No model/client success rates are claimed without retained run evidence.

## Prepare And Run

Build targets with `python scripts/build_skill_targets.py`. Use
`python scripts/run_behavior_evals.py --list` to inspect scenario IDs.
Prepare an isolated case outside this repository:

```text
python scripts/run_behavior_evals.py --case save-reload --target codex --output /tmp/webdev-save-eval
```

The output contains `workspace/`, `prompt.txt`, `rubric.json`, and `result.json`.
The prompt names the target instructions and fixture launch command. It does
not expose the expected answer. Start a fresh client in `workspace/`, give it
`prompt.txt`, and keep a transcript outside the workspace. Do not reuse the
implementation conversation for review. For the missing-browser case, disable
browser capability in the actual client rather than merely telling it to pretend.

For repeatable execution, supply a trusted local adapter command after `--`:

```text
python scripts/run_behavior_evals.py --case review-defect --target codex --output /tmp/webdev-review-eval --client codex --model recorded-model-id -- python /absolute/path/to/local-adapter.py
```

The runner appends three absolute arguments: workspace, prompt file, and trace
file. The adapter configures the installed client using its supported interface,
starts a fresh session in that workspace, and records the actual execution trace.
Never put credentials in command arguments. The runner does not install tools,
select an API provider, provision credentials, or bypass the client's sandbox.
Configure the adapter to restrict file access to the fixture; a directory is not
a sandbox. Use local synthetic data and disable production/external actions.
The timeout terminates the adapter process group on POSIX; Windows adapters must
manage their own descendants. No paid run occurs without choosing an adapter.

## Assess Results

Inspect the retained trace and workspace diff against `rubric.json`. Record:

- client/model versions, target, kit commit, and available capabilities;
- observed outcome and evidence location for each rubric item;
- unintended changes, unnecessary questions or tool calls, and verification honesty;
- outcome `passed`, `failed`, `blocked`, or `unverified` with concrete reasons.

Keep `result.json` as runner evidence and write human judgments separately to
`assessment.json`. An unrun case stays `not-run`; a completed adapter remains
`unverified` until its behavior is assessed. Missing traces and timeouts cannot
count as success. Do not publish raw transcripts containing private information.

Repeat relevant cases in fresh workspaces on each supported client; use separate
with-kit and without-kit runs when comparing effect. Never count synthetic
adapter smoke checks as real model evidence. Release stability still requires
the independent project/client reports in Governance.

## Fixture Scope

The dependency-free HTML/JavaScript page deliberately contains a local-storage
persistence defect. It supports CSS scope, debugging, review, blocked-browser,
resume, prototype, glossary, vertical planning, and assumption-analysis cases.
Cases receive only their declared synthetic context; local overlays live under
host `.agents/project/`, including for native plugins. The runner captures
fixture changes and includes kit changes so policy tampering is visible.

## Validation

`python scripts/validate_behavior_evals.py` validates scenario inputs and checks
runner success, missing-trace, timeout, launch-error, and overwrite protection
with a synthetic adapter. It does not execute an AI model.

## Design Sources

The workflows use original kit-specific wording informed by
[Agentic Coding Design Patterns](https://github.com/mokevnin/agentic-coding-design-patterns):
throwaway prototypes, writer/reviewer context separation, tracer-bullet tasks,
domain vocabulary, and feedback loops. Existing kit permissions and lightweight
routing remain authoritative.

## Field-Derived Cases

See [reproducible workflows](reproducible-workflows.md) for bugfix, screenshot,
review, migration, and blocked-verification examples. The
[field evidence guide](field-evidence.md) separates supplied configuration
snapshots from observed agent runs. Screenshot cases require the operator to
capture and attach actual reference PNGs before starting the client.

Record `--client-version`, `--shell`, and repeatable `--capability` values when
using an adapter. These are operator-reported metadata, not verified tool
availability. `result.json` records the runner OS automatically; if an adapter
runs a remote client, record that client's OS separately in the assessment.
`kit_source_dirty` flags uncommitted source changes; the retained file hashes
describe the actual prepared runtime. A source commit alone does not identify
an uncommitted candidate. Cursor fixtures place native rules at the host root,
matching the archive contract.
