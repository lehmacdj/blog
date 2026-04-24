---
layout: post
title: "orphan instances"
date: 2026-04-23 17:22 -0700
permalink: /UnwAZzzngQLR/orphan-instances
redirect_from:
  - /UnwAZzzngQLR
---

Regarding [[4ab8aab7]] or similar features in other languages (e.g. [[A2tVR0i9YcsB]]
or traits in Rust) this is a form code smell where the definition site of a type
class instance is not located in the same module where the type or typeclass is
defined. Orphan instances break [[3nJYq6q6JOEA]].

Exactly what an orphan instance is probably affected by several features:
- [[ddgDTcVHs968]]
- [[TChq81fMCv9p]]
- [[9cmxkzhW9IDE]]
