---
layout: post
title: "compile time execution of code assertion / baking code"
date: 2026-04-23 17:11 -0700
permalink: /8BHXL4aXonrC/compile-time-execution-of-code-assertion-baking-code
redirect_from:
  - /8BHXL4aXonrC
---

It would be nice to have an assertion that can be used to require a piece of code to be evaluated at compile time. This has a number of benefits:
- guarantees fast performance similarly to inspection testing, if the code cannot be run at compile time it should fail
- make runtime failures into compile time failures

It is very important to be careful with allowing IO at compile time. It shouldn't be too easy to accidentally run IO at compile time instead of at runtime, as this could lead to wrong data. However it needn't be impossible to run IO at compile time, because this could be useful generating a table based on some kind of data source, perhaps for leap seconds for example.

This feature exists in:
- jai lang at least to some extent under the name of baking
- The D programming language also features this
