#!/usr/bin/env python3
"""Second-pass fix for doubly-generated IDs.

The first pass (fix-double-generated-ids.py) used title-based matching, which
covered titled wikilinks `[[id|title]]` but missed untitled `[[id]]` (no title
to match against existing files). This script catches those by aligning all
wikilinks (titled + untitled) positionally against pre-rename content from the
`sroqnyum` jj revision.

The map in fix-untitled-double-generated-ids.txt was built by:
1. For each wiki file, fetch its pre-rename version via `jj file show -r sroqnyum
   <old-hex>.md` (where old-hex comes from inverse id-map.txt).
2. Extract wikilinks from both pre-rename and current content.
3. Align positionally, skipping cur-side IDs that aren't 12 chars and old-side
   IDs that aren't in id-map.txt.
4. For each pair (cur, old) where cur != idmap[old], record cur as a phantom
   that should map to idmap[old].

Includes 4 manual additions for files where post-rename edits broke positional
alignment, and 2 entries for the Oshi no Ko file that was renamed again after
the original migration (HegvW0RhM8wT/RsFcTVmHyMZh -> rAMmg8OZYt3m).
"""

import re
from pathlib import Path

WIKI_DIR = Path.home() / "wiki"
MAP_FILE = Path(__file__).parent / "fix-untitled-double-generated-ids.txt"

fix_map = {}
with open(MAP_FILE) as f:
    for line in f:
        bad, good = line.strip().split()
        fix_map[bad] = good

print(f"Loaded {len(fix_map)} mappings")

# Match only wikilinks: [[id]] or [[id|title]]
pattern = re.compile(
    r"\[\[(" + "|".join(re.escape(bad) for bad in fix_map) + r")(\|[^\]]*)?\]\]"
)

def replacer(m):
    return f"[[{fix_map[m.group(1)]}{m.group(2) or ''}]]"

wiki_files = list(WIKI_DIR.glob("*.md"))
fixed = 0
total_replacements = 0
for f in wiki_files:
    content = f.read_text()
    new_content, n = pattern.subn(replacer, content)
    if n > 0:
        f.write_text(new_content)
        fixed += 1
        total_replacements += n

print(f"Done. Fixed {fixed} files, {total_replacements} replacements.")
