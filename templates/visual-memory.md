---
id: 'agents.templates.visual-memory'
title: 'Visual Memory Template'
doc_type: 'template'
layer: 'template'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/template'
    - 'workflow/design-memory'
parent:
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
related:
    - '[[templates/design-direction-contract|Design Direction Contract Template]]'
    - '[[common/anti-template-defaults|Anti-Template Defaults]]'
depends_on: []
---

# Visual Memory

Purpose: local-only hierarchical project memory for accepted, rejected, and repeated visual directions.

Copy this template into `project/visual-memory.md` when a host project needs durable visual memory. Do not publish filled project-specific visual memory in reusable skill packages.

## Precedence

Use the narrowest applicable memory without silently erasing broader decisions:

1. explicit current user or approved design-spec direction;
2. page or flow override for the affected surface;
3. project master direction;
4. reusable defaults from the design skills.

Record why a page override differs from the master direction. If two entries at
the same level conflict, use the most recently approved entry and flag the
conflict during design review.

## Project Master Direction

```text
approved at:
product character:
typography roles:
color and contrast rules:
layout rhythm:
signature elements:
motion model:
global avoid list:
evidence or approval:
```

## Page And Flow Overrides

### Override Entry

```text
date:
page/flow:
overrides master field:
local direction:
reason:
evidence or approval:
expires/review when:
```

## Tried Directions

### Direction Entry

```text
date:
project/screen:
direction:
palette:
typography:
signature element:
result:
avoid repeating:
```

## Strong Local Preferences

```text
- ...
```

## Rejected Defaults

```text
- ...
```

## Successful Patterns

```text
- ...
```

## Avoid Repeating

```text
- ...
```

## Last Updated

...
