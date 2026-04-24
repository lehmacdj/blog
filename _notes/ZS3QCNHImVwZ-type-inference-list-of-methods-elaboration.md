---
layout: post
title: "type inference (+ list of methods) / elaboration"
date: 2026-04-23 17:21 -0700
permalink: /ZS3QCNHImVwZ/type-inference-list-of-methods-elaboration
redirect_from:
  - /ZS3QCNHImVwZ
---

Ability of a type system to determine the type of a term. In general undecidable for complicated type systems, however there are fairly good inference schemes for restricted scenarios.
- MLSub (subtypes / subtyping)
- Quicklook (impredicative polymorphism)
- Hindley Milner (full inference for rank 1 types)
- Bidirectional type checking (extensible, relatively easy to implement approach)

Type inference starts to be called elaboration when dependent types get involved, because one often tries to also infer terms. This gets even harder very quickly.
