---
id: 'agents.skills.technical-seo-app.references.source-refresh'
title: 'Source Refresh'
doc_type: 'skill-reference'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'technical-seo-app'
tags:
    - 'agents/skill-package'
    - 'frontend/seo'
    - 'agents/reference'
parent:
    - '[[skills/technical-seo-app/SKILL|Technical SEO App]]'
related:
    - '[[skills/technical-seo-app/references/audit-rubric|Audit Rubric]]'
depends_on:
    - '[[skills/technical-seo-app/SKILL|Technical SEO App]]'
---

# Source Refresh

Use this reference whenever the task depends on current search-engine,
framework, deployment-platform, webmaster-tool, or AI-crawler behavior.

## Official Source Hierarchy

1. Next.js official docs through Next.js docs MCP for Metadata API, App Router,
   `robots.ts`, `sitemap.ts`, JSON-LD, route handlers, and caching behavior.
2. Vercel official docs for deployment, Speed Insights, Web Analytics,
   AI-tooling, and Markdown access.
3. Google Search Central and Search Console Help for crawling, indexing,
   sitemaps, structured data, Search Console ownership, and AI Search features.
4. Yandex Webmaster Help for Yandex verification, indexing, `robots.txt`, and
   sitemap behavior.
5. Official crawler documentation from providers such as OpenAI or Google for
   crawler user agents and robots controls.

## Mandatory Refresh Cases

- The user asks for "latest", "current", "best practice", webmaster setup,
  AI-search compatibility, Search Console, Yandex Webmaster, crawler rules, or
  ranking-system changes.
- The change touches Next.js Metadata API, `robots.ts`, `sitemap.ts`,
  structured data, AI crawler access, or Vercel-specific observability.
- The recommendation depends on an external product dashboard, validation tool,
  or provider policy.

## Source Notes To Preserve

- Google AI search features use normal Google Search technical requirements and
  controls; do not require a special AI-only metadata file unless Google docs
  change.
- `Google-Extended` is a Google-controlled crawler token for Gemini app and
  Vertex AI grounding/control surfaces, not the same as blocking Google Search
  indexing.
- Vercel and Next.js publish machine-readable documentation surfaces such as
  `llms.txt` and Markdown access for agents; treat those as discoverability
  patterns, not ranking guarantees.
- Search Console and Yandex Webmaster ownership can require code-level proof,
  but the exact token must come from the user or existing repo config.

## Reporting

For every material finding, include the source family used, for example:
`Source: Next.js Metadata docs`, `Source: Google Search Central`, or
`Source: Yandex Webmaster Help`. Include direct links in final answers when
external browsing was used.
