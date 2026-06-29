# No Anonymous Functions

Use named components, handlers, and helpers.

Bad:

```tsx
export default () => <div>Agents</div>;
```

Good:

```tsx
const AgentsPage = () => <div>Agents</div>;

export default AgentsPage;
```
