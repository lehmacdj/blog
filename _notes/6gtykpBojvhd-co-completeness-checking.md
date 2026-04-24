---
layout: post
title: "co-completeness checking"
date: 2026-04-23 17:21 -0700
permalink: /6gtykpBojvhd/co-completeness-checking
redirect_from:
  - /6gtykpBojvhd
---

It would be really neat to also be able to optionally invoke completeness checking in the dual situation to the one where one typically does.

For example, when writing a parser you often want to make sure you've implemented a parser for each case of a [coproducts / variants / enums](/EdP0HQuZhLDD/coproducts-variants-enums). It would be neat if one could automatically derive a [dual type operator](/nrO5W22ORJzs/dual-type-operator) and use completeness checking to ensure that each variant is covered.

Strictly speaking, perhaps co-completeness checking is what I call [completeness checking](/6QbUR4dyX9Wd/completeness-checking) for records, and the actual desire expressed by this note is the ability to explicitly represent the dual of a [coproducts / variants / enums](/EdP0HQuZhLDD/coproducts-variants-enums). Perhaps the dual type could explicitly be used as part of the implementation of pattern matching.
