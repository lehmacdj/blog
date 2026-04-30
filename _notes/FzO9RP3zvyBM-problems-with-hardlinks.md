---
layout: post
title: "problems with hardlinks"
date: 2026-04-29 21:51 -0700
permalink: /FzO9RP3zvyBM/problems-with-hardlinks
redirect_from:
  - /FzO9RP3zvyBM
---

This is for tracking various problems with [hardlinks](/hbbzJ0lZT8Tc/hardlinks).

## Common filesystem system operations can break hardlinks
A common way to atomically modify a file is to make changes to a copy, then moving the copy to replace the original. This breaks hard links. The copy has a separate inode number and moving it only replaces the targeted path, not both.

You can easily replicate this behavior as follows:
```bash
echo 'foo' >foo.txt
echo 'bar' >bar.txt
ln foo.txt hardlink.txt
echo 'The hardlink works' >hardlink.txt
cat foo.txt hardlink.txt
# The hardlink works
# The hardlink works
```

Then doing:
```bash
echo 'Replacement' >replacement.txt
mv replacement.txt hardlink.txt
cat foo.txt hardlink.txt
# The hardlink works
# Replacement
```
