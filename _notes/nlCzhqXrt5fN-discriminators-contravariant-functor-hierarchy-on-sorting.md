---
layout: post
title: "Discriminators (contravariant functor hierarchy, O(n) sorting!)"
date: 2026-04-23 17:24 -0700
permalink: /nlCzhqXrt5fN/discriminators-contravariant-functor-hierarchy-on-sorting
redirect_from:
  - /nlCzhqXrt5fN
---

[Fancy way](https://hackage.haskell.org/package/discrimination) of obtaining technically O(n) sorting algorithms for most data types. The way this is achieved is by providing a scalable solution for doing a radix/bucket sort. Other data types are converted to bucket sortable types and compared based on a bucket sort.

[The paper](http://hjemmesider.diku.dk/~henglein/papers/henglein2011a.pdf) is pretty approachable.
