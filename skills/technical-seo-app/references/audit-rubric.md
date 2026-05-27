---
id: 'agents.skills.technical-seo-app.references.audit-rubric'
title: 'Audit Rubric'
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
depends_on:
    - '[[skills/technical-seo-app/SKILL|Technical SEO App]]'
---

# Audit Rubric

Use this reference for deep SEO audits and review-style responses.

## Audit Surface

- Metadata: title, description, canonical, locale, Open Graph, Twitter cards,
  robots metadata, verification metadata, and metadata inheritance.
- Crawling: `robots.txt`, sitemap, internal links, published filters, route
  generation, not-found behavior, status codes, and duplicate URLs.
- Content: visible headings, descriptions, dates, tags, images, slugs, language,
  author, and source-content validation.
- Structured data: schema type, canonical URL, visible-content parity, dates,
  image URLs, author/entity consistency, and validator follow-up.
- AI discoverability: crawler access policy, `llms.txt`, Markdown summaries,
  content freshness, and provider-specific crawler controls.
- Webmaster tools: code-level verification tokens, sitemap URLs, and dashboard
  actions the user must complete outside the repo.

## Finding Format

Lead with findings ordered by severity:

```text
Severity: high | medium | low
Area: affected route, file, or SEO surface
Evidence: what the repo currently does
Source basis: official source or repo contract used
Risk: concrete crawl/index/share/AI-discovery failure
Fix: scoped code or documentation change
Verification: command, page check, or external validation step
```

If no issues are found, state that clearly and list residual risk, such as
unrun live Search Console inspection or unavailable production crawl data.

## Severity Guide

- High: blocks indexing or ownership verification, exposes wrong canonical
  host, breaks sitemap route generation, or emits misleading structured data.
- Medium: incomplete sitemap coverage, inconsistent metadata, missing social
  previews, weak AI-discoverability surface, or stale taxonomy propagation.
- Low: polish, non-blocking metadata inconsistencies, optional validation
  follow-up, or improvement with unclear impact.

## Implementation Gate

- Audit-only requests stop after the report.
- Implementation requests may edit after the audit summary.
- Verification-token requests stop and ask for the exact token if it is not
  present in repo config or the prompt.
