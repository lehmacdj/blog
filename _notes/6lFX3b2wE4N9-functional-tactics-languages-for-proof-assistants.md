---
layout: post
title: "functional tactics languages for proof assistants"
date: 2026-04-23 17:13 -0700
permalink: /6lFX3b2wE4N9/functional-tactics-languages-for-proof-assistants
redirect_from:
  - /6lFX3b2wE4N9
---

I took a course titled Certified Software Systems where we learned how to use Coq. One irritating aspect of Coq is its tactics language, Ltac. Ltac can be described as a very messy imperative programming language for manipulating proof terms. Yes it is very powerful and is much easier than constructing proof terms by hand, but it seems like it might be possible to construct an even better tactics language by designing a functional tactics language. Since the space that the language needs to manipulate is mostly pure anyways (proof requirements), I don't see a reason why a functional language isn't well suited to being a tactics language.
