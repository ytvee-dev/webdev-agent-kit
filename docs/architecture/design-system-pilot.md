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

This pilot provides templates for trying a design-system workflow on a real
project. Start with one component and record what works and what needs fixing.
It is optional and does not add a Figma editing tool or automatic synchronization
between Figma and code.

## Proposed Workflow

Start with an existing component family, ideally one with variants, tokens and
effects. Inspect the installed code/library and the matching Figma instances
where available. Decide which source to follow for the API, behavior, tokens and appearance.
For example, code may define behavior while Figma defines spacing.

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

The package checks confirm that the templates ship and the test cases can be
prepared. They do not confirm that tools edit Figma correctly, preserve tokens
when moving between Figma and code, or work across different projects. Those
questions need real project trials.
