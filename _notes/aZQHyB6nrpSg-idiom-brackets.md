---
layout: post
title: "idiom brackets"
date: 2026-04-23 17:14 -0700
permalink: /aZQHyB6nrpSg/idiom-brackets
redirect_from:
  - /aZQHyB6nrpSg
---

[An idris feature](http://docs.idris-lang.org/en/latest/tutorial/interfaces.html#idiom-brackets) that makes programming with applicative functors easier.

Semantically it is supposed to be interpreted such that ```idris [| f a b |] == f <$> a <*> b ``` but it is a little bit more complicated because it is smart enough to lift pure values using pure as well.

This notation was first introduced in Connor McBride and Ross Paterson's paper "Applicative Programming with Effects"[^1].

[^1]:
    Conor McBride and Ross Paterson. 2008. Applicative programming with effects.
    J. Funct. Program. 18, 1 (January 2008), 1-13.
    DOI=10.1017/S0956796807006326 http://dx.doi.org/10.1017/S0956796807006326
