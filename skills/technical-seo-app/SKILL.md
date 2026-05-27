---
name: technical-seo-app
description: Use when a React or Next.js request involves source-backed technical SEO audit or fixes: metadata, canonical URLs, robots, sitemap, crawlability, indexing, structured data, social previews, Search Console or Yandex Webmaster verification, external content tags/taxonomy, llms.txt, AI crawler access, or AI-agent discoverability. Do not use for marketing copy-only SEO tasks without technical site behavior.
id: 'agents.skills.technical-seo-app.skill'
title: 'Technical SEO App'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'technical-seo-app'
tags:
    - 'agents/skill-package'
    - 'frontend/seo'
    - 'agents/skill'
parent:
    - '[[SUMMARY|Agent Documentation Summary]]'
related:
    - '[[skills/technical-seo-app/references/ai-agent-discoverability|AI Agent Discoverability]]'
    - '[[skills/technical-seo-app/references/audit-rubric|Audit Rubric]]'
    - '[[skills/technical-seo-app/references/crawling-indexing|Crawling and Indexing]]'
    - '[[skills/technical-seo-app/references/external-content-taxonomy|External Content Taxonomy]]'
    - '[[skills/technical-seo-app/references/metadata-rules|Metadata Rules]]'
    - '[[skills/technical-seo-app/references/source-refresh|Source Refresh]]'
    - '[[skills/technical-seo-app/references/structured-data|Structured Data]]'
    - '[[skills/technical-seo-app/references/webmaster-tools|Webmaster Tools]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Technical SEO App

## Purpose

Run source-backed technical SEO audits and implement scoped SEO fixes in React
and Next.js applications without confusing generic marketing optimization with
site behavior.

Treat this as a `.agents`-compatible reusable skill. Keep host-project facts in
`.agents/project/**`; use this package for portable workflow rules.

## Default Workflow

1. Classify the request:
    - audit-only: inspect, compare with current official docs, and report;
    - implementation: inspect, report the intended changes briefly, then edit;
    - webmaster setup: require real verification values from the user or repo;
    - AI discoverability: evaluate crawl access and machine-readable surfaces
      without claiming unverified ranking benefits.
2. Refresh official sources before relying on changing behavior. Read
   `references/source-refresh.md` when the work depends on current Next.js,
   Vercel, Google, Yandex, or AI-crawler behavior.
3. Inspect repo-local SEO context before editing:
    - root and project `AGENTS.md` instructions;
    - relevant `.agents/project/**` overlays, especially any SEO profile;
    - route/path indexes before broad search;
    - affected source files and nearby patterns.
4. Audit the affected surface and produce either:
    - "aligned" with evidence and any residual risk, or
    - findings with severity, evidence, source basis, recommended fix, and
      verification.
5. Apply fixes only when the user asks for implementation or the current
   request is explicitly an implementation request.
6. Verify with the repo verification profile. For docs-only skill changes, run
   skill validation and markdown formatting checks.

## Scope

- Metadata titles, descriptions, canonical URLs, Open Graph, Twitter cards,
  robots metadata, and webmaster verification tags.
- `robots.txt`, sitemaps, crawlability, indexability, redirects, duplicate URL
  handling, internal linking, orphan routes, and noindex behavior.
- Structured data that matches visible content and supported page types.
- Build-time or remote content feeds whose frontmatter, tags, slugs, images,
  dates, and published state drive SEO output.
- Search Console and Yandex Webmaster code-level setup when verification values
  are available.
- AI-agent discoverability through crawl policy, `llms.txt`, Markdown mirrors,
  and documented crawler access controls.

## Source-First Rules

- Use official docs or configured docs MCP before encoding or applying current
  behavior for Next.js, Vercel, Google, Yandex, OpenAI crawlers, or other
  crawler/provider surfaces.
- Prefer Next.js docs MCP for Next.js API and file-convention details.
- Use only primary sources for search-engine rules, webmaster tools, crawler
  tokens, and AI-search behavior.
- Record the source used in audit findings when it materially affects the
  recommendation.
- Do not invent verification tokens, site ownership state, Search Console
  properties, Yandex Webmaster settings, or production crawl results.

## Implementation Rules

- Keep route files thin. Prefer existing SEO helpers, site config, content
  query helpers, and App Router conventions over one-off route logic.
- Validate untrusted route params, content frontmatter, external feed data, and
  user-provided verification values at the boundary already used by the repo.
- Do not add schema-validation packages, analytics tools, crawler services, or
  SEO libraries without explicit user approval.
- Do not fetch the app's own route handlers from server code when direct module
  calls are available.
- Do not treat `keywords` metadata as a primary ranking lever. Use tags and
  keywords to keep site taxonomy, visible content, structured data, and
  machine-readable summaries coherent.
- Keep AI discoverability claims precise: improve access and machine-readable
  context; do not promise ranking or AI answer inclusion unless the official
  source says so.

## Reference Map

- Read `references/source-refresh.md` before audits or fixes that rely on
  current external behavior.
- Read `references/audit-rubric.md` for deep audits and report shape.
- Read `references/metadata-rules.md` for metadata, canonical URLs, social
  previews, and Next.js Metadata API checks.
- Read `references/crawling-indexing.md` for robots, sitemap, crawlability,
  indexing, and internal link coverage.
- Read `references/structured-data.md` before adding or reviewing JSON-LD.
- Read `references/webmaster-tools.md` for Search Console or Yandex Webmaster
  setup that requires code changes.
- Read `references/ai-agent-discoverability.md` for AI crawler access,
  `llms.txt`, Markdown access, and crawler controls.
- Read `references/external-content-taxonomy.md` when SEO depends on external
  content repositories, frontmatter tags, or build-time content feeds.
