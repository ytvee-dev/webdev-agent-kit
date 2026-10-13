---
id: 'agents.docs.architecture.design-system-pilot'
title: 'Draft Design System Pilot'
doc_type: 'guide'
layer: 'docs'
status: 'draft'
publishable: true
local_only: false
tags:
    - 'frontend/design'
    - 'field-testing'
parent:
    - '[[docs/README]]'
related:
    - '[[templates/project/design-system-pilot]]'
    - '[[templates/project/design-system-feedback]]'
    - '[[docs/install/roles]]'
depends_on: []
---

# Draft Design System Pilot

This release ships sketches for owner testing on a real project. They are not
automatically activated, do not add a skill or writing provider, and do not
promise automatic Figma/code synchronization. Stable rules will be shaped by
observed failures and corrections in a later release.

## Proposed Workflow

Start with an existing component family, ideally one with variants, tokens and
effects. Inspect the installed code/library and the matching Figma instances
where available. Choose source authority separately for API, behavior, tokens
and appearance; do not assume Figma or code always wins.

Use [the pilot contract](../../templates/project/design-system-pilot.md) to map
component identity, anatomy, properties, states, aliases, modes, effects and
existing consumers. Mark conflicts, unavailable data and inferred behavior.
The first useful output is a read-only inventory and proposed mapping.

Then authorize one bounded change if useful. Work through available tools and
existing engineering conventions, preserving component APIs, Figma IDs, overrides
and native settings. Inspect partial results before retrying. Library publication,
screen migration, new dependencies and broad token changes need their own scope.

Verify one component in representative states before expansion. Compare source
properties and rendered evidence, and exercise relevant keyboard/focus, long
content, token modes, overrides and existing Storybook stories. Do not invent
mobile behavior or install Storybook solely to fill this template.

## Suggested Field Cases

| Case | What the pilot should reveal |
| --- | --- |
| Local-only system | Reuse actual exports/tokens without demanding Figma |
| Figma and code disagree | Identify ownership and request a decision before dependent writes |
| Instance override | Preserve base identity while recording instance-specific values |
| Mode or alias mismatch | Resolve the right mode and detect missing/cyclic/type-invalid aliases |
| Layered visual effect | Inspect ancestor opacity, effect order, clipping and background separately |
| Partial tool access | Produce a useful bounded inventory with explicit unsupported operations |
| Failed partial write | Reinspect changed state and resume without blind batch replay |

## Feedback For The Next Release

Use [the field-feedback record](../../templates/project/design-system-feedback.md)
in the host's local `.agents/project/`. Keep exact prompts, source revision,
expected/actual behavior, evidence and local corrections. Include a near-miss
where the correction should not apply. The follow-up issue will collect sanitized
results; a local preference does not automatically become a universal rule.

Until those runs occur, extraction accuracy, writing-provider compatibility,
token round-tripping and multi-project behavior remain unverified. This release
validates template distribution and scenario preparation only.
