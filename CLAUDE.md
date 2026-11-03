# Blog Codebase

Jekyll blog that syncs notes from `~/wiki/`.

## Key Files
- `bin/publish-note` / `bin/sync-notes` - Publishing scripts
- `bin/sync-photos` - Publishes captioned photos from the Photos library as `photo`-tagged notes (blog-only: no wiki note; source recorded as `photo: <uuid>` frontmatter, opted-out photos in `_ignored-photos.txt`)
- `bin/blog_utils.py` - Shared utilities
- `_notes/` - Published posts (`{id}-{slug}.md`)
- `index.html` - Home page with tag filtering

## Testing
- use `jekyll serve` to spin up a development version of the site
- visit the site at http://localhost:4000 to see the rendered version of the site
- run unit tests from the repo root: `PYTHONPATH=bin python3 -m unittest discover -s bin`
- tag-filter-tests.html has tests that demonstrate behavior for the tag bar on the main page
