---
layout: post
title: "easily checking which sum case is used"
date: 2026-04-23 17:19 -0700
permalink: /uDadVZnfjFD5/easily-checking-which-sum-case-is-used
redirect_from:
  - /uDadVZnfjFD5
---

Another practical example of this is checking which case of a sum type something is.

For example consider a simple expression language:
```haskell
data Expr a = Var a | App (Expr a) (Expr a) | Lambda a (Expr a)
```
and suppose we want to write a function that filters a list of expressions for only the variables:
```
filterVars :: [Expr a] -> [Expr a]
```

We can define an auxiliary function in a where clause:
```haskell
filterVars1 = filter isVar where
  isVar (Expr a) = True
  isVar _ = False
```
or we can even use `-XLambdaCase` to write this inline
```haskell
filterVars2 = filter (\case Var _ -> True; _ -> False)
```
but having to do the pattern matching at all is a nuisance.

It would be much nicer to have an operator `is` that would allow writing this like so:
```haskell
filterVars3 = filter (is Var)
```

Swift gets part of the way to implementing this because it allows pattern matching on just the `enum`'s name but it doesn't go all the way because it doesn't allow using patterns as expressions:
```swift
let isVariable = switch expr {
case .variable: true
default: false
}
```
