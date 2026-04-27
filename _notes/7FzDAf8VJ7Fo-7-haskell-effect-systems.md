---
layout: post
title: "7 Haskell effect systems"
date: 2026-04-26 23:40 -0700
permalink: /7FzDAf8VJ7Fo/7-haskell-effect-systems
redirect_from:
  - /7FzDAf8VJ7Fo
tags: [haskell, inkhaven]
---

An overview of Haskell's effect systems that I've used.

*This was written pretty hastily for Inkhaven. I hope to return to this and add more details later.*

## IO
The simplest "effect system" in Haskell that has been around since the beginning. As an effect system, this just divides functions into pure and impure.

This has a little bit of a special status because Haskell's main function is declared `main :: IO ()`, meaning that all other effect systems must eventually delegate to `IO`.

## mtl
Monad transformers allow extending a monad with extra capabilities. This allows creating large stacks of monad transformers with a bunch of different effects, e.g. `StateT AppState (ExceptT AppError (ReaderT Configuration IO a))`.

This quickly gets unwieldy because effects from lower layers need to be lifted through the upper layers.

`mtl` adds type classes for common kinds of effects, e.g. `MonadState`, `MonadError`, `MonadReader` which can be implemented generically to avoid needing to lift through monad transformers.

As an added benefit this also makes it easier to test functions. A function requiring only `MonadState` can just as easily be implemented using a pure function.

The worst part about `mtl` is that declaring new effects requires implementing every relevant type class when declaring a new effect. Conversely, implementing a new type class requires adding an implementation for every relevant monad transformer.

This is called the $$n^2$$ instances problem. It's possible to work around this for the most part with [Haskell: the OVERLAPPABLE MonadTrans instance pattern](/byPuFMGvYUE0/haskell-the-overlappable-monadtrans-instance-pattern), but it still requires more boilerplate than other effect systems we will see.

## ReaderT IO / unliftio
`ReaderT IO` makes the observation that most custom effects can easily be represented by `IO` anyways.

Instead of implementing `MonadState` with `StateT` it can just as easily be implemented by manipulating an `IORef` in `IO`. Why use separate exceptions from `ExceptT` when `IO` exceptions can achieve the same purpose?

Because extra parameters are still annoying to pass around, it's common to still use the `ReaderT` type to remove boilerplate associated with passing them.

Finally, `unliftio` makes it easier to express higher order operations like bracket. Because `ReaderT` isn't stateful it's possible to "unlift" it, which makes it possible to represent more generic error handling operations.

It remains a little bit hard to define custom effects and reinterpret them flexibly with this approach. To implement a pure version of an effect, you still often end up stuck with the complexity of monad transformer stacks and the $$n^2$$ instances problem.

## polysemy
Algebraic effect systems attempt to get rid of the boilerplate involved in defining custom type classes for effects once and for all. They also try to implement fancier algebraic effect patterns.

Based on the weaving pattern introduced by [Effect Handler's in Scope](https://www.cs.ox.ac.uk/people/nicolas.wu/papers/Scope.pdf), this library is based on free monads, keeping track of an open union of capabilities.

## fused-effects
`fused-effects` is pretty much like `polysemy` but uses type classes instead of an open union. This provides a bit more efficiency at runtime trading off for greater boilerplate.

## in-other-words
`in-other-words` is the most creative effect system I've seen so far. It provides a really ergonomic interface by providing granular primitive effects that encapsulate higher order effect patterns. User defined effects can be translated into these effects, which makes gets rid of some of the complexity imposed by polysemy and fused-effect's weaving pattern.

In practice its biggest flaw is its lack of documentation, and the raw complexity of the effects it offers. Some of its effects are extremely general, and reasoning through how they can be instantiated into something useful is really hard.

## effectful
Effectful is the application of `ReaderT IO` / unliftio's lessons to algebraic effect systems. It implements everything in terms of IO, but wraps it up in a neat interface that makes it easier to work with.

It's also able to provide a reasonably safe pure interface.

This is currently my favorite effect system for new projects.
