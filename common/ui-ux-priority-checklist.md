---
id: 'agents.common.ui-ux-priority-checklist'
title: 'UI UX Priority Checklist'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/design'
    - 'quality/ux'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/design-quality-rubric|Design Quality Rubric]]'
    - '[[common/form-feedback-rules|Form Feedback Rules]]'
    - '[[common/navigation-ux-rules|Navigation UX Rules]]'
    - '[[common/data-visualization-rules|Data Visualization Rules]]'
    - '[[common/icon-quality-rules|Icon Quality Rules]]'
    - '[[common/mobile-responsive-rules|Mobile Responsive Rules]]'
depends_on: []
---

# UI UX Priority Checklist

Purpose: provide a small priority model for frontend UI and UX review so agents check user-impacting risks before aesthetic polish.

Use this checklist when a task changes how a rendered interface looks, feels, moves, communicates state, handles input, or presents data.

## Priority Order

### P0 Accessibility And Operability

Check first because inaccessible UI can block the task completely.

- Interactive elements have visible focus states and semantic roles.
- Icon-only controls have accessible names.
- Text and functional icons have sufficient contrast.
- Color is not the only way to communicate status, validation, or chart meaning.
- Motion respects reduced-motion preferences when motion is present.
- Keyboard and pointer paths both work for critical actions.

### P1 Interaction States And Feedback

- Primary, secondary, disabled, loading, success, error, selected, expanded, and destructive states are distinguishable when relevant.
- Async actions show feedback and prevent duplicate destructive submissions when needed.
- Empty states, errors, and loading states guide the next action instead of filling space.
- The screen has one primary action unless the product workflow requires a different model.

### P2 Layout, Responsive Behavior, And Overflow

- The mobile model is explicit, not inferred from desktop alone.
- No horizontal overflow appears at required small viewports.
- Fixed or sticky headers, sidebars, modals, and toolbars do not hide content.
- Text wraps intentionally and long content has a readable measure.
- Section rhythm, component gaps, and internal control padding follow an intentional scale.

### P3 Forms, Navigation, And Task Completion

- Forms use persistent labels, clear helper text, field-level errors, and recovery paths.
- Navigation exposes the current location and preserves expected back behavior.
- Deep states that need sharing, reload, or return paths are represented by URL or route state when appropriate.
- Destructive actions are separated from ordinary navigation or primary actions.

### P4 Performance And Stability

- Images, fonts, and async content reserve space to reduce layout shift.
- Heavy lists, charts, and client-only surfaces are reviewed for user-visible jank.
- Animation uses transform or opacity when possible.
- Performance claims are evidence-backed; speculative optimizations stay optional.

### P5 Data, Charts, And Numbers

- Charts match the data question and include legends, labels, units, or summaries when needed.
- Data visualizations have empty, loading, and error states.
- Numbers, dates, currencies, and units are formatted consistently.
- Fake metrics are not invented to make a UI look complete.

### P6 Visual Distinctiveness And Polish

Check after the interface is operable, stable, and task-oriented.

- The design direction is subject-grounded.
- Typography, color, layout, and motion choices support the single job.
- Structural devices encode meaning instead of decoration.
- The screen avoids generic template defaults unless the brief explicitly justifies them.

## Output Guidance

When this checklist is used in review, report:

```text
Priority risks checked:
Blocking issues:
High-impact concerns:
Optional polish:
Evidence:
Unknowns or blocked checks:
```

## Validation Gate

Do not treat a visually polished screen as acceptable when P0, P1, or P2 issues block use, comprehension, accessibility, or responsive behavior.
