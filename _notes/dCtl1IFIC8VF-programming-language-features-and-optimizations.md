---
layout: post
title: "programming language features (and optimizations)"
date: 2026-04-23 17:12 -0700
permalink: /dCtl1IFIC8VF/programming-language-features-and-optimizations
redirect_from:
  - /dCtl1IFIC8VF
tags: [inkhaven, recommended, programming-languages]
---

My dream programming language would be able to express the syntax and semantics of every other programming language idiomatically. In this framing a good programming language would have few builtins[^builtins] but would still be able to manifest many more specific features as library definitions.

[^builtins]: Features implemented with special support in the compiler. Also sometimes called intrinsics (e.g. by the rust compiler)

I take a very general view of features. Optimizations are included in this list because in order practically exploit the fact that one programming can express the semantics of another, it must be able to match its performance[^why-match-performance]. Thus optimizations are more or less "features" for a programming language; they help determine what the programming language can practically be used for.

[^why-match-performance]: Even though the lambda calculus is Turing complete and can technically implement arbitrary floating point arithmetic, no one is seriously trying to train neural networks using it.

Maximizing which features are expressible as part of the standard library, maximizes what users are able to rewrite. If users don't like the features the language provides in its standard library they can write their own. Such a language is maximally flexible for users.

Of course, actually using custom built features comes at the expense of interoperability with the broader ecosystem. But I think it is better to give users the choice of what they need to interoperate with, rather than artificially restricting it to guarantee good interoperability[^go-lang].

[^go-lang]: This is my largest problem with the philosophy behind the design of go-lang. While true that a simpler language leads to more uniform programming styles, it also makes it harder to build shared abstractions.

With a sufficient floor of metaprogramming capabilities, any feature could be implemented as a builtin or as part of the standard library. I collect this list so that I can sort/consider which features are more primitive and which are the most useful to be able to reprogram. Each programming language features thus becomes both a test and an axiom for programming language expressivity.

*Meta note: I went through and made a bunch of these notes public. There's still a lot of links that aren't public. A lot of the pages themselves are stubs and have highly varying levels of research/detail/revision put into them.*

## [meta programming](/ncxpONlAUxwN/meta-programming)
Features enabling and enabled by metaprogramming. In some sense these are the most important because they're what enables implementing features in terms of each other. I'm also interested in evaluating which of these features are the most irreducible.

Features providing metaprogramming ability:
- [homoiconicity](/NBcoqhpqPI7Q/homoiconicity)
- [get runtime string of compile-time identifier](/QKeZY0XKOiI6/get-runtime-string-of-compile-time-identifier)
- [storing morphological data with identifiers](/xWpiR33ashZN/storing-morphological-data-with-identifiers)
- [compile time execution of code assertion / baking code](/8BHXL4aXonrC/compile-time-execution-of-code-assertion-baking-code)

Features implementable by metaprogramming:
- embedded query languages, e.g. [LINQ](/JJkIIMTFCOS2/linq)
- EDSLs in general get better as metaprogramming is better supported by a programming language

Features kind of like metaprogramming in terms of the expressiveness they provide:
- [overloadable literals](/Z1PKno9u7n88/overloadable-literals)
- [first class patterns](/xHw0NhTYpNsv/first-class-patterns)
- [first class constructor names](/iJCO4lkr7tNY/first-class-constructor-names)
- [first class modules](/zgEZe8EylXt3/first-class-modules)
- [self types](/6lzBYvOGzs77/self-types)
- [Lambda with receiver](/2glFqLPSCCmX/lambda-with-receiver)
- [contextual keywords](/gSlE0WOhgelG/contextual-keywords)
- [raw identifiers](/CPg3TGdClzgM/raw-identifiers)
- [functional tactics languages for proof assistants](/6lFX3b2wE4N9/functional-tactics-languages-for-proof-assistants)

## working with (generally monadic) effects
This category encapsulates language features that make working with effects easier:
- do notation
- [monad extraction](/AfQULF8hGowN/monad-extraction)
- [idiom brackets](/aZQHyB6nrpSg/idiom-brackets)
- lifted versions of boolean operators
- [dedicated syntax for specific effects](/vwO1Erpqe9jg/dedicated-syntax-for-specific-effects)
- [pattern match failures are an effect / parsers via pattern matching](/9prPQE3hGLjS/pattern-match-failures-are-an-effect-parsers-via-pattern-matching)
- [the runtime system should be deeply tied to effect system](/NqZArcVKG3dy/the-runtime-system-should-be-deeply-tied-to-effect-system)
- [Implicit Conversions Between Effects](/kX1jiVaBymWv/implicit-conversions-between-effects)
- See also: [Effects](/t1WnMS8gb0uo/effects)

