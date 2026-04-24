---
layout: post
title: "homoiconicity"
date: 2026-04-23 17:10 -0700
permalink: /NBcoqhpqPI7Q/homoiconicity
redirect_from:
  - /NBcoqhpqPI7Q
---

Property of a programming language that is represented textually such that it has the same structure as it's AST/internal representation. It's only really possible to achieve this in s-expression based languages, i.e. Lisps.

In non-homoicon languages you can still get most of the benefits with quasi-quoters like Haskell has. It allows writing `[t| IO () |]` or `[e| putStrLn "some string" |]` respectively to represent a type or expression. If you also supported robust anti-quoting and using such quasi-quotes in pattern positions, you could write metaprograms similarly to you can in lisp despite the language not really being homoiconic.
