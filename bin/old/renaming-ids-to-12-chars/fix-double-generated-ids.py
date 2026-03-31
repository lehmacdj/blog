#!/usr/bin/env python3
"""Fix doubly-generated IDs in wiki wikilinks."""

import re
from pathlib import Path

WIKI_DIR = Path.home() / "wiki"

# Load fix map
fix_map = {}
with open("/tmp/claude/fix-map.txt") as f:
  for line in f:
    bad, good = line.strip().split()
    fix_map[bad] = good

print(f"Loaded {len(fix_map)} mappings")

# Build single-pass regex
pattern = re.compile(
  r"(?<![A-Za-z0-9])("
  + "|".join(re.escape(bad) for bad in fix_map)
  + r")(?![A-Za-z0-9])"
)

def replacer(m):
  return fix_map[m.group(1)]

# Fix all wiki files
wiki_files = list(WIKI_DIR.glob("*.md"))
fixed = 0
for i, f in enumerate(wiki_files):
  if i % 500 == 0:
    print(f"  {i}/{len(wiki_files)} files...")
  content = f.read_text()
  new_content = pattern.sub(replacer, content)
  if new_content != content:
    f.write_text(new_content)
    fixed += 1

print(f"Done. Fixed {fixed} files.")
