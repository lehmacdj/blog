---
layout: post
title: "coeffects can act as interpreters for effects"
date: 2026-04-23 17:18 -0700
permalink: /0yMXYaW73qbq/coeffects-can-act-as-interpreters-for-effects
redirect_from:
  - /0yMXYaW73qbq
---

This is currently more of wish than a true fact. But here are some motivating examples to suggest why this might be the case:

Consider a reader/input effectful computation:
```
addInput3Times : {input int} int
addInput3Times = !input + !input + !input
```
one strategy for evaluating this is to provide it with a constant value:
```
runInputConst : int -> forall a. {input int} a -> a
```
we can alternatively view this as adjoining [the context co-effect](/UymtcOEMxlBk/the-context-co-effect) and then evaluating via via the adjunction between Product and Reader.
```
-- given:
context : forall a. int -> a -> [context int] a
eval : forall a. [context int] {input int} a -> a

-- we can do:
eval (context 3 addInput3Times)) = 9
```
