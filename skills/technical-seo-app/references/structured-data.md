---
id: 'agents.skills.technical-seo-app.references.structured-data'
title: 'Structured Data'
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

# Structured Data

Use this reference before adding or changing JSON-LD.

## Principles

- Add structured data only when it represents visible page content and a real
  page type.
- Prefer Google-supported rich result schemas only when the page satisfies the
  documented requirements. Otherwise use schema.org types for clarity without
  claiming rich-result eligibility.
- Avoid speculative schema, fake ratings, hidden FAQs, fabricated authorship,
  or fields that do not exist in the content source.
- Keep JSON-LD generation on the server and escape serialized JSON before
  putting it into `dangerouslySetInnerHTML`.

## Common Content Site Types

| Page type | Candidate schema |
|---|---|
| Blog post or essay | `Article` or a more specific article subtype |
| Home page | `WebSite` |
| About or author page | `ProfilePage` plus `Person` |
| Tag or topic page | `CollectionPage` plus `ItemList` |

## Review Checklist

- `@context`, `@type`, URL, headline/name, description, language, image, date,
  and author match visible content and canonical route.
- Article dates use valid ISO strings and distinguish published versus modified
  dates when both exist.
- Tags map to `keywords` or `about` only when they come from validated content
  taxonomy.
- Item lists use stable positions and canonical item URLs.
- Validation instructions point to official Google Rich Results Test or schema
  validation tools, but the agent does not claim live validation unless it was
  actually run.
