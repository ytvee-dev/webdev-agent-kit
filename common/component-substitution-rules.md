---
id: 'agents.common.component-substitution-rules'
title: 'Component Substitution Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags: []
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/frontend-design-system-rules]]'
depends_on: []
---

# Component Substitution Rules

Load when extending, wrapping, swapping, or reviewing a component that promises
compatibility with another component.

Liskov and Wing's behavioral subtyping requires that clients relying on the
original contract retain their guarantees when a subtype is substituted.
Accepting the same type signature alone is insufficient. See the
[original paper](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf).
The frontend checks below apply that principle to component composition; they
do not require inheritance or a full SOLID redesign.

## Preserve Observable Contracts

- Accept the inputs and states promised by the original API; do not silently
  require an extra provider, nonempty value, or new prop for existing callers.
- Preserve callback payloads, timing, and call count, including cancel/failure.
- Preserve controlled/uncontrolled ownership, defaults, disabled behavior,
  error behavior, and cleanup guarantees.
- Preserve documented ref targets, focus behavior, keyboard activation, and
  semantic roles. Do not advertise button compatibility for an inert element.
- Keep loading and async transitions compatible: a rerender must not duplicate
  a subscription or recreate an owned resource without cleanup.
- A visual variant must not silently change navigation, submission, or state
  persistence.

These checks follow observable caller expectations, not visual similarity.
[React's props guidance](https://react.dev/learn/passing-props-to-a-component)
grounds explicit input contracts; the
[HTML button contract](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button)
grounds native activation and form behavior.

## Concrete Counterexamples

| Replacement | Broken guarantee | Scoped correction |
| --- | --- | --- |
| SaveButton drops disabled before rendering Button | Disabled input can still activate | Forward the supported disabled behavior |
| TextField wrapper calls onChange with a string instead of its promised event | Existing caller cannot read event.target.value | Preserve the event contract or introduce a distinctly named API |
| Link-looking button replaces navigation with submission | Caller expects a URL transition | Keep the navigation primitive or explicitly change the contract |
| Modal wrapper adds another portal and focus owner | Focus/overlay lifecycle has two owners | Reuse the primitive's ownership |
| Compatible variant requires a new provider | Existing valid caller now crashes | Preserve preconditions or expose a separate component |

Use the changed component's actual contract to select relevant checks. Reuse
existing tests or a minimal interaction check. New test authoring follows
`common/test-policy.md`. Do not flag unrelated components or invent defects
merely to demonstrate a principle.
