---
layout: post
title: "dual type operator"
date: 2026-04-23 17:21 -0700
permalink: /nrO5W22ORJzs/dual-type-operator
redirect_from:
  - /nrO5W22ORJzs
---

Hypothetical operator that allows computing the dual of a type.

For example given a type:
```haskell
data Either a b = Left a | Right b
```

You might want to be able to express `Dual (Either a b)` which should be isomorphic to:
```swift
data DualEither a b = DualEither {left :: a, right :: b}
```

One might want this for co-completeness checking.

Maybe you kind of get for free in certain linear logic like type systems (literally the dual relationship?)?
