---
layout: post
title: "first class constructor names"
date: 2026-04-23 17:13 -0700
permalink: /iJCO4lkr7tNY/first-class-constructor-names
redirect_from:
  - /iJCO4lkr7tNY
---

It would be really nice if constructor tags were reified into the language and allowed pattern matching on them.

For example, given a data type with three constructors it might be nice write a function converting a value to a string like so:
```haskell
data Op = Add Expr Expr | Sub Expr Expr | Mult Expr Expr

show :: Op -> String
show (constructor e1 e2) =
    let opSym = case constructor of
            | Add -> "+"
            | Sub -> "-"
            | Mult -> "*"
     in show e1 ++ opSym ++ show e2
```

Obviously this is more difficult to support when there are constructors with different numbers of parameters.

See also Pattern Calculus by Barry Jay for a language that implements something like this.
