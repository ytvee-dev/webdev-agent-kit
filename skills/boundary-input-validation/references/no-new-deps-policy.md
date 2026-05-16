# No New Dependencies Policy

- Start by checking `package.json`, existing helpers, and existing call sites.
- Prefer built-in language/runtime features and existing repo utilities first.
- If a package truly appears necessary, confirm that it is not already installed
  and request user approval before any install.
- Do not introduce schema validation libraries unless the user explicitly
  approves them.
