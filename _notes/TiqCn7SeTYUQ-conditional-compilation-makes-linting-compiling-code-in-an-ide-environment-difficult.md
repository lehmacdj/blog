---
layout: post
title: "conditional compilation makes linting/compiling code in an ide environment difficult"
date: 2026-04-23 18:40 -0700
permalink: /TiqCn7SeTYUQ/conditional-compilation-makes-linting-compiling-code-in-an-ide-environment-difficult
redirect_from:
  - /TiqCn7SeTYUQ
---

When compiling code in an ide, generally there will only be a single set of flags active, therefore it is possible for there to be a compile error in a piece of code that isn't checked in the configuration used for ide diagnostics. This is a problem with C pre-processor (CPP) and rust `#[cfg(test)]` pragmas in particular.

The solution to this is to compile every configuration separately when compiling for ide diagnostics, but this can potentially lead to a blow up of possibilities, which could be expensive as building a project takes a long time without compiling it 2, 4 or even 8 times. A solution to this is to have compilation take into account different alternatives when compiling code natively, so that each file can still be compiled in a single pass (using for example external dependency requirement coeffect.
