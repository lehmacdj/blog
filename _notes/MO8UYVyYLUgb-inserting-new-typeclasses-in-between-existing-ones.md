---
layout: post
title: "inserting new typeclasses in-between existing ones"
date: 2026-04-23 17:22 -0700
permalink: /MO8UYVyYLUgb/inserting-new-typeclasses-in-between-existing-ones
redirect_from:
  - /MO8UYVyYLUgb
---

Typeclass systems should ideally allow users to define typeclasses that are supertypes of existing typeclasses. For example Selective is a superclass of Monad because it admits an implementation `selectM` that is defined for all Monads. A library providing `Selective` however, can't anticipate every possible type the user might use. So it would be useful to be able to insert a default implementation of Selective for any Monad. e.g.
```haskell
-- this does not compile in Haskell as is because resolving this type of
-- constraint is hard
instance {-# OVERLAPPABLE #-} Monad m => Selective m where
  select = selectM
```

Haskell has needed to revise its typeclass hierarchy because a new better formulation came along that required reparenting various type classes. The primary examples of this are Semigroup => Monoid and Applicative => Monad. These revisions could have been made easier by providing a default instance potentially.
