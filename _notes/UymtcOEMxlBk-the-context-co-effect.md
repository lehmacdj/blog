---
layout: post
title: "the context co-effect"
date: 2026-04-23 17:18 -0700
permalink: /UymtcOEMxlBk/the-context-co-effect
redirect_from:
  - /UymtcOEMxlBk
---

Co-effect that is dual to the input effect. Interpreted canonically via the comonad
```haskell
data Product c a = Product c a

instance Comonad (Product c) where
  extract (Product _ x) = x
  duplicate p@(Product c _) = Product c p
```

Useful for referring to additional values in a comonadic context.
