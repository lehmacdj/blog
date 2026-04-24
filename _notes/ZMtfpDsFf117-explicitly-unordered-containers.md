---
layout: post
title: "explicitly unordered containers"
date: 2026-04-23 17:24 -0700
permalink: /ZMtfpDsFf117/explicitly-unordered-containers
redirect_from:
  - /ZMtfpDsFf117
---

Having unordered containers such as pairs makes it possible to implement commutative operations in a naturally symmetric way.

For example:
```
upair : nat -> nat -> U nat
add : U nat -> nat

(+) : nat -> nat -> nat
(+) = add . upair

lemma : flip upair = upair
```

Having unordered containers provides a few benefits for theorem provers in particular because it makes proving results like the symmetry of addition possible without needing to use induction if it is possible judgemental equality in the type theory to take the unordered container into account for its equality relation. Even if not however, it perhaps makes it easier to reuse machinery for proving results about operations that are symmetric.
