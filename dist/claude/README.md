# WebDev Assistant

WebDev Assistant is a focused frontend agent skill pack for React and Next.js projects that use CSS Modules, Redux, TanStack, and Axios.

## Target Stack

- React
- Next.js
- CSS Modules
- Redux
- TanStack
- Axios

Other frontend frameworks, styling systems, UI libraries, app generators, and backend tooling are not supported defaults.

## Runtime Source Of Truth

`AGENTS.md` and `skills/**` operate the agent.

`README.md` is only a human-facing repository overview and installation guide.

## Distribution

Source files are the source of truth.

Generated distribution targets are produced from source during packaging or release and must not be used as runtime context or edited manually.

When generated output is needed, rebuild it from source instead of patching `dist/codex` or `dist/claude` directly.
