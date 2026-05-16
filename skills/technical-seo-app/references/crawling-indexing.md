# Crawling and Indexing

## General checks

- Check robots behavior for the affected environment.
- Confirm sitemap coverage for indexable pages.
- Look for accidental `noindex`, duplicate routes, or orphaned internal pages.
- Verify internal linking when new sections or routes are introduced.

## Next.js 16 file conventions

Use the built-in file conventions rather than static files in `/public`:

**`src/app/sitemap.ts`** — generates `sitemap.xml` dynamically. Export a default
function returning an array of sitemap entries:

```ts
export default function sitemap(): MetadataRoute.Sitemap {
    return [
        { url: 'https://example.com', lastModified: new Date() },
        { url: 'https://example.com/posts', lastModified: new Date() },
    ]
}
```

**`src/app/robots.ts`** — generates `robots.txt` dynamically:

```ts
export default function robots(): MetadataRoute.Robots {
    return {
        rules: { userAgent: '*', allow: '/' },
        sitemap: 'https://example.com/sitemap.xml',
    }
}
```

Both files are automatically served by Next.js at `/sitemap.xml` and
`/robots.txt`. They replace hand-written static files in `/public`.
