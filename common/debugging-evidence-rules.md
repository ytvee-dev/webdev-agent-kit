---
id: 'agents.common.debugging-evidence-rules'
title: 'Debugging Evidence Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'workflow/debugging'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-bugfix-debugger/SKILL|Frontend Bugfix Debugger]]'
depends_on: []
---

# Debugging Evidence Rules

Purpose: require bugfix work to start from symptoms, reproduction, and evidence.

## Rules

- Record the observed symptom before changing code.
- Reproduce the issue or state why reproduction is blocked.
- Use one bug hypothesis at a time.
- Prefer logs, errors, failing commands, rendered behavior, or source evidence
  over guesses.
- Fix the smallest cause that explains the evidence.
- Verify with the same failing command, route, interaction, or symptom when
  possible.

