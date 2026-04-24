---
layout: post
title: "the runtime system should be deeply tied to effect system"
date: 2026-04-23 17:17 -0700
permalink: /NqZArcVKG3dy/the-runtime-system-should-be-deeply-tied-to-effect-system
redirect_from:
  - /NqZArcVKG3dy
---

The runtime system is responsible for interpreting the programming language in terms of things the CPU / operating system understands. This is very similar in function to any other kind of interpreter except for the fact that it interprets many effects at the same time. Allowing it to be interact with the effect system directly would allow the effect system to be much more tightly tied to other functionality.

Examples:
- error handling can either be caught returning to pure functions or delegated to the runtime system causing a crash
- If the runtime / language emits effects for language events like pattern match failure, this could also be used to implement something like [pattern match failures are an effect / parsers via pattern matching](/9prPQE3hGLjS/pattern-match-failures-are-an-effect-parsers-via-pattern-matching) fairly intuitively.
