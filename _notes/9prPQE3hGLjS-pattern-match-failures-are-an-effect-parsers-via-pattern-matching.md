---
layout: post
title: "pattern match failures are an effect / parsers via pattern matching"
date: 2026-04-23 17:15 -0700
permalink: /9prPQE3hGLjS/pattern-match-failures-are-an-effect-parsers-via-pattern-matching
redirect_from:
  - /9prPQE3hGLjS
---

Assuming we have these functions with sensible implementations:
```
parseInt : String -> {Fail} Int
words : String -> [String]
```

Using View patterns we should be able to write code like this:
```
-- parse a string like "1 2" into a pair of integers
parsePair : String -> {Fail} (Int, Int)
parsePair (words -> [parseInt -> x, parseInt -> y]) = (x, y)
```

When parseInt fails during pattern matching, the 'Fail' is handled by the pattern matching compiler implementation which treats Fail as a pattern match failure. In a second illustration of the benefit of this, it isn't even necessary to write an exhaustive pattern match, if the pattern matching fails {Fail} is thrown which is exactly what we want, and can be caught or handled by the caller as desired.

Additionally this approach composes well, it would then be possible to use parsePair several times to parse a whole bunch of integers strung together by spaces probably.

## Potential problems
Using the default fail type could lead to accidental swallowed errors, that lead to worse than expected error messages (though not compromising purity). An alternative that somewhat fixes this would be to use a custom effect like `PatternMatchFailure` for the pattern match fallthrough functionality, and provide a utility/handler for converting `Fail` error to `PatterMatchFailure`, within some scope.
