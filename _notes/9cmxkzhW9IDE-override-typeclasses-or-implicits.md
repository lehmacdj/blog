---
layout: post
title: "override typeclasses or implicits"
date: 2026-04-23 17:22 -0700
permalink: /9cmxkzhW9IDE/override-typeclasses-or-implicits
redirect_from:
  - /9cmxkzhW9IDE
---

This is really important for preventing the restriction of there only being one typeclass per type from being a problem. Having newtypes for each desirable instance does not completely solve the problem by itself.

```
with (Monoid All) (True &lt;> True)
```

```
with (Monoid Any) (uses (someList.traverse) (== x))
```

[givens (Scala 3)](/A2tVR0i9YcsB/givens-scala-3) has a fairly good picture for how this can be implemented.

See also:
- scoped typeclasses or implicits
