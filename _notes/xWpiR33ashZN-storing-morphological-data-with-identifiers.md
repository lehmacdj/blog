---
layout: post
title: "storing morphological data with identifiers"
date: 2026-04-23 17:11 -0700
permalink: /xWpiR33ashZN/storing-morphological-data-with-identifiers
redirect_from:
  - /xWpiR33ashZN
---

Refactoring names to make them more descriptive is really useful, however oftenembedding semantic information in names makes renaming painful/expensive. In order to solve this problem it might be possible to allow defining identifiers in terms of other ones.

This might look something like this (using an example from `lens`):
```
on : <identifier-fragment>
of : <identifier-fragment>
{camelCased [`rewrite`, `on`, `of`]} : ASetter s t a b -> ASetter a b a b -> (b -> Maybe a) -> s -> t
```

The idea would be that `on` and `of` would be well-scoped, thus and that the camelCased operator computes a name at compile time to use for the symbol. It would then be a compile error to not rename occurrences of rewriteOnOf when renaming rewrite as well.
