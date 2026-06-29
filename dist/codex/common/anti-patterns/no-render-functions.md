# No Render Functions

Do not create JSX helpers named `renderXxx`, `xxxRender`, or similar.

Bad:

```tsx
const renderTags = () => tags.map((tag) => <TagBadge key={tag.id} tag={tag} />);

return <div>{renderTags()}</div>;
```

Good:

```tsx
const TagsList = ({ tags }: TagsListProps) => (
    <div>{tags.map((tag) => <TagBadge key={tag.id} tag={tag} />)}</div>
);

return <TagsList tags={tags} />;
```
