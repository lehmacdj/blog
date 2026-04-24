---
layout: post
title: "self types"
date: 2026-04-23 17:13 -0700
permalink: /6lzBYvOGzs77/self-types
redirect_from:
  - /6lzBYvOGzs77
---

Kind has self dependent function types `f(a : A) -> B(f, a)`. They appear to be based on Self types, which are typically styled ι-types in theory. Apparently these [can do a lot of things](https://github.com/HigherOrderCO/Kind-Legacy/blob/5a6a5e2f2cff35f77176009dfb4c2f1a1bac2799/blog/1-beyond-inductive-datatypes.md) that are hard to do with ordinary function types.

I'm somewhat concerned about the soundness of self types.

The main use case of self types is to implement higher inductive data types without needing to build in native support for them, e.g.:
```
// Natural numbers
Nat: Type
  self(P: Nat -> Type) ->
  (zero: P(Nat.zero)) ->
  (succ: (pred: Nat) -> P(Nat.succ(pred))) ->
  P(self)

// The zero constructor of Nat
Nat.zero: Nat
  (P, zero, succ) zero // same as: "λP. λzero. λsucc. zero"

// The succ constructor of Nat
Nat.succ(pred: Nat): Nat
  (P, zero, succ) succ(pred) // same as: "λP. λzero. λsucc. (succ pred)"

// A recursive function that removes all `succ` constructors
destroy(a: Nat): Nat
  a((a) Nat)(Nat.zero, (a.pred) destroy(a.pred))

// An inductive proof that destroying a natural number results in zero
destroy_theorem(a: Nat): destroy(a) == Nat.zero
  a((a) destroy(a) == Nat.zero, refl, (a.pred) destroy_theorem(a.pred))

// Syntax notes:
// - "self(x: A) -> B" is a self-forall (self-dependent function type)
// - "(f, x) f(f(x))" is a lambda (as in, "λf. λx. (f (f x))")
// - "." is just a name-valid character (so "foo.bar" is just a name)
```
