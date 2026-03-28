#!/usr/bin/env python3
import re
from pathlib import Path

mapping = {
  "1657d223": "Rna31XL7OHqU",
  "2fdb6119": "qeIskL2GME7w",
  "74aba351": "F0NiTXMRHlLf",
  "89f52db5": "m1hm9H9NxeLD",
  "9b80aaf5": "EaF5QphkhxlD",
  "b1ff90c4": "rGhYCT5cjMgg",
  "de14645c": "1zuNpog5p4DD",
  "df5a7476": "80ez771I2kAJ",
  "fb05acf7": "pI5A62E7dfuR",
}

notes_dir = Path("_notes")
for old_id, new_id in mapping.items():
  matches = list(notes_dir.glob(f"{new_id}-*.md"))
  if not matches:
    print(f"  WARNING: no file for {new_id}")
    continue
  path = matches[0]
  content = path.read_text()

  # Extract slug from permalink
  m = re.search(r"permalink: /" + new_id + r"/(\S+)", content)
  slug = m.group(1) if m else None

  old_bare = f"  - /{old_id}"
  old_full = f"  - /{old_id}/{slug}" if slug else None

  lines = content.split("\n")
  new_lines = []
  in_redirects = False
  for line in lines:
    new_lines.append(line)
    if line.startswith("redirect_from:"):
      in_redirects = True
    elif in_redirects and not line.startswith("  - "):
      # End of redirect block — insert old redirects before this line
      if old_bare not in content:
        new_lines.insert(-1, old_bare)
      if old_full and old_full not in content:
        new_lines.insert(-1, old_full)
      in_redirects = False

  new_content = "\n".join(new_lines)
  if new_content != content:
    path.write_text(new_content)
    print(f"  Updated {path.name}")
  else:
    print(f"  No change {path.name}")
