#!/usr/bin/env python3
"""
Migrate all wiki note IDs that aren't 12-char base62 to new 12-char
base62 IDs. Uses a single-pass regex replacement for efficiency.
"""

import random
import re
import string
from pathlib import Path

WIKI_DIR = Path.home() / "wiki"
BLOG_DIR = Path(__file__).parent.parent.resolve()
NOTES_DIR = BLOG_DIR / "_notes"
IMAGES_DIR = BLOG_DIR / "images"

BASE62 = string.ascii_letters + string.digits


def generate_id():
  return "".join(random.choices(BASE62, k=12))


def is_valid_id(note_id):
  return bool(re.fullmatch(r"[A-Za-z0-9]{12}", note_id))


def build_id_map():
  """Build mapping from old IDs to new 12-char base62 IDs."""
  id_map = {}
  used_ids = set()

  for f in WIKI_DIR.glob("*.md"):
    if f.stem == "index":
      continue
    if is_valid_id(f.stem):
      used_ids.add(f.stem)

  for f in sorted(WIKI_DIR.glob("*.md")):
    if f.stem == "index" or is_valid_id(f.stem):
      continue
    new_id = generate_id()
    while new_id in used_ids:
      new_id = generate_id()
    used_ids.add(new_id)
    id_map[f.stem] = new_id

  return id_map


def make_replacer(id_map):
  """Build a compiled regex + replacement function for single-pass."""
  # Match any old ID that appears as a whole "word" bounded by
  # non-alphanumeric chars (or start/end of string)
  pattern = re.compile(
    r"(?<![A-Za-z0-9])("
    + "|".join(re.escape(old) for old in id_map)
    + r")(?![A-Za-z0-9])"
  )
  def replacer(m):
    return id_map[m.group(1)]
  return pattern, replacer


def main():
  print("Building ID map...")
  id_map = build_id_map()
  print(f"  {len(id_map)} IDs to migrate")

  if not id_map:
    print("Nothing to do.")
    return

  map_path = BLOG_DIR / "tmp~" / "id-map.txt"
  with open(map_path, "w") as f:
    for old_id, new_id in sorted(id_map.items()):
      f.write(f"{old_id} -> {new_id}\n")
  print(f"  ID map written to {map_path}")

  print("Compiling regex...")
  pattern, replacer = make_replacer(id_map)

  # Update wiki file contents (single pass per file)
  print("Updating wiki file contents...")
  wiki_files = list(WIKI_DIR.glob("*.md"))
  for i, f in enumerate(wiki_files):
    if i % 500 == 0:
      print(f"  {i}/{len(wiki_files)} files...")
    content = f.read_text()
    new_content = pattern.sub(replacer, content)
    if new_content != content:
      f.write_text(new_content)

  # Rename wiki files
  print("Renaming wiki files...")
  for old_id, new_id in id_map.items():
    old_path = WIKI_DIR / f"{old_id}.md"
    new_path = WIKI_DIR / f"{new_id}.md"
    if old_path.exists():
      old_path.rename(new_path)

  # Update blog notes
  print("Updating blog notes...")
  if NOTES_DIR.exists():
    for note_path in list(NOTES_DIR.glob("*.md")):
      match = re.match(r"^([A-Za-z0-9]{8,12})(?:-|$)", note_path.stem)
      if not match or match.group(1) not in id_map:
        continue
      old_id = match.group(1)
      new_id = id_map[old_id]

      content = note_path.read_text()
      # Replace IDs in content
      content = pattern.sub(replacer, content)
      # Replace image path prefixes
      content = content.replace(f"{old_id}-", f"{new_id}-")

      new_name = note_path.name.replace(f"{old_id}-", f"{new_id}-", 1)
      new_path = NOTES_DIR / new_name
      new_path.write_text(content)
      if note_path != new_path:
        note_path.unlink()
      print(f"  {note_path.name} -> {new_name}")

  # Rename blog images
  print("Updating blog images...")
  if IMAGES_DIR.exists():
    for img_path in list(IMAGES_DIR.iterdir()):
      for old_id, new_id in id_map.items():
        if img_path.name.startswith(f"{old_id}-"):
          new_name = img_path.name.replace(
            f"{old_id}-", f"{new_id}-", 1
          )
          img_path.rename(IMAGES_DIR / new_name)
          print(f"  {img_path.name} -> {new_name}")
          break

  # Also update index.md references
  index_path = WIKI_DIR / "index.md"
  if index_path.exists():
    content = index_path.read_text()
    new_content = pattern.sub(replacer, content)
    if new_content != content:
      index_path.write_text(new_content)
      print("  Updated index.md references")

  print("Done.")


if __name__ == "__main__":
  main()
