---
id: 'agents.docs.architecture.reproducible-workflows'
title: 'Reproducible Workflow Examples'
doc_type: 'guide'
layer: 'docs'
status: 'active'
publishable: true
local_only: false
tags: []
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[docs/architecture/field-evidence]]'
    - '[[docs/architecture/behavior-evaluation]]'
depends_on: []
---

# Reproducible Workflow Examples

These examples use public synthetic inputs under `evals/live/`. They describe
reproduction and expected contracts, not claimed live agent results. Prerequisite:
Python, a source checkout, and your chosen installed client. Browser cases also
need a callable browser tool; the kit does not install one.

Run `python scripts/build_skill_targets.py`, then prepare each case into a
different empty directory outside this checkout. Example paths below use
`/tmp`; on Windows use distinct absolute directories under your temporary
directory. Available canonical targets: `codex`, `claude-code`, `cursor`.

## Scoped Bugfix And Review

```text
python scripts/run_behavior_evals.py --case save-reload --target codex --output /tmp/webdev-save
python scripts/run_behavior_evals.py --case review-defect --target codex --output /tmp/webdev-review
```

Open the prepared `workspace/` in a fresh client and supply `prompt.txt`.
For browser reproduction, serve that workspace with
`python -m http.server 8765 --bind 127.0.0.1`. Open the page, select dark, save,
and reload. The original page shows success but reads a different storage key
from the one it writes. Use fresh browser storage for each before/after run.

Expected bugfix: align the save/restore contract, demonstrate persistence, and
preserve unrelated CSS. Expected review: explain the defect with file evidence
without editing. Review runs start from their own original fixture and fresh
context, not the bugfix conversation. A storage-exception case is a separate
assumption analysis; do not expand this fix without evidence.

## Screenshot Spec And Rendered Review

```text
python scripts/run_behavior_evals.py --case screenshot-spec --target codex --output /tmp/webdev-spec
python scripts/run_behavior_evals.py --case screenshot-review --target codex --output /tmp/webdev-visual
```

Each output includes a separate `reference/index.html` outside the agent's
workspace. This is a deterministic reference page, not a captured screenshot.

1. Serve `reference/` on port 8766 using the same Python server command with
   that port. Capture PNGs at 960×640 and 375×667 with your existing browser.
   Record browser version, device scale, and viewport. Use the same settings
   for current-page captures.
2. Attach those actual PNGs to the client along with `prompt.txt`. Do not give
   the agent reference HTML as a shortcut to image inspection.
3. For `screenshot-spec`, expect a bounded spec with visible layout/state
   evidence and explicit unknown interactions. Source must remain unchanged.
4. For `screenshot-review`, serve the fixture workspace on port 8765 and
   compare rendered captures. Expected differences include button color,
   content width, and vertical offset; the narrow viewport can affect which
   differences are visible.
5. Retain actual captures and observations. Missing images or unavailable
   rendering mean requested/blocked evidence, never a claimed visual pass.

The fixture is static HTML. Screenshot analysis and visual QA are
framework-agnostic; it does not establish React/Next implementation coverage.
Use `small-color` separately for a minimal CSS change without visual overhead.

## Verification Failure And Confirmation

Prepare `refresh-build-coverage`, `stale-browser-profile`, `windows-shell`,
and `windows-sandbox` with the same command shape.

- Build coverage: inspect scripts, correct the stale local claim, and keep both
  commands not-run because execution was not requested.
- Stale browser: disable browser tools in the actual client for this run. Old
  profile availability does not establish a current screenshot.
- Windows shell: classify the supplied shim block and subsequent real lint
  error in the synthetic log. Do not execute Windows commands on another OS.
- Windows sandbox: retain passed build and blocked rendered verification
  separately; do not restart the failed server.

## Host Migration And Component Contracts

Use `onboarding-existing` to check preservation when replacement is not
authorized, and `migrate-instructions` for explicit migration. Confirm the
original-rule coverage map, backup, reachable local instructions, relative
links, and repeat-run no-op. A plugin-only install must preserve the original
root if shared policy is absent rather than create a dangling pointer.

Use `component-substitution` to review disabled and callback contracts, and
`purpose-names` to check domain naming while preserving external API fields.

## Retain And Assess

Keep `result.json` as runner evidence; attach client version, model, tool
availability, trace, changed files, and per-rubric observations. Write a separate
`assessment.json` with passed/failed/blocked/unverified outcomes. Adapter exit
zero never grades behavior. The [evaluation guide](behavior-evaluation.md)
explains optional adapters and the [report guide](field-evidence.md) describes
public regression contributions.
