# Blog Codebase

Jekyll blog that syncs notes from `~/wiki/`.

## Key Files
- `bin/publish-note` / `bin/sync-notes` - Publishing scripts
- `bin/sync-photos` - Publishes captioned photos from the Photos library as `photo`-tagged notes (blog-only: no wiki note; source recorded as `photo: <uuid>` frontmatter, opted-out photos in the gitignored `_ignored-photos.txt` so they stay private; caption edits during triage are written back to Photos; photo posts are untitled unless given a title: `untitled: true` with an auto caption-summary `title` used only for metadata, permalink `/<id>`, rendered as thumbnail + caption in `_includes/note-list.html`, no heading in `post.html`, no `<title>` in feeds)
- `bin/blog_utils.py` - Shared utilities
- `_notes/` - Published posts (`{id}-{slug}.md`)
- `index.html` - Home page with tag filtering

## Testing
- use `jekyll serve` to spin up a development version of the site
- visit the site at http://localhost:4000 to see the rendered version of the site
- run unit tests from the repo root: `PYTHONPATH=bin python3 -m unittest discover -s bin`
- tag-filter-tests.html has tests that demonstrate behavior for the tag bar on the main page
