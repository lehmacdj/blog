---
layout: post
title: "super compilation"
date: 2026-04-23 17:20 -0700
permalink: /mUFaDSi2Kni8/super-compilation
redirect_from:
  - /mUFaDSi2Kni8
---

Technique where whatever is executable at compile time is executed at compile time resulting in an executable that does minimal computations at runtime.

Often this involves trading off compilation time & executable size for execution time. Sometimes, naively reducing to normal form (ala lambda calculus normal form evaluation) doesn't yield better performance on modern processors due to cache misses from having a larger executable size (TODO would be good to have an example of this).

[compile time execution of code assertion / baking code](/8BHXL4aXonrC/compile-time-execution-of-code-assertion-baking-code) is a more practically viable version of this, where instead of just doing it for everything, you have the programmer direct where it would be most effective.
