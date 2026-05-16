# Metadata Patterns

## metadataBase

Set `metadataBase` in the root `layout.tsx`. Without it, relative paths in Open
Graph images, canonical URLs, and other metadata fields are not resolved, and
Next.js logs a warning in development.

```ts
export const metadata: Metadata = {
    metadataBase: new URL('https://example.com'),
}
```

## generateMetadata is server-only

`generateMetadata()` and the static `metadata` export work only in Server
Components. Do not add them to Client Components — they are silently ignored.

## Field length limits

| Field | Recommended limit |
|---|---|
| `title` | ≤ 60 characters |
| `description` | ≤ 240 characters |

Titles longer than 60 characters are truncated in most search engine results.
Descriptions are used for snippet display and should fit in ~2 short sentences.

## Content alignment

- Keep page metadata aligned with the route's real content.
- Reuse validated data when generating titles, descriptions, or Open Graph fields.
- Treat canonical URLs, titles, and descriptions as route-level concerns.
- When a page can be empty or missing, make metadata behavior explicit rather
  than relying on accidental fallback values.

## JSON-LD structured data

Add structured data when the page type benefits from rich results. Render it as
a `<script>` tag inside the Server Component — do not put it in `generateMetadata`:

```tsx
export default function ArticlePage({ post }) {
    const jsonLd = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        headline: post.title,
        datePublished: post.date,
        description: post.description,
    }

    return (
        <>
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
            />
            {/* page content */}
        </>
    )
}
```

Common schema types: `Article` (blog posts, essays), `WebSite` (home page),
`Person` (author / about page).

## Sitemap and robots

Use Next.js file conventions for crawl directives — do not hand-write static files:

- `src/app/sitemap.ts` — exports a function returning sitemap entries
- `src/app/robots.ts` — exports a function returning robots rules
