# Structured Data

## Principles

- Add structured data only when it improves clarity for a real page type.
- Keep schema content consistent with visible page content.
- Avoid speculative or misleading structured data just to chase rich snippets.

## Common schema types for content sites

| Page type | Recommended schema |
|---|---|
| Blog post / essay | `Article` |
| Home / landing page | `WebSite` |
| Author / about page | `Person` |

## Rendering pattern

Render structured data as a `<script type="application/ld+json">` tag inside the
Server Component for the page. Do not include it in `generateMetadata`:

```tsx
export default function PostPage({ post }) {
    const jsonLd = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        headline: post.title,
        description: post.description,
        datePublished: post.date,
        author: { '@type': 'Person', name: 'Author Name' },
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

## Validation

Test structured data with Google's Rich Results Test after adding or changing
schemas. Confirm that schema properties match the visible content on the page.
