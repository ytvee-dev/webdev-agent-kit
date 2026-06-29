# Target Stack Narrowing

Status: active architecture note.

WebDev Assistant targets only React, Next.js, CSS Modules, Redux, TanStack, and Axios.

Source files are the source of truth. Generated `dist/codex/**` and `dist/claude/**` must be rebuilt after source changes.

Agents must not present unrelated frontend frameworks, UI libraries, app generators, or styling systems as supported defaults.

Vite may be mentioned only as an already-detected build tool inside a supported React project. It is not a target app stack for this bundle.

Runtime routing must start from `AGENTS.md`, not `README.md`, `SUMMARY.md`, or generated `dist/**` files.

Stack-specific guidance must prefer local project conventions first, then official documentation for the detected target-stack library.

The target source map is:

- React official docs.
- Next.js official docs.
- CSS Modules documentation and Next.js CSS Modules docs when relevant.
- Redux official docs.
- TanStack Query or Router official docs.
- Axios official docs.
- TypeScript official docs.
- MDN for browser platform behavior.
