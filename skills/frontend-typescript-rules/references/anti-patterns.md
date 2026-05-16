# Anti-Patterns

- `any`
- `@ts-ignore`
- unsafe double casts (`value as unknown as Target`)
- broad `Record<string, unknown>` fallbacks where a real type exists
- copy-pasted public types that drift from the source of truth
- `as` type assertions instead of proper narrowing — use type guards or
  discriminated unions to narrow instead of asserting
- `Function` as a type — use a concrete signature: `() => void`,
  `(id: string) => Promise<User>`, etc.
- Excessive generic parameters when a concrete type works just as well
- `object` as a type — use a concrete shape or at minimum `Record<string, unknown>`
