# Adaptation Checklist

Use this checklist in Plan Mode to build the project adaptation plan. Do not
edit files while using the checklist in Plan Mode.

## Host Root

- Confirm whether `AGENTS.md` exists at the host project root.
- If missing, plan to create it as a stable pointer to `.agents/AGENTS.md`.
- If present, check whether it mirrors `.agents/AGENTS.md`, points elsewhere,
  or contains unrelated host instructions.
- Plan to keep only the stable pointer unless the canonical policy path itself
  changes.

## Project Shape

Inspect source and config paths while excluding generated, vendor, build, cache,
and tool-output directories.

Collect:

- package manager and scripts;
- framework and router model;
- React version and rendering model;
- TypeScript strictness and module aliases;
- app/source roots;
- route, layout, metadata, sitemap, robots, API route, and server action paths;
- component, hook, utility, content, data, and shared module paths;
- styling system, tokens, global styles, CSS Modules, Tailwind, or design
  system entry points;
- state-management layer, providers, stores, selectors, and client caches;
- validation helpers, schema libraries, route-param parsing, and public
  boundary handling;
- auth, session, secrets, environment variables, public entry points, and other
  security-sensitive surfaces;
- SEO surfaces, structured data, social preview, canonical URL, and crawlability
  implementation;
- Figma/design constraints when present;
- test, lint, typecheck, formatting, build, and preview commands.

## Overlay Plan

Plan updates for the local-only overlays:

- `project/stack-profile.md` - framework, runtime, tooling, package manager,
  TypeScript, state, validation, and verification summary.
- `project/architecture-map.md` - route tree, app/source roots, shared code,
  server/client zones, data flow, and key feature areas.
- `project/styling-profile.md` - styling system, token sources, breakpoints,
  global styles, component styles, and naming conventions.
- `project/verification-profile.md` - relevant checks, order, scope, and known
  blockers.
- `project/approved-patterns.md` - project-specific allowed patterns and local
  examples only.
- `project/anti-patterns.md` - project-specific prohibited patterns,
  exceptions, and local examples only.
- `project/figma-profile.md` - Figma/design-to-code rules when the project has
  them; otherwise plan a minimal placeholder stating no project-specific Figma
  facts were found.
- `project/react/path-index.md` - component, hook, state, style, asset, utility,
  and client UI lookup paths.
- `project/next/path-index.md` - App Router route, layout, metadata, server,
  API, sitemap, robots, and SEO lookup paths when Next.js exists.

## Plan Output

The final Plan Mode response must tell the future implementer exactly which
files to create or update, what facts to put in each overlay, which paths to
avoid, and which verification commands to run after implementation.
