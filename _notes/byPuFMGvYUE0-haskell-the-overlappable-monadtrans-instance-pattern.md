---
layout: post
title: "Haskell: the OVERLAPPABLE MonadTrans instance pattern"
date: 2026-04-26 23:36 -0700
permalink: /byPuFMGvYUE0/haskell-the-overlappable-monadtrans-instance-pattern
redirect_from:
  - /byPuFMGvYUE0
tags: [unlisted, haskell]
---

A common problem with using MTL style type classes is that you end up needing $$n^2$$ instances.

Suppose you're using the `MonadLsp` class while writing a language server. The lsp package declares instances for `ReaderT`, `IdentityT`, and `LspT`, but if you want to use it with any other monad transformer you need to define your own instance.

Likewise if you're defining a new monad transformer you need to define instances for every `Monad...` class you want to use it with.

This leads to a lot of boilerplate and discourages defining as granular type classes as is common when using more user friendly effect systems.

A solution to this problem is to create `{-# OVERLAPPABLE #-}` instances as follows.

```haskell
instance {-# OVERLAPPABLE #-} (MonadTrans t, MonadLsp c m) => MonadLsp c (t m) where
  getLspEnv = lift . getLspEnv
```

An instance like this is almost always harmless because more than *99.9%* that is exactly the instance that you would have written anyways. But this way you only have to write instances for monads that implement this functionality in a truly novel way, or want to override the behavior in some way.

## More complicated stuff
TODO: explain how to use `MonadTransControl`/`MonadBaseControl` or `MonadUnliftIO` to implement things that are more complicated.

## Prior art
- <https://lukasz-golebiewski.github.io/haskell/effects/2021/01/06/overlappable-instances.html>: explains the core idea and has examples, it's wordier than I like
