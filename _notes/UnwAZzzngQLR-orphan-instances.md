---
layout: post
title: "orphan instances"
date: 2026-04-23 17:22 -0700
permalink: /UnwAZzzngQLR/orphan-instances
redirect_from:
  - /UnwAZzzngQLR
---

Regarding [typeclasses / traits](/iKz45KVyICwj/typeclasses-traits) this is a code smell where the definition site of a type class instance is not located in the same module where the type or typeclass is defined. Orphan instances break [confluent instance resolution](/3nJYq6q6JOEA/confluent-instance-resolution).

Exactly what an orphan instance is probably affected by several features:
- [multiparameter type classes](/ddgDTcVHs968/multiparameter-type-classes)
- [scoped typeclasses or implicits](/TChq81fMCv9p/scoped-typeclasses-or-implicits)
- [override typeclasses or implicits](/9cmxkzhW9IDE/override-typeclasses-or-implicits)
