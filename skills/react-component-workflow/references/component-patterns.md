# Component Patterns

## Orchestration vs presentation

Separate orchestration from presentation when it makes the code easier to
reason about independently.

**Orchestration component** — owns data fetching, async state, business logic,
and conditional rendering decisions. Knows about the data model. Passes results
down as props.

**Presentation component** — receives fully resolved props and renders UI.
No fetching, no business logic, no conditional data wiring.

**When to split:**
- The component mixes data-loading and rendering concerns in a way that makes
  either harder to read or test.
- The presentation can be reused in a different context with different data.
- The component is large enough that reading both concerns together is fatiguing.

**When NOT to split:**
- The component is small and reads clearly as a unit.
- The "presentation" half would need so many props it becomes harder to follow.
- Splitting would create an abstraction with only one caller.

## Composition

- Keep props explicit; avoid hidden coupling through module state or magic imports.
- Prefer composition over wrapper pyramids.
- Extract helpers or child components only when readability or reuse genuinely
  improves — three similar lines of inline JSX is fine; a premature component
  abstraction is not.
- Keep reusable copy, links, and metadata adjacent to the component as explicit
  config objects or neighboring modules instead of hardcoding them deep in JSX.
- Prefer arrow functions for component-local handlers and helpers.

## State ownership

- Own state at the lowest component that needs it.
- Lift state only when two sibling components genuinely need to share it.
- Derive values from existing state instead of creating parallel state that must
  be kept in sync.
- Before adding a new helper or shared component, check whether the repo already
  has a reusable implementation that should be reused or carefully extended.

## Reactive shared-state consumers

- Treat context, selectors, and custom store-like hooks as reactive inputs whose
  identity matters for rerenders.
- Subscribe to the smallest value a component actually needs for rendering or
  control flow.
- When grouped derived data must stay together, prefer a named stable selector
  or store helper over inline object rebuilding at the call site.
- Distinguish service hooks from reactive state hooks: command-oriented hooks
  may safely expose stable callbacks, but reactive state objects should not be
  destructured casually.
