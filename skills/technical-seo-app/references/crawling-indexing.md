---
id: 'agents.skills.technical-seo-app.references.crawling-indexing'
title: 'Crawling and Indexing'
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
    - '[[skills/technical-seo-app/references/source-refresh|Source Refresh]]'
    - '[[skills/technical-seo-app/references/ai-agent-discoverability|AI Agent Discoverability]]'
depends_on:
    - '[[skills/technical-seo-app/SKILL|Technical SEO App]]'
---

# Crawling and Indexing

Use this reference for `robots.txt`, sitemaps, crawlability, indexability,
internal linking, and route coverage.

## Source Baseline

- Next.js supports generated `app/robots.ts` and `app/sitemap.ts` metadata file
  conventions. Confirm the current version through Next.js docs MCP.
- Google Search requires Googlebot to be able to fetch the page with HTTP 200,
  read indexable text in the HTML, and access required resources for rendering.
- Sitemaps help discovery, but they do not replace crawlable internal links.
- Yandex Webmaster also supports sitemap discovery through `robots.txt` or
  direct submission.

## Audit Steps

1. Fetch or inspect the generated `robots.txt` behavior and confirm sitemap URLs
   are absolute and production-safe.
2. Inspect sitemap generation and verify coverage for every indexable route
   class: static pages, content detail pages, listing pages, and taxonomy pages.
3. Compare sitemap entries with published content filters, dates, canonical
   paths, route params, and not-found behavior.
4. Check for accidental `noindex`, blocked crawlers, duplicate canonical URLs,
   orphan pages, missing internal links, and environment-specific host mistakes.
5. For dynamic content sources, verify that build-time or cached content loading
   cannot silently omit published pages from sitemap or tag pages.

## Implementation Rules

- Prefer `app/robots.ts` and `app/sitemap.ts` when the repo already uses App
  Router metadata conventions.
- Keep sitemap URLs canonical and absolute.
- Use source content `updatedAt` when available, falling back to publish date.
- Keep crawl blocks narrow and explicit. Do not block AI crawlers or search
  crawlers unless the user asks for that access policy.
- Do not submit or modify live webmaster settings from the agent. Provide the
  code-level setup and verification steps instead.
