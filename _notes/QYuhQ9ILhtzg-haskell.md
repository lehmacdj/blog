---
layout: post
title: "Haskell"
date: 2026-04-23 17:11 -0700
permalink: /QYuhQ9ILhtzg/haskell
redirect_from:
  - /QYuhQ9ILhtzg
---

See also Haskell Software Engineering

## Flaws
- Not having control flow operators sucks. Especially not being able to return early from a function leads to far too much nesting in common situations where there is a lot of different error handling. But it's not just error handling for which this is a problem, it's also annoying when wanting to short circuit some processing in some situations etc.
- Namespacing is a huge problem. The fact that records/variants aren't scoped to their type name causes name conflicts, and there's also the problem of commonly conflicting names e.g. `catch` for IO monad vs `catch` for Polysemy vs `catch` for UnliftIO all being different.
