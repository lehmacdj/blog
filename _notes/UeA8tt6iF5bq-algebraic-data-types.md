---
layout: post
title: "algebraic data types"
date: 2026-04-23 17:20 -0700
permalink: /UeA8tt6iF5bq/algebraic-data-types
redirect_from:
  - /UeA8tt6iF5bq
---

A common language feature in functional programming languages that allows easily declaring types that are a sum of products.

Examples in various languages:
```haskell
data Stuff = Foo {_a :: Int, _b :: Bool} | Bar (Maybe Foo)
```

```ocaml
(* no guarantee this works; I barely remembered OCaml when I wrote this *)
type stuff = foo of (int, bool) | bar of (foo option)
```

```swift
enum Stuff {
  case foo(a: Int, b: Bool)
  case bar(Foo?)
}
```
```

```rust
// same as the OCaml, still good enough to demonstrate basic syntax
enum stuff {
  Foo(i32, bool),
  Bar(Box<stuff>)
}
```

Algebraic data types tend to make it easy to describe data that might come in several different shapes, and also are very good at representing tree like structures.

Essentially they're a single feature bundling together:
- [structs/record types](/3dDEa8tnSN83/structs-record-types)
- coproducts / variants / enums
- [recursive (µ) types](/EJjBX51KQ1Yy/recursive-µ-types)
- [nominative (ν) types](/qQ783yMXPPbQ/nominative-ν-types)

Common object oriented programming languages use a lot of boilerplate when representing ADTs because they represent these as class hierarchies.
