---
layout: post
title: "Editor patterns for file modification"
date: 2026-04-28 16:56 -0700
permalink: /pEciHZHYU5xx/editor-patterns-for-file-modification
redirect_from:
  - /pEciHZHYU5xx
---

These are patterns that editors might use when writing changes to a file after editing it.
- **Truncate-and-rewrite.** `open(path, O_WRONLY|O_TRUNC)`, `write(...)`, `close()`.
- **Modify-in-place.** Same as above but without truncating. Same considerations
- **Write-tempfile-then-rename.** `open("path.tmp.XXX", O_WRONLY|O_CREAT)`, `write(...)`, `fsync()`, `close()`, `rename("path.tmp.XXX", "path")` (e.g. vim)
- **Backup-rename-write.** `rename("path", "path~")`, `open("path", O_WRONLY|O_CREAT)`, `write(...)`, `close()`, optionally `unlink("path~")` (e.g. vim with backupfile=no)
- **macOS-specific atomic replace.** `renamex_np()` with `RENAME_SWAP`, or `FSReplaceObject` from the higher-level APIs. TextEdit, some Apple apps
- **In-place mmap edits.**: (especially anything Electron-based with SQLite, or scientific data tools)
- **Lock files and dotfiles.** Many editors create `.path.lock`, `.~lock.path#`, `.path.swp`, `path.swo`, etc.
