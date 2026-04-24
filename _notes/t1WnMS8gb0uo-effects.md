---
layout: post
title: "Effects"
date: 2026-04-23 17:17 -0700
permalink: /t1WnMS8gb0uo/effects
redirect_from:
  - /t1WnMS8gb0uo
---

Effects refer to side-effects performed by a computation. Generally these are producer effects, but more generally effects can refer to coeffects / consumer effects as well.
- [Analysis/comparison](https://github.com/lexi-lambda/eff/blob/master/notes/semantics-zoo.md) of the semantics of producer effects in Haskell libraries
- Why use an effect system?

## Producer Effects
Producer effects do things like the following:
- interaction with the environment, i.e. the IO monad in Haskell
- input/reader
- output/writer
- failure
- error handling (throw with catch)
- nondeterministic computation
- state
- more general algebraic effects
- Often capabilities can also be considered effects

Producer can be represented by monads, or more general structures such as productors (see: The Sequential Semantics of Producer Effects) that still provide an interpretation of thunking.
