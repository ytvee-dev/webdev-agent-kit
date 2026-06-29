---
id: 'agents.common.anti-patterns.no-anonymous-functions'
title: 'No Anonymous Functions'
doc_type: 'anti-pattern-template'
layer: 'common'
status: 'active'
publishable: true
local_only: false
tags:
    - 'agents/common'
    - 'anti-patterns/react'
parent:
    - '[[common/anti-patterns/README|Anti-Pattern Templates]]'
related: []
depends_on: []
---

# No Anonymous Functions

## Rule

Use named components, handlers, and helpers. Do not export anonymous components or hide meaningful logic inside unnamed callbacks.

## Bad

```tsx
export default () => {
    return <div>Agents</div>;
};
```

```tsx
<button onClick={() => saveAgent(agent.id)}>Save</button>
```

## Good

```tsx
const AgentsPage = () => {
    return <div>Agents</div>;
};

export default AgentsPage;
```

```tsx
const handleSaveAgent = () => {
    saveAgent(agent.id);
};

<button onClick={handleSaveAgent}>Save</button>
```

## Apply When

Name exported components, event handlers, repeated callbacks, and helpers with behavior.
