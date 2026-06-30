---
id: 'agents.common.anti-patterns.no-tests-for-components-or-functions'
title: 'No Tests For Components Or Functions'
doc_type: 'anti-pattern-template'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'anti-patterns/testing'
parent:
    - '[[common/anti-patterns/README|Anti-Pattern Templates]]'
related:
    - '[[common/lint-verification-rules|Lint Verification Rules]]'
depends_on: []
---

# No Tests For Components Or Functions

## Rule

Do not create tests for components or functions.

## Bad

```tsx
import { render } from '@testing-library/react';

it('renders tag selector', () => {
    render(<TagSelector />);
});
```

## Forbidden Files And Setup

- Test files for components or functions.
- Unit test setup.
- Component test setup.
- End-to-end test setup.
- Visual regression test setup.
- New test scripts or test dependencies.

## Good

- Run the existing lint command.
- Run existing typecheck or build commands when available.
- Use rendered UI verification for visual changes.
- Document what was checked.

## Apply When

Use this whenever an agent considers adding tests, test scripts, test dependencies, or test framework setup.
