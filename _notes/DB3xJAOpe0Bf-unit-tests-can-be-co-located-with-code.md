---
layout: post
title: "unit tests can be co-located with code"
date: 2026-04-23 18:29 -0700
permalink: /DB3xJAOpe0Bf/unit-tests-can-be-co-located-with-code
redirect_from:
  - /DB3xJAOpe0Bf
---

Generally we have a separate test suite that lives in entirely different set of files from the code we are writing. This is advantageous from the perspective of compilers that compile each file individually and then link the resulting files together because it allows excluding test code from release executables. However, it would be advantageous to co-locate tests with code because
- tests act as documentation, making the code easier to understand
- it makes relocating top level functions easier, there is no need to also move the test

In order to make this feasible it is either necessary to use conditional compilation[^conditional-compilation], link-time dead code elimination or accept the fact that your executable will be a little larger.

I do this in markdown-language-server and I like it quite a bit.

[^conditional-compilation]: be careful because conditional compilation makes linting/compiling code in an ide environment difficult

See also:
- co-location
