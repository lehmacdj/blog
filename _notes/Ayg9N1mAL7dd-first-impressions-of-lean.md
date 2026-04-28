---
layout: post
title: "First impressions of Lean"
date: 2026-04-27 23:49 -0700
permalink: /Ayg9N1mAL7dd/first-impressions-of-lean
redirect_from:
  - /Ayg9N1mAL7dd
  - /Ayg9N1mAL7dd/initial-lean-impressions
tags: [inkhaven, lean, programming-languages]
---

Since reading [a perfectable programming language](https://alok.github.io/lean-pages/perfectable-lean/) I started getting the itch to try actual dependently typed programming languages again.

[Haskell is my favorite programming language](/GEbCU1EGqkQU/an-expressive-programming-language) because it provides one of the strongest type system but my most common frustrations in Haskell are from not having access to stronger types. [Dependent types in Haskell](https://ghc.serokell.io/dh) are an active research project, but still far away. So when I've wanted more power I've had to make do with Coq (now Roqc) plus a little bit of dabbling in Idris and Agda.

In my usual fashion, I dove right in without reading the tutorial, hoping my experience with similar languages would take me far enough.

## First steps
I started out by just typing out some definitions.
```lean
def x : Int := 1
def y : Type := Int
def z : x := 1
```

I was surprised that the last example failed to compile:
> ▼ 2:14-2:15: error:
> failed to synthesize instance of type class
>   OfNat x 1
> numerals are polymorphic in Lean, but the numeral `1` cannot be used in a context where the expected type is
>   x
> due to the absence of the instance above

This was fixable by using:
```lean
def y : x := (1 : Int)
```

I had a bit of trouble figuring out that Eq.refl needed an argument, but nicely `_` allows inferring the type:
```lean
def x : Type := Int
def y : Int := 1
def z : x = Int := Eq.refl _
```

Of course, I later discovered that there's a `rfl` tactic that allows avoiding this boilerplate.

I also ran into some other surprising sharp edges:
```lean
def decrement : Nat -> Nat
  | 0 => n
  | 1 + n => n
```

Doesn't compile but this does:
```lean
def decrement : Nat -> Nat
  | 0 => n
  | n + 1 => n
```

It's cool that it's possible to pattern match on syntax like this, but it's annoying that it's a bit inconsistent.

## Lambda Calculus Confluence
Basic syntax out of the way, I started implanting the simply typed lambda calculus.

Debrujin indexes:
```lean
inductive Term where
  | var : Nat -> Term
  | lam : Term -> Term
  | app : Term -> Term -> Term
```

Of course, I can't implement a full interpreter because I can't solve the halting problem, so I implement single step semantics:
```lean
def step_cbn (t : Term) : Maybe Term :=
  match t with
  | Term.lam _ => Maybe.nothing
  | Term.var _ => Maybe.nothing
  | Term.app (Term.lam body) t2 =>
      Maybe.just $ shift_down 0 (subst 0 (shift 1 0 t2) body)
  | Term.app t1 t2 => match step_cbn t1 with
    | Maybe.just t1' => Maybe.just $ Term.app t1' t2
    | Maybe.nothing => match step_cbn t2 with
      | Maybe.nothing => Maybe.nothing
      | Maybe.just t2' => Maybe.just $ Term.app t1 t2'
```

There's several different evaluation orders for the simply typed lambda calculus. I recall that Church-Rosser theorem proves that when a term converges, it always converges to the same term regardless of evaluation order.

```lean
inductive ConvergesCBN : Term -> Term -> Type where
  | value : step_cbn v = Maybe.nothing -> ConvergesCBN v v
  | step  : step_cbn e = Maybe.just e' -> ConvergesCBN e' v -> ConvergesCBN e v

inductive ConvergesCBV : Term -> Term -> Type where
  | value : step_cbv v = Maybe.nothing -> ConvergesCBV v v
  | step : step_cbv e = Maybe.just e' -> ConvergesCBV e' v -> ConvergesCBV e v

noncomputable def cbv_implies_cbn_convergence :
  ConvergesCBV e v -> ConvergesCBN e v := sorry
```

I didn't end up making that much progress. I also tried big step semantics, but that ended up not being much easier, and after Codex and Claude found several holes in my definitions, that made the theorem unprovable as stated, I gave up.

## Ecosystem
Lean's ecosystem still feels fairly immature.
- parser libraries: I use megaparsec/attoparsec in Haskell
  - [fgdorais/lean4-parser](https://github.com/fgdorais/lean4-parser): this provides decent parser combinators, but none of the fancier recovery or error handling offered by megaparsec.
- C bindings are possible, but you'll likely need to implement them yourself
- effects: monad transformers are the default way of representing effects; usable, but a far cry from Haskell's wide variety
- tooling quite good, `lean --server` provides top good tooling even in Neovim. I appreciated this compared with using

## A meetup
People writing Lean seem to be very dedicated to verifying things for verifications sake. I love that. I think this is the standard for what should be demanded of our libraries and tools.

I'm curious to try diving into metaprogramming, which I hear is pretty good, but that'll have to wait for another day.
