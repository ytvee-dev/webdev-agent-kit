---
id: 'agents.skills.design-screenshot-spec.references.product-behavior-review'
title: 'Product Behavior Review'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'design-screenshot-spec'
tags:
    - 'frontend/design'
    - 'agents/reference'
parent:
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
related:
    - '[[skills/frontend-design-intelligence/SKILL|Frontend Design Intelligence]]'
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
depends_on: []
---

# Product Behavior Review

Use after inspecting the in-scope design. For a brief without visual sources,
apply the same decision discipline to the supplied product requirements.
Sections cover evidence, decision coverage, question formulation, and handoff.

## Establish What Is Known

Read the user's brief, previous answers, observed design/prototype, and relevant
existing routes/components. Distinguish explicit requirements, observed design
facts, existing implementation behavior, proposals, and unknowns. Existing code
is context; it does not decide whether a new design intends different behavior.

Map the user's goal, entry points, primary action, completion outcome, and each
interactive component. For each action record:

`source/state -> trigger -> destination or resulting state -> feedback/recovery`

Record guards/permissions, data changes, persistence, navigation/back behavior,
and motion only when evidenced or confirmed. A static image of a form is not
evidence of how it appears. Separate visible prototype behavior from production
requirements; a prototype transition does not prove saving or backend semantics.

## Cover The Actual Product Decisions

Review each applicable area below against real components. Mark absent areas
not applicable; do not turn the list into a generic questionnaire or invent
features to fill it. Every unresolved in-scope product/design choice belongs in
the decision register and must be resolved with the user before dependent work.

| Area | Decisions to inspect, then clarify if unresolved |
| --- | --- |
| Entry and navigation | CTA destination, route versus overlay, deep link, back/forward, selected tab, query/filter preservation |
| Forms and overlays | Opening trigger, create/edit mode, prefilling, conditional fields, modal/drawer/inline presentation, close button/Escape/outside click, unsaved input, focus return |
| Submission and data | Required fields, validation timing/messages, loading and duplicate submission, success destination, persistence, cancel/undo, API failure and retry |
| Component states | Default, hover, focus, selected, disabled, loading, empty, error, success; permissions and unavailable actions when relevant |
| Motion | Trigger, start/end states, animated properties, duration/easing/delay, interruption, exit sequence, reduced-motion alternative |
| Responsive use | Stack/order changes, navigation mode, overflow/scroll/sticky regions, touch behavior, missing widths, keyboard/focus operation |
| Product coherence | Primary task clarity, competing actions, terminology, content/source of truth, recoverability, inconsistent behavior between similar controls |

Do not assume a form opens on click, a dialog closes on backdrop, a successful
submit redirects, a filter survives reload, or an unseen animation lasts 200 ms.
Even choosing no animation is a product choice when the motion contract is open.
Preserve existing confirmed accessibility requirements; surface conflicts with
the design and propose a resolution instead of silently changing visible intent.

## Ask Questions That Can Be Answered

For each question include the element/state and evidence, the missing decision,
why it matters to the user, and a concise recommendation with concrete tradeoffs
when useful. Recommendations remain proposals. Avoid jargon, leading choices,
and asking the user to restate facts already visible or previously confirmed.

Example questions after inspection:

- "The Save button and success toast are designed, but the next screen is not.
  Should success keep the edited form open or return to the list? Staying here
  supports repeated edits; returning makes finishing the task more explicit."
- "The creation dialog has a close icon, but no unsaved-input state. Should
  Escape or an outside click discard the draft, retain it, or request confirmation?
  I recommend retaining the draft when reopening to prevent accidental loss."
- "The prototype slides the drawer in, but exit timing and reduced-motion
  behavior are missing. Should closing mirror the entrance, and should reduced
  motion show the drawer immediately?"
- "The mobile reference hides filters without showing an entry point. Should
  they move into a sheet or remain inline below search? The sheet leaves more
  room for results; inline controls make active filters easier to discover."

Ask in small coherent rounds, typically one to three related questions, ordered
by dependencies. Use the host's supported question interface when available,
otherwise plain conversation. Do not stop after a fixed total number of
questions while unresolved decisions remain. A generic planning intake limit
does not authorize guessing design behavior; complete this design-specific
review in subsequent rounds. Keep already answered decisions stable and ask
again only when new evidence conflicts or the user changes the requirement.

If the user defers a decision, mark it unresolved and keep dependent work
blocked. Silence, timeout, a preselected option, and approval to implement the
overall task are not answers to missing product choices. Continue independent
inspection and confirmed work without inventing those choices.

## Decision Register And Handoff

Keep a compact register in the existing spec or local decision log:

`ID | component/state | evidence | question | proposal/tradeoff | user answer/source | status | dependent scope`

Use `open`, `answered`, or `deferred`; only an explicit answer or an existing
confirmed requirement settles a choice. Record which references govern visual
conflicts. Link resolved answers into states/interactions, responsive behavior,
motion, and observable acceptance criteria. Preserve partial progress across
turns so another agent does not reinterpret a proposal as a requirement.

Implementation handoff requires evidence coverage and resolved decisions for
that slice. Never label the entire design ready while dependent questions remain.
Do not use a prototype experiment to choose for the user: ask whether they want
an experiment, retain observations, and obtain the user's decision afterward.

## Source Basis

Reviewed 2026-09-14:

- [Anthropic design critique](https://github.com/anthropics/knowledge-work-plugins/blob/main/design/skills/design-critique/SKILL.md) grounds feedback in specific usability, hierarchy, consistency, and accessibility observations with alternatives and reasons.
- [Anthropic frontend design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) informs subject-specific critique, intentional motion, and user-facing wording. Its creative latitude does not override fidelity or the user-decision gate here.
- [OpenAI skill guidance](https://developers.openai.com/codex/skills) informs explicit inputs/outputs, narrow routing, and progressive disclosure into these references.