## working with coeffects
- [method (/with) notation](/zOnT5C3LH1V2/method-with-notation): relatively undeveloped, but interesting
- [coeffects can act as interpreters for effects](/0yMXYaW73qbq/coeffects-can-act-as-interpreters-for-effects): vague but interesting, method notation has some extra ideas for this
- See also: [coeffects / consumer effects](/mxPjuprza4i8/coeffects-consumer-effects)

## concurrency / distributed programming
- [structured concurrency / nurseries](/Nxtt5aJb3FnJ/structured-concurrency-nurseries)
- [async/await](/lNKqn420Niw4/async-await)
- [controlling placement of logic onto specific machines](/yKIqGyLcKXQc/controlling-placement-of-logic-onto-specific-machines)
- [surfacing semantic information about distributed behavior](/dgmN2nnuWwRr/surfacing-semantic-information-about-distributed-behavior)
- [decomposing transactional systems](/65rqGUe3XiKm/decomposing-transactional-systems)

## Working with data
[pattern matching](/GQrJD6Vydss6/pattern-matching):
- [first class patterns](/xHw0NhTYpNsv/first-class-patterns)
- [easily checking which sum case is used](/uDadVZnfjFD5/easily-checking-which-sum-case-is-used)
- [first class constructor names](/iJCO4lkr7tNY/first-class-constructor-names)
- Higher Kinded Data

Accessors / key paths / lenses:
- generic/uniform syntax for arbitrary n-functors/lenses

