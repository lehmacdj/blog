---
layout: post
title: "an expressive programming language"
date: 2026-04-07 22:43 -0700
permalink: /GEbCU1EGqkQU/an-expressive-programming-language
redirect_from:
  - /GEbCU1EGqkQU
tags: [inkhaven, haskell, recommended, programming-languages]
---

I tried naming as may programming languages as I could and came up with these before I got bored: C Rust Perl Bash Zsh Fish Zig C++ D Visual Basic Prolog Racket Elisp VimScript Lua Ruby Idris Agda Rocq C# F# F\* Clojure Kotlin Scala Java ECMAScript TypeScript Raku Python OCaml Standard ML Jai Pony koka Cyclone Unison Swift Objective C Piet J APL Brainfuck Purescript Elm JIF (Java Information Flow) moss LLVM CUDA MLIR x86 ARM MIPS

But Haskell is my favorite.

## Why?
It's expressive. Things that other languages must implement as builtin features, can and are implemented as libraries. This gives you the power to customize the language however you see fit.

In most languages the and `&&` operator needs special compiler treatment to ensure that `false && doSomethingExpensive()` doesn't evaluate `doSomethingExpensive()` unnecessarily. In Haskell laziness gives you this for free. The `&&` operator can be defined in the standard library just like any other function without any special compiler treatment:
```haskell
(&&) :: Bool -> Bool -> Bool
True  && b = b
False && _ = False
```

If you evaluate `False && someExpensiveComputation`, laziness means that the second clause never evaluates `someExpensiveComputation`, the computation only needs to see that the first argument is `False` to produce its result.

But there's a problem with laziness. It makes it hard to predict what order things will get evaluated in, because you need to look at the implementation of your function to know what order its arguments will be evaluated in. For IO like reading a file or printing to the console you need a way to guarantee the order things run in. Haskell adopted `do` notation and monads for this purpose. But it turns out that it's a very general abstraction that generalizes exception handling, `async`/`await`, generators (e.g. `yield`), and many other things.

But so far we've only listed two language features: laziness and monads. By "avoiding success at all costs" Haskell has accumulated decades of experimental language features produced by programming languages research. This allows Haskell to absorb features and express patterns invented in pretty much any other programming language.

RSpec is a Ruby library for writing unit tests. It lets you describe the behaviors of your program using near natural language syntax.
```ruby
RSpec.describe Order do
  it "sums the prices of its line items" do
    order = Order.new
    order.add_entry(LineItem.new(:item => Item.new(
      :price => Money.new(1.11, :USD)
    )))
    order.add_entry(LineItem.new(:item => Item.new(
      :price => Money.new(2.22, :USD),
      :quantity => 2
    )))
    expect(order.total).to eq(Money.new(5.55, :USD))
  end
end
```

Without even needing to resort to [macros](https://wiki.haskell.org/Template_Haskell) HSpec embeds a very similar syntax:
```haskell
spec :: Spec
spec = describe do
  it "sums the prices of its line items" do
    let order = orderFromEntries
      [ LineItem
          { price = Money { value = 1.11, currency = USD }
          , quantity = 1
          }
      , LineItem
          { price = Money { value = 2.22, currency = USD }
          , quantity = 2
          }
      ]
    orderTotal order `shouldBe` Money { value = 5.55, currency = USD }
```

There's even database libraries like squeal that embed SQL syntax in a type safe way without needing macros:
```haskell
getUsers :: Statement DB () User
getUsers = query $ select_
  (#u ! #name `as` #userName :* #e ! #email `as` #userEmail)
  ( from (table (#users `as` #u)
    & innerJoin (table (#emails `as` #e))
      (#u ! #id .== #e ! #user_id)) )
```

Personally that's too many operators and too complicated types even for me, but I like the idea that it's possible in the programming language I use. Maybe someday I'll have a problem for which that complexity is worth it. The thing that I love the most about Haskell is that people do these things even if its not worth it.

Through clever encodings, it's even possible to do anything you can do in a dependently typed programming language/proof assistant like Lean and Rocq with [a little bit extra boilerplate](https://hackage.haskell.org/package/singletons).

## The languages with features I envy
When writing Haskell, there's still some languages left with features that I envy:
- Any programming language with fast compile times: I used to work at a company with a ~2 million lines of code Haskell codebase. It took 3-4 hours to compile from scratch.
- True dependently typed programming languages (like Lean, Idris, Agda, Rocq) are way more ergonomic for any kind of advanced type level programming. Haskell's [working on becoming Dependent Haskell](https://ghc.serokell.io/dh), but it's still a really long way off.
- Languages with better macro systems, mostly Racket, who's macro system is powerful enough to implement [Hackett](https://lexi-lambda.github.io/hackett/), a `#lang` pragma that more or less implements Haskell in Racket.
- Rust: while Haskell has linear types, they are not nearly as mature as Rust's uniqueness types for resource management.
- Prolog: logic programming can be more declarative than laziness.

My dream is a programming language that can subsume all of these features.

## Epilogue
I'm not sure there is a perfect programming language, nor will there probably ever be. Perhaps someday there'll be a programming language that combines all the features I like. [Perhaps Lean will be perfected](https://alok.github.io/lean-pages/perfectable-lean/). But who knows, for now Haskell is still my favorite programming language.
