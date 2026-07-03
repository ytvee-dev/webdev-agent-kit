---
id: 'agents.common.data-visualization-rules'
title: 'Data Visualization Rules'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'frontend/data-visualization'
    - 'quality/ux'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/ui-ux-priority-checklist|UI UX Priority Checklist]]'
    - '[[common/interface-copy-rules|Interface Copy Rules]]'
    - '[[common/performance-review-rules|Performance Review Rules]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on: []
---

# Data Visualization Rules

Purpose: keep charts, metrics, dashboards, and data-heavy UI honest, readable, accessible, and scoped to the user's decision.

Use when implementing, reviewing, or visually verifying charts, KPI cards, dashboards, tables, reports, timelines, funnels, analytics views, financial views, or comparison surfaces.

## Data Honesty

- Do not invent fake metrics, fake trends, fake percentages, or fake business outcomes to make a page look complete.
- If sample data is unavoidable for a static mock, label it clearly as sample data and keep it plausible.
- The visualization must answer a data question, not decorate the page.
- A metric card must communicate what changed, the unit, and the scope when those facts are needed for interpretation.

## Chart Selection

- Trend over time usually favors a line chart or area chart.
- Category comparison usually favors a bar chart.
- Part-to-whole views should avoid pie or donut charts when there are too many categories or small differences.
- Distribution and correlation need chart types that support density or relationship reading.
- For small datasets, direct labels can reduce eye travel.
- For complex datasets, provide filtering, drill-down, grouping, or table fallback only when the product flow needs it.

## Readability And Accessibility

- Do not rely on color alone to differentiate data series, risk, validation, or status.
- Legends, labels, units, axes, and tooltips must be close enough to the data to reduce interpretation cost.
- Interactive chart details must not rely only on hover when touch or keyboard access matters.
- Screen-reader summaries or table alternatives should exist when charts convey critical information and the project has a pattern for them.
- Number, date, currency, and unit formatting should match locale and project conventions when available.

## States

- Empty data must show a meaningful empty state, not a broken chart frame.
- Loading data should reserve enough space to prevent layout shift.
- Error states must explain what failed and provide a retry or recovery path when relevant.
- Stale, partial, delayed, or filtered data must be labeled when that affects decisions.

## Responsive Behavior

- Charts must remain readable on mobile; simplify axes, labels, legends, density, or layout when needed.
- Tables must handle narrow viewports without hiding critical data or forcing uncontrolled horizontal scroll unless the project intentionally uses a data-grid pattern.
- Dashboard density must match the user's scanning task: executive summary, operational monitoring, or drill-down analysis.

## Implementation Boundaries

- Reuse existing charting, table, formatting, data-fetching, CSS Modules, and state conventions.
- Do not install chart libraries, data-grid packages, animation libraries, or formatting packages without explicit approval.
- Do not move data processing into Redux to make visualization components easier to render.

## Validation Gate

Before final reporting, state what question the chart or data surface answers, what states were considered, and whether responsive and accessibility risks remain.
