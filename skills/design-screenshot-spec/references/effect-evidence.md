---
id: 'agents.skills.design-screenshot-spec.references.effect-evidence'
title: 'Effect Evidence And Translation'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'design-screenshot-spec'
tags:
    - 'frontend/design'
    - 'verification'
parent:
    - '[[skills/design-screenshot-spec/SKILL]]'
related:
    - '[[skills/design-screenshot-spec/references/design-source-inspection]]'
depends_on: []
---

# Effect Evidence And Translation

Use when the supplied design has depth, translucency, blur, compositing or a
reported visual-effect mismatch. This is read-only inspection and a handoff
contract, not proof that an implementation has matched a real design.

## Acquire The Contributing Layers

1. Match file/revision, node, component instance, state, mode and viewport.
   Inspect the selected layer, relevant ancestors, nested backgrounds and
   instance overrides. A parent's effect or opacity is not the child's property.
2. Capture the matching rendered design and the structured properties or
   legible selected-layer panels. Record provenance for each value. A generated
   CSS snippet alone is insufficient when it omits layers, bindings or effects.
3. Preserve effect order, enabled/disabled status, type and owning layer. For
   shadows, record offset X/Y, blur radius, spread when exposed, color/alpha,
   blend mode and inner/outer type. Record style/variable identity, alias chain,
   resolved value and active mode separately from literal values.
4. Distinguish node/group opacity from fill alpha, layer blur from background
   blur, clipping from masks, strokes from inner shadows and gradients from
   overlays. Capture blend/isolation context, transparent backdrop and geometry
   when they change the effect. Inspect each materially different state.
5. Do not reduce new, progressive, noise, texture, glass or shader effects to a
   familiar shadow/blur. Record the actual exposed type and parameters, plus
   what the tool cannot represent. Tool schemas may expose less than Figma's
   native model; a successful read does not establish complete coverage.

## Evidence States

Use `observed`, `estimated`, `unknown`, `not-exposed` or `unsupported` for each
material property. An explicitly observed disabled effect differs from a missing
effects field. Never fill unread values with zero, normal, none, a guessed token
or an exact-looking color. An inaccessible token alias does not become a literal
source value. Keep unresolved component/token authority in the decision register.

For screenshot-only input, describe the visible result and label approximations;
do not claim to have identified its hidden layer structure or exact parameters.
Request the smallest missing property capture only after available inspection.

## Translation And Verification Handoff

Explain the intended compositing before proposing CSS or assets. Multiple
box-shadows, an inset shadow, a pseudo-element, filter, backdrop-filter and an
exported asset are candidates with different semantics, not interchangeable
translations. A Figma blur radius or blend mode need not match CSS numerically.

For example, parent opacity affects the composite including children, whereas
fill alpha does not reduce child text opacity. Backdrop filtering affects the
area behind a surface and needs appropriate transparency/context; applying a
foreground blur changes the content itself. Do not choose whichever looks
closest in one screenshot without recording the difference.

The handoff ledger contains source/layer, ordered effect properties, binding and
resolved mode, evidence state, proposed implementation, unsupported difference,
and the exact state/background/viewport to compare. Reuse existing tokens and
components only after the mapping is verified. Unapproved visual deviations
remain blocked; independent work may continue.

Verify the implemented result separately through `frontend-visual-qa` against
the captured source: effect order, edges, transparency, clipping, text clarity,
different backgrounds and relevant states. Record intended differences and
rendered evidence; a CSS declaration or passing build is not visual fidelity.
Visual QA consumes captured source evidence and does not acquire Figma itself.

## Source Basis And Field Limit

Checked against [Figma effect types](https://developers.figma.com/docs/plugins/api/Effect/)
and the official `figma/plugin-typings` source, plus MDN
[opacity](https://developer.mozilla.org/en-US/docs/Web/CSS/opacity) and
[backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter).
These explain available concepts, not capabilities guaranteed by a specific MCP.
The issue's original Figma file was not supplied; real-case fidelity remains a
field acceptance task, with failures and unsupported effects retained explicitly.
