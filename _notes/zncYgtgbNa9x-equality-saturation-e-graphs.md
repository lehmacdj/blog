---
layout: post
title: "equality saturation (e-graphs)"
date: 2026-04-23 17:20 -0700
permalink: /zncYgtgbNa9x/equality-saturation-e-graphs
redirect_from:
  - /zncYgtgbNa9x
---

An approach for efficiently, exhaustively applying a bunch of rewrite rules.

The approach is to encode an AST as a set of equivalence classes. This allows exhaustively rewriting terms to "saturate" the equality classes, after which an optimal (measured by a cost function) expression can be extracted. It's possible to work over multi-colored e-graphs to allow using rewrites that are only applicable in certain contexts.

See also:
- [egg](https://egraphs-good.github.io/): a library that implements efficient e-graph algorithms
- [Samuel Coward's Equality Saturation for Circuit Synthesis and Verification](<attachments/Thesis_Imperial.pdf>): a thesis that I found through the PLDG listserve that includes a nice description of equality saturation/e-graphs
