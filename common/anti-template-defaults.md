---
id: 'agents.common.anti-template-defaults'
title: 'Anti-Template Defaults'
doc_type: 'common-rule'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'docs/design'
    - 'quality/anti-slop'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
    - '[[common/design-quality-rubric|Design Quality Rubric]]'
depends_on: []
---

# Anti-Template Defaults

Purpose: prevent generic AI-generated frontend design choices from becoming the default visual language.

These styles are not banned. They are suspicious when they appear automatically without a subject-grounded reason.

## Suspicious Defaults

Flag these patterns:

- cream editorial page with serif display and terracotta accent;
- near-black page with acid green or vermilion accent;
- broadsheet or newsprint layout with dense columns and hairline rules;
- generic SaaS hero with gradient blobs;
- fake dashboard metrics used to make a page look complete;
- three-card feature grid without real hierarchy;
- glass cards and glow effects without subject reason;
- random icons used as filler;
- oversized border radius everywhere;
- shadows used as a substitute for hierarchy;
- decorative numbered cards without sequence;
- badges that do not change user understanding;
- timeline layout without actual time or order;
- dashboard layout for content that is not analytical;
- marketing copy that could fit any product.

## Required Challenge

When a suspicious default appears, ask:

```text
What subject-specific reason justifies this choice?
What user job does it support?
What would be lost if it were removed?
Is this a project convention or a model habit?
```

If the answer is weak, remove or replace the pattern.

## Structural Slop

Structural elements must encode meaning.

Avoid:

- numbering without sequence;
- dividers without grouping;
- labels without classification;
- badges without status or semantic difference;
- grids that make unrelated things look equivalent;
- repeated visual motifs that dilute the signature element.

## Replacement Rule

Do not only delete generic defaults. Replace them with subject-grounded structure:

- product workflow;
- actual data hierarchy;
- user decision path;
- domain-specific metaphor;
- meaningful empty/error/loading state;
- one restrained signature element.
