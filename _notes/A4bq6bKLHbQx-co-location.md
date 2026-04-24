---
layout: post
title: "co-location"
date: 2026-04-23 18:47 -0700
permalink: /A4bq6bKLHbQx/co-location
redirect_from:
  - /A4bq6bKLHbQx
---

It should be easy to keep related things close together in the codebase. This gets very hard when considering the expression problem, as it sometimes becomes necessary to split things up by vertical/horizontal.

## Things that should be co-locatable
- [unit tests can be co-located with code](/DB3xJAOpe0Bf/unit-tests-can-be-co-located-with-code).

## Things that maybe should be co-locatable
- co-locatablity of routes with their server implementations

## Beyond the file paradigm
Co-location becomes a somewhat meaningless concept when one is able to work with graphs because anything can be related to arbitrarily many things as opposed to being limited by a file. Unison comes fairly close to achieving this by storing every function individually in a database.