## optimizations
- [someone's ideal array programming language: ideas about non-uniform compute + SIMD + etc.](https://www.ashermancinelli.com/csblog/2025-7-20-Ideal-Array-Language.html#why-does-this-matter)
- [stream fusion](/5JBEx6WCIHoE/stream-fusion)
- [super compilation](/mUFaDSi2Kni8/super-compilation)
- [equality saturation (e-graphs)](/zncYgtgbNa9x/equality-saturation-e-graphs)

## evaluation order
- [lazy evaluation order / call by name](/2B407TlcHBup/lazy-evaluation-order-call-by-name)
- [call by push value](/svrWWFkcUvTd/call-by-push-value)

## types
Primitive types:
- basic types: [closed vs open types](/48FOjJ7COOaX/closed-vs-open-types)
  - [structs/record types](/3dDEa8tnSN83/structs-record-types)
  - row types (i.e. extensible records)
  - [coproducts / variants / enums](/EdP0HQuZhLDD/coproducts-variants-enums)
  - [polymorphic variants](/XuvkOLlAiCEm/polymorphic-variants)
  - [recursive (µ) types](/EJjBX51KQ1Yy/recursive-µ-types)
  - [nominative (ν) types](/qQ783yMXPPbQ/nominative-ν-types)
  - [algebraic data types](/UeA8tt6iF5bq/algebraic-data-types)
- dependent types:
  - dependent product
  - dependent sum
  - interval / cubic type theory / univalence
  - cumulative universes
- linear types

Broader concepts:
- [type inference (+ list of methods) / elaboration](/ZS3QCNHImVwZ/type-inference-list-of-methods-elaboration)
- [completeness checking](/6QbUR4dyX9Wd/completeness-checking)
- [subtypes / subtyping](/E6doTkK2Znp0/subtypes-subtyping)
- [structural types](/o8Dyaxi0ZKPK/structural-types)
- gradual typing / migratory typing
- pure functions, mutability
  - ST monad

Weird/highly non-standard stuff:
- [dual type operator](/nrO5W22ORJzs/dual-type-operator)
- [co-completeness checking](/6gtykpBojvhd/co-completeness-checking)
- [self types](/6lzBYvOGzs77/self-types)
- [Lambda with receiver](/2glFqLPSCCmX/lambda-with-receiver)
- probably not practical or interesting: [representing types as just namespaces](/Crx6jhw9TK7r/representing-types-as-just-namespaces)


## [typeclasses / traits](/iKz45KVyICwj/typeclasses-traits)
Typeclass features:
- [inserting new typeclasses in-between existing ones](/MO8UYVyYLUgb/inserting-new-typeclasses-in-between-existing-ones)
- [override typeclasses or implicits](/9cmxkzhW9IDE/override-typeclasses-or-implicits)
- [confluent instance resolution](/3nJYq6q6JOEA/confluent-instance-resolution)
- [scoped typeclasses or implicits](/TChq81fMCv9p/scoped-typeclasses-or-implicits)
- [orphan instances](/UnwAZzzngQLR/orphan-instances)
- [givens (Scala 3)](/A2tVR0i9YcsB/givens-scala-3)
- [multiparameter type classes](/ddgDTcVHs968/multiparameter-type-classes)
- [auto derived type classes](/I3MsqrihWOL9/auto-derived-type-classes)

## standard library
The main purpose of a standard library is to define the shared vocabulary that all programs can coordinate around. Because more primitive features are implemented as part of the "standard library", it places an even larger burden on the design of its standard library.

Properties the standard library should have:
- layers of primitiveness: that allow giving up progressive amounts of interoperability for the ability to redefine larger parts of the language
- facilitate migrations between standard library types to make the decision to include/not-include various things as unimpactful as possible

Must haves:
- [type safe dates/times/durations](/9q45qzJgPaIz/type-safe-dates-times-durations)
- OSString type
- theorem proving:
  - [explicitly unordered containers](/ZMtfpDsFf117/explicitly-unordered-containers)

Things to consider adding to a type class hierarchy beyond what Haskell has:
- [Partial Equality / Ordering](/RoZrSQ0VADCE/partial-equality-ordering)
- [Selective](/qy3O2KrKgJYU/selective)
- [Discriminators (contravariant functor hierarchy, O(n) sorting!)](/nlCzhqXrt5fN/discriminators-contravariant-functor-hierarchy-on-sorting)

## modules / scoping
- [first class modules](/zgEZe8EylXt3/first-class-modules)
- [storing morphological data with identifiers](/xWpiR33ashZN/storing-morphological-data-with-identifiers)
- [flexible scope resolution with article like functions/keywords](/x7PUneHXkXAH/flexible-scope-resolution-with-article-like-functions-keywords)
- limited / more local scopes:
  - [local type declarations](/F4TTPLipKTSS/local-type-declarations)
  - [scoped typeclasses or implicits](/TChq81fMCv9p/scoped-typeclasses-or-implicits)
  - [defining functions/global variables over a limited scope](/mpYtVwtsssAa/defining-functions-global-variables-over-a-limited-scope)

## lifetimes / scoping
- [RAII](/dRm9QXhhosuz/raii)
- [defer statement](/dn7y1F0E7gIR/defer-statement)
- [deconstructors / deinitializers](/0FSraZkV6OJ7/deconstructors-deinitializers)
- lifetime annotations ala rust
- borrow checker
- move semantics (e.g. `consume` in Swift)

## control flow
- [implementing control flow as library functions](/KI7CnXtB4sYS/implementing-control-flow-as-library-functions)
- loops:
  - for loops
  - foreach loops
  - [while loop](/sSiTDOesjtyI/while-loop)
  - [until loop](/n4l4TUphkC42/until-loop)
  - do while loop
  - unconditional forever loop
  - [do while with block loop](/4hDfrbOYfERt/do-while-with-block-loop)
- [if statements](/JwjtjzAsEbm9/if-statements)
- [switch / case analysis statements](/Wdj1LjlC97rO/switch-case-analysis-statements)
- [allowing statements to be used as expressions](/T2LKKGgNsdGW/allowing-statements-to-be-used-as-expressions)
- [defer statement](/dn7y1F0E7gIR/defer-statement)
- try { ... } catch { ... }

Dis-preferred:
- [with/using blocks](/KAvQgJqAafP2/with-using-blocks)
- [try { ... } finally { ... }](/VeqfqfVzppXi/try-finally)

## code location / relocating code
- removing indentation from nested code structures
- [unit tests can be co-located with code](/DB3xJAOpe0Bf/unit-tests-can-be-co-located-with-code)
- get calling function location
- [defer statement](/dn7y1F0E7gIR/defer-statement) is useful for putting de-initialization next to initialization logic

## testing
- [unit tests can be co-located with code](/DB3xJAOpe0Bf/unit-tests-can-be-co-located-with-code)
- inspection testing
- unit tests can be discovered at compile time / in the IDE without necessarily running arbitrary code

# See also
- programming language benchmarks for ways of testing what features are useful for programming tasks
- my programming language for features that are core enough to warrant consideration as primitives for my programming language design project
