---
layout: post
title: "unit tests can be co-located with code"
date: 2026-04-23 18:29 -0700
permalink: /DB3xJAOpe0Bf/unit-tests-can-be-co-located-with-code
redirect_from:
  - /DB3xJAOpe0Bf
---

Generally test suites live in separate files from the code they test. Historically, this was advantageous from the perspective of compiler development. Files that compile  file individually and then link the resulting files together because it allows excluding test code from release executables. However, it would be advantageous to co-locate tests with code because:
- tests act as documentation, making the code easier to understand
- it makes relocating top level functions easier, there is no need to also move the test
- it makes tests in context for LLMs by default

In order to make this feasible it is necessary to either:
- use conditional compilation[^conditional-compilation]
- link-time dead code elimination
- accept the fact that your executable will be a little larger.

I do this in [wiki-language-server](https://github.com/lehmacdj/wiki-language-server) and I like it quite a bit.

[^conditional-compilation]: be careful because

[conditional compilation makes linting/compiling code in an ide environment difficult](/TiqCn7SeTYUQ/conditional-compilation-makes-linting-compiling-code-in-an-ide-environment-difficult)

See also:
- [co-location](/A4bq6bKLHbQx/co-location)
