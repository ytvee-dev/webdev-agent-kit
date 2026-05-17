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
    []
depends_on:
    - '[[skills/technical-seo-app/SKILL|Technical SEO App]]'
---

# Metadata Rules

## Content alignment

- Align titles and descriptions with the route's actual content.
- Keep canonical behavior explicit for indexable pages.
- Ensure Open Graph fields are coherent with user-facing metadata.
- Treat route-level metadata as a maintained surface, not an afterthought.

## metadataBase

`metadataBase` must be set in the root `layout.tsx` whenever relative paths are
used in Open Graph images, Twitter images, or canonical URLs. Without it,
Next.js cannot resolve relative paths and logs a warning in development; in
production the tags are rendered incorrectly.

## Length limits

| Field | Recommended limit |
|---|---|
| `title` | ≤ 60 characters |
| `description` | ≤ 240 characters |

## generateMetadata is server-only

`generateMetadata()` and the static `metadata` export only work in Server
Components. Adding them to a Client Component has no effect — they are silently
ignored by Next.js.

## Open Graph

- Set `openGraph.type` appropriate to the page: `website` for the home page,
  `article` for blog posts and essays.
- Include `publishedTime` for articles.
- Provide an `ogImage` with explicit dimensions to avoid layout shift in link
  previews.
