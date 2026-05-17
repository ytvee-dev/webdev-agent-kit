---
name: technical-seo-app
description: Use when the user request involves technical SEO, metadata,
    canonical URLs, robots, sitemap, crawlability, social previews, or structured
    data in a React or Next.js application.
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
    - '[[skills/technical-seo-app/references/crawling-indexing|Crawling and Indexing]]'
    - '[[skills/technical-seo-app/references/metadata-rules|Metadata Rules]]'
    - '[[skills/technical-seo-app/references/structured-data|Structured Data]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Technical SEO App

## Default workflow

1. Audit the current metadata and crawlability setup.
2. Compare current behavior with the affected routes or pages.
3. Report one of:
    - everything is already aligned, or
    - concrete SEO risks and recommended fixes
4. Apply fixes only when the user asks for implementation.

## Scope

- titles and descriptions
- canonical URLs
- robots and sitemap behavior
- Open Graph / social metadata
- crawlability and indexability
- structured data when appropriate

## Reference map

- `references/metadata-rules.md`
- `references/crawling-indexing.md`
- `references/structured-data.md`
