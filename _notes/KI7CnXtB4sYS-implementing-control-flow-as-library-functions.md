---
layout: post
title: "implementing control flow as library functions"
date: 2026-04-23 17:30 -0700
permalink: /KI7CnXtB4sYS/implementing-control-flow-as-library-functions
redirect_from:
  - /KI7CnXtB4sYS
---

With higher order functions it is possible implement most imperative control flow structures as library functions. The key thing to making this work is that the blocks need to be suspended as a thunk so they only executes when they need to.

Lazy languages like Haskell make this very easy, because the thunking is implicit and done maximally by default. It is also possible to suspend computation using parameterless closures in strict languages.

Swift also offers a `@autoclosure` trait that allows wrapping non-closure parameters with parameters. This is useful for `assert` or logging functions that might not need to compute all of their parameters all the time.

Examples:
- bracket operations in Haskell implement [with/using blocks](/KAvQgJqAafP2/with-using-blocks)
- C#/Java/Swift stream processing libraries offer functions like `.ForEach` which executes an action for each element of an `IEnumerable` (analogous to a `for each` loop)
