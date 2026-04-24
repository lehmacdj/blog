---
layout: post
title: "flexible scope resolution with article like functions/keywords"
date: 2026-04-23 17:29 -0700
permalink: /x7PUneHXkXAH/flexible-scope-resolution-with-article-like-functions-keywords
redirect_from:
  - /x7PUneHXkXAH
---

Articles in natural language seem to serve the purpose of scope resolution. It
might be nice to replicate this to some extent to provide user control over
scope in a programming language.

For example, `the` macro/function/keyword could perform one of the two following
functions (probably the former is a better default behavior without an article,
so maybe this could switch to the mode of the second one?):
- asserts that there is a single thing with the given name in scope (e.g. there
  is no automatic scope resolution in effect)
- sets the strategy for scope resolution to choose the best match from the
  existing scope (in this case, the default would be to throw an error when
  there are ambiguities when resolving scope)

Then assuming we had two functions named `trace` (admittedly this is a
relatively contrived example):
```
trace : StackTrace
trace : String -> {IO} ()
```

Suppose we have two trace functions (one refers to the dynamically scoped stack
trace and the other traces to the console). Then `print (the trace)` might be
able to print the stack trace instead of the function trace by some heuristic.
