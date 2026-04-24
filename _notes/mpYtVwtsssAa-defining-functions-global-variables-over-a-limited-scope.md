---
layout: post
title: "defining functions/global variables over a limited scope"
date: 2026-04-23 17:30 -0700
permalink: /mpYtVwtsssAa/defining-functions-global-variables-over-a-limited-scope
redirect_from:
  - /mpYtVwtsssAa
---

The idea here is to be able at a very low cost define a single function/variable/symbol within a limited scope.

Here `id_stream` is in scope for fresh_id and avoid but nothing else, and fresh_id/avoid are defined at the top level of the current module.
```ocaml
let id_stream = Fresh.make @@ HashSet.make () in
let fresh_id = fun () -> Fresh.next id_stream
and avoid = fun () -> Fresh.avoid id_stream
```

> I think that Fresh was a module providing operations using an opaque type representing variables that have already been used. I think the goal here was to pass a single instance to these locally defined versions, which then allowed could be used without explicitly threading around an environment?
