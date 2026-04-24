---
layout: post
title: "programming language features (and optimizations)"
date: 2026-04-23 17:12 -0700
permalink: /dCtl1IFIC8VF/programming-language-features-and-optimizations
redirect_from:
  - /dCtl1IFIC8VF
---

My dream programming language would be able to express the syntax and semantics of every other programming language idiomatically. Each programming language features thus becomes both a test and an axiom for programming language expressivity. In this framing a good programming language would have few builtins (features implemented with special support in the compiler) but would still be able to manifest pretty much any of these features as a special case of its builtins.

Optimizations are included in this list because in order practically exploit the fact that one programming can express the semantics of another, it must be able to match its performance. Even though the lambda calculus is Turing complete and can implement arbitrary floating point arithmetic, no one would try to train a neural network using it. Thus optimizations are more or less be "features" for a programming language with respect to what the programming language can actually be used for.

## [meta programming](/ncxpONlAUxwN/meta-programming)
Features enabling metaprogramming:
- [homoiconicity](/NBcoqhpqPI7Q/homoiconicity)
- [get runtime string of compile-time identifier](/QKeZY0XKOiI6/get-runtime-string-of-compile-time-identifier)
- [storing morphological data with identifiers](/xWpiR33ashZN/storing-morphological-data-with-identifiers)
- [compile time execution of code assertion / baking code](/8BHXL4aXonrC/compile-time-execution-of-code-assertion-baking-code)

Features implementable by metaprogramming:
- embedded query languages, e.g.
  - [LINQ](/JJkIIMTFCOS2/linq)
- EDSLs in general get better as metaprogramming is better supported by a programming language

Features kind of like metaprogramming in terms of the expressiveness they provide:
- [overloadable literals](/Z1PKno9u7n88/overloadable-literals)
- first class patterns
- first class constructor names
- first class modules
- self types
- Lambda with receiver
- contextual keywords
- raw identifiers
- functional tactics languages for proof assistants

## working with (generally monadic) effects
This category encapsulates language features that make working with effects easier:
- do notation
- monad extraction
- idiom brackets
- lifted versions of boolean operators
- dedicated syntax for specific effects
- pattern match failures are an effect / parsers via pattern matching
- the runtime system should be deeply tied to effect system
- Implicit Conversions Between Effects
- See also: Effects

## working with coeffects
- working with coeffects, relatively undeveloped, but interesting: method notation (with notation)
- vague but interesting, some ideas for this are in method notation page above too: coeffects can act as interpreters for effects
- See also: coeffects / consumer effects

## concurrency / distributed programming
- structured concurrency / nurseries
- async/await
- controlling placement of logic onto specific machines
- surfacing semantic information about distributed behavior
- decomposing transactional systems

## Working with data
pattern matching:
- first class patterns
- easily checking which sum case is used
- first class constructor names
- Higher Kinded Data

Accessors / key paths / lenses:
- generic/uniform syntax for arbitrary n-functors/lenses

## optimizations
- [someone's ideal array programming language: ideas about non-uniform compute + SIMD + etc.](https://www.ashermancinelli.com/csblog/2025-7-20-Ideal-Array-Language.html#why-does-this-matter)
- stream fusion
- super compilation
- equality saturation (e-graphs)

## evaluation order
- lazy evaluation order / call by name
- call by push value

## types
Primitive types:
- basic types: closed vs open types
  - structs/record types
  - row types (i.e. extensible records)
  - coproducts / variants / enums
  - polymorphic variants
  - recursive (µ) types
  - nominative (ν) types
  - algebraic data types
- dependent types:
  - dependent product
  - dependent sum
  - interval / cubic type theory / univalence
  - cumulative universes

Broader concepts:
- type inference (+ list of methods) / elaboration
- completeness checking
- subtypes / subtyping
- structural types
- Weird/highly non-standard stuff:
  - dual type operator
  - co-completeness checking
  - self types
  - Lambda with receiver
  - probably not practical or interesting: representing types as just namespaces


## typeclasses / traits
Typeclass features:
- inserting new typeclasses in-between existing ones
- override typeclasses or implicits
- confluent instance resolution
- scoped typeclasses or implicits
- orphan instances
- givens (Scala 3)
- multiparameter type classes
- auto derived type classes

## standard library
Things that belong in the standard library, so that other things may coordinate around them. Ideally the language should be designed so as to facilitate easier migrations between standard library types as much as possible to make the decision to include/not-include these things as unimpactful as possible.
- type safe dates/times/durations
- theorem proving:
  - explicitly unordered containers

Things to consider adding to a type class hierarchy beyond what Haskell has:
- Partial Equality / Ordering
- Selective
- Discriminators (contravariant functor hierarchy, O(n) sorting!)

## modules / scoping
- first class modules
- [storing morphological data with identifiers](/xWpiR33ashZN/storing-morphological-data-with-identifiers)
- flexible scope resolution with article like functions/keywords
- limited / more local scopes:
  - local type declarations
  - scoped typeclasses or implicits
  - defining functions/global variables over a limited scope

## lifetimes / scoping
- RAII
- defer statement
- deconstructors / deinitializers
- lifetime annotations ala rust
- borrow checker
- move semantics (e.g. `consume` in Swift)

## control flow
- implementing control flow as library functions
- loops:
  - for loops
  - foreach loops
  - while loop
  - until loop
  - do while loop
  - unconditional forever loop
  - do while with block loop
- if statements
- switch / case analysis statements
- allowing statements to be used as expressions
- defer statement
- try { ... } catch { ... }

Dis-preferred:
- with/using blocks
- try { ... } finally { ... }

## code location / relocating code
- removing indentation from nested code structures
- unit tests can be co-located with code
- get calling function location
- defer statement is useful for putting de-initialization next to initialization logic

## testing
- inspection testing
- unit tests can be co-located with code
- unit tests can be discovered at compile time / in the IDE without necessarily running arbitrary code

# See also
*NOTE: I haven't gotten around to publishing these yet, links are dead on <https://unformeddelta.wiki>*
- programming language benchmarks for ways of testing what features are useful for programming tasks
- my programming language for features that are core enough to warrant consideration as primitives for my programming language design project
