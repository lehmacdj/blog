---
layout: post
title: "first class modules"
date: 2026-04-23 17:13 -0700
permalink: /zgEZe8EylXt3/first-class-modules
redirect_from:
  - /zgEZe8EylXt3
---

Passing around modules as functions is a very powerful capability and allows emulating a lot of other language features in combination with a few other things:
- with abstract types in modules you can emulate GADTs: http://lambda-the-ultimate.org/node/4101
- together with implicit arguments it can also be used to implement something similar to type classes by using the module as the type class dictionary

This is a fairly large pain point in Haskell, here are some proposals for improving Haskell's module system that provide interesting insights into what design decisions can cause large problems further down the road:
- Less ambitious [proposal](https://github.com/goldfirere/ghc-proposals/blob/1d2c9154dcbe3d063757a1a90ff34ed57a58efdf/proposals/0000-local-modules.rst) that does a good job of showcasing some of the flaws in GHC's module system that caused a more amitious proposal to not be possible
- More ambitious [proposal](https://github.com/michaelpj/ghc-proposals/blob/a8613d0f0410334e7609fa02785608f255e6f8bf/proposals/0000-first-class-modules.rst): probably too much to implement in GHC, but good design ideas for a new language

## Implementation notes
Typically first class modules are implemented as a fancy dependent record. It would be good to unify the implementation of records with the implementation of modules ideally.
