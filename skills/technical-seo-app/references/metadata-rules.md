---
id: 'agents.skills.technical-seo-app.references.metadata-rules'
title: 'Metadata Rules'
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

# Metadata Rules

Use this reference for metadata, canonical URLs, robots metadata, and social
previews. Confirm current Next.js behavior through Next.js docs MCP before
editing metadata APIs.

## Next.js App Router Rules

- Use `metadata` for static route metadata and `generateMetadata` when metadata
  depends on params, external data, or parent metadata.
- Keep `metadata` and `generateMetadata` in Server Components only.
- Do not export both `metadata` and `generateMetadata` from the same route
  segment.
- Set `metadataBase` at the root layout when relative canonical URLs, Open
  Graph images, or Twitter images are used.
- Remember that nested metadata objects are shallowly merged. A later route
  segment that defines `openGraph` or `robots` replaces that nested object.
- Prefer shared metadata helpers when the repo already has them.

## Content Alignment

- Align title, description, canonical URL, Open Graph, Twitter card, and visible
  page content.
- Keep canonical behavior explicit for every indexable page.
- Use the route's real language/locale and normalize Open Graph locale format
  according to the repo's existing helper.
- Use article Open Graph fields only for article-like pages and include
  published/modified dates when the content model supports them.
- Use tags as a taxonomy signal only when they also exist in visible content,
  structured data, or machine-readable summaries.

## Review Checklist

- Title is route-specific and does not conflict with parent template behavior.
- Description summarizes the visible page, not a hidden marketing variant.
- Canonical URL resolves to the preferred indexable URL.
- Social image path resolves to an absolute URL through `metadataBase` or is
  already absolute.
- `robots` metadata does not accidentally `noindex` published routes.
- Missing or unpublished content returns `noindex` metadata where the app
  renders a not-found or unavailable state.
