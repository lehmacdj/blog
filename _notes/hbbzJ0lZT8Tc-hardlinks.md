---
layout: post
title: "hardlinks"
date: 2026-04-29 21:48 -0700
permalink: /hbbzJ0lZT8Tc/hardlinks
redirect_from:
  - /hbbzJ0lZT8Tc
---

A way of having two files that reference the same underlying data, such that modifying one modifies the other.

In the context of file system implementation, technically a hardlink is just a directory entry associating a name with an [inode](https://en.wikipedia.org/wiki/Inode). Every addressable file has at least one, but in colloquial usage it's more common to only talk about hardlinks when there are multiple for a single inode.

Most file systems support file hardlinks, associating multiple paths to a single inode. Using file hardlinks is fairly brittle.

Directory hardlinks usually aren't supported because they create directory cycles, and most tools that traverse file systems assume a tree structure.

In macOS from OS 10.5 HFS+ supported directory hardlinks and used them for [Time Machine](https://en.wikipedia.org/wiki/Time_Machine_(macOS)). It was possible though risky to create directory hardlinks using the syscall api. APFS removed support for hardlinks in favor of [APFS clones](https://en.wikipedia.org/wiki/Apple_File_System).
