---
layout: post
title: "method notation (with notation)"
date: 2026-04-23 17:18 -0700
permalink: /zOnT5C3LH1V2/method-notation-with-notation
redirect_from:
  - /zOnT5C3LH1V2
---

This notation was originally introduced by Comonads are objects and provides a syntax similar to do notation which makes programming with comonads easier.

I kind of like the framing of calling this with notation better now. It mirrors a helper function `with` that one might use in Swift to get around immutability restrictions:
```swift
lazy var someView = UIView().with { view in
    view.backgroundColor = .red
    view.frame = .zero
    // this is a kind of dumb example sorry but the semantics should be clear
}
```

Sidenote: perhaps seen though this lens mutability makes a coeffect?

## Quotes from the article
This seems interesting to explore:
> Moreover, the idea of using comonads as a more powerful case analysis is strongly suggested by "THE" comonad: the cofree comonad. If you combine the cofree comonad with method syntax, you get a DSL for case analysis on the base functor of the cofree comonad.

The iterator example works equally well:
```
next3 :: Iterator a -> a
next3 = method
    this # next  -- Move one step forward
    this # next  -- Move another step forward
    this # next  -- Return the next value
```

## My original exposition
The main idea is that an expression like:
```haskell
method
  wa> expr1
  expr2
  wc> expr3
```
should desugar like:
```haskell
   \wa ->
let _wb =      extend (\this -> expr1) wa
    wc =      extend (\this -> expr2) _wb
 in extract $ extend (\this -> expr3) wc
```
where expr1, expr2, and expr3 may contain `this` a reference to the "current" comonadic value, which plays a similar role to `this` or `self` in object oriented programming.

In other words, a comonadic computation is expressed as subsequent values of comonadic type composed together. The prompts[^prompt] `wa>` and `wc>` bring previous values into scope for all subsequent statements kind of like creating a copy of an object in the object oriented analogy[^immutability].

$For the language: (Co)effects/(In)equalities/Meta phases I want to try to give the prompts syntax that is closer to como's syntax for saving unpattern matched values, because the method notation and pattern matching syntax seem related to me. See also: pattern matching provides a dual expression language for details on how pattern matching seems comonadic. It is also probably worth investigating what this kind of syntactic sugar should look like in pattern matches.

[^immutability]: Of course, in Haskell everything is immutable so saving copies is pretty cheap.
[^prompt]: This comes from `>` being a common character to end prompts in REPLs.
