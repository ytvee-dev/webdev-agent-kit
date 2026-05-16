# Validation Patterns

- Validate as close to the input boundary as possible.
- Prefer explicit parsing and small guard helpers over spreading defensive checks
  throughout the call graph.
- Reuse existing project helpers before adding new ones.
- Keep normalization and validation in one place when practical.
- If multiple consumers share the same boundary rule, prefer one shared helper
  with a clear contract over duplicated checks.
