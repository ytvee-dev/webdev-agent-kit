# AGENTS.md

This file is the generic repo-wide entrypoint for the embedded `AGENTS.md` +
`.agents/` bundle. The canonical publishable copy lives at `.agents/AGENTS.md`,
and the host-project root `AGENTS.md` must stay synchronized with it.

## Bundle Model

- `AGENTS.md` holds generic bundle policy, precedence, and skill discovery.
- `.agents/AGENTS.md` is the canonical publishable copy of this policy file.
- `.agents/common/**` holds reusable shared rules that may be published to the
  shared `webdev-assistant` repository.
- `.agents/project/**` holds host-repo facts, examples, overlays, and local
  addenda only.
- `.agents/skills/**` holds reusable workflows that may be published to the
  shared `webdev-assistant` repository.
- `.agents/` itself is the local checkout of the shared
  `git@github.com:ytvee-dev/webdev-assistant.git` repository.
- `.agents/project/**` is intentionally local-only inside that nested checkout
  and must never be published upstream.

## Inspect First

Before implementation work:

1. Read `AGENTS.md`.
2. Read `.agents/SUMMARY.md`.
3. Load the relevant skill from `.agents/skills/`.
4. Read the relevant `.agents/common/**` docs and `.agents/project/**` overlays.
5. Read the affected source files and configs before changing anything.

Do not skip this order when the task changes code, agent policy, or bundle
structure. Select skills from the user prompt and repo context; the user does
not need to name a skill explicitly.

## Host Project Rules

- Detect project type, stack, routing model, styling system, and verification
  commands from the inspected host repository and `.agents/project/**`.
- Do not store host-project stack facts, architecture, or local examples in
  `AGENTS.md`, `.agents/common/**`, or reusable skill packages.
- Treat `.agents/project/**` as the current host-project context, not as static
  notes.
- After changing host code or documentation structure, update the relevant local
  `.agents/project/**` overlays in the same task.

## Generic Workflow Rules

- Prefer MCP tools and repo-local documentation over broad guesswork whenever
  the required tool or context is available.
- Prefer solutions that do not require installing new packages.
- Before proposing or installing a package, check whether it already exists in
  the host repo and get explicit user approval before installation.
- Do not interact with production systems, production data, or live production
  environments.
- Do not invent architecture, API contracts, or missing implementation details;
  narrow the search and then ask the user if the repo still does not define the
  needed fact.
- Do not modify the host repository root `README.md` unless the user explicitly
  asks for it.

## Upstream Bundle Rules

- Publishable checkout-root bundle content inside `.agents/` is limited to
  `AGENTS.md`, `SUMMARY.md`, `common/**`, `skills/**`, `README.md`, and
  `.gitignore`.
- For `.agents/` documentation git work, use branch names in the form
  `[fix|feat]-[description]`.
- Keep `description` to 1-3 lowercase kebab-case words that summarize the
  grouped documentation commits.
- Do not use numbers, timestamps, ticket ids, repo names, or placeholders such
  as `webdev`, `assistant`, or `bundle` in `.agents/` documentation branch
  names unless the word is the real subject of the change.
- When committing publishable documentation changes in `.agents/`, use
  `fix(docs): <short description>` or `feat(docs): <short description>`.
- Reuse the same core description in the branch name, commit subject, and PR
  title when `webdev-assistant-sync` opens a PR.
- Never publish `project/**`, old helper paths such as `upstream/**`, source
  code, or other host-project files to `webdev-assistant`.
- Use `webdev-assistant-sync` for bundle sync and publication tasks.
- Do not run git publication commands from the host project repository root; run
  them only inside the nested `.agents/` git repository.

## Skill Map

- Task classification and workflow routing -> `webapp-task-protocol`
- Next.js App Router work -> `nextjs-app-router`
- React component architecture and implementation -> `react-component-workflow`
- Redux and shared client-state work -> `redux-state-workflow`
- TypeScript rules and safe refactors -> `frontend-typescript-rules`
- Boundary validation without new dependencies -> `boundary-input-validation`
- Review pass and verification -> `frontend-review-and-fix`
- Agent rules and skill authoring -> `agent-rules-skill-author`
- Bundle sync and upstream publication -> `webdev-assistant-sync`
- Screenshot-based design inspection -> `screenshot-design-inspector`
- Architecture planning from user specs -> `architecture-from-spec`
- Technical SEO audit/fixes -> `technical-seo-app`
- Security audit/reporting -> `frontend-security-inspector`
- Refresh of `.agents/project/*` docs -> `project-context-adapter`

## Common Bundle Docs

- `.agents/common/approved-patterns.md`
- `.agents/common/anti-patterns.md`
- `.agents/common/documentation-maintenance.md`

## Local Project Overlay Docs

- `.agents/project/stack-profile.md`
- `.agents/project/architecture-map.md`
- `.agents/project/styling-profile.md`
- `.agents/project/verification-profile.md`
- `.agents/project/approved-patterns.md`
- `.agents/project/anti-patterns.md`
- `.agents/project/figma-profile.md`
- `.agents/project/react/path-index.md`
- `.agents/project/next/path-index.md`
