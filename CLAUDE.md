# Blog Codebase

Jekyll blog that syncs notes from `~/wiki/`.

## Key Files
- `publish-note` / `sync-notes` - Publishing scripts
- `blog_utils.py` - Shared utilities
- `_notes/` - Published posts (`{id}-{slug}.md`)
- `index.html` - Home page with tag filtering

## Testing
- use `jekyll serve` to spin up a development version of the site
- visit the site at http://localhost:4000 to see the rendered version of the site
- tag-filter-tests.html has tests that demonstrate behavior for the tag bar on the main page
