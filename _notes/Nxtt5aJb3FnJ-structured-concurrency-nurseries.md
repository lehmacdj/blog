---
layout: post
title: "structured concurrency / nurseries"
date: 2026-04-23 17:18 -0700
permalink: /Nxtt5aJb3FnJ/structured-concurrency-nurseries
redirect_from:
  - /Nxtt5aJb3FnJ
---

An approach to concurrency arises from an analogy to the introduction of structured programming (if/for/while control structures). The key concept is a nursery (called a `TaskGroup` in Swift). The nursery allows spawning threads but ensures that threads join so that procedure/function calls may maintain their property of encapsulating control flow. Usage looks like this:
```python
async with trio.open_nursery() as nursery:
    while True:
        incoming_connection = await server_socket.accept()
        nursery.start_soon(connection_handler, incoming_connection)
```

This enables some emergent effects:
- error handling is easier, because exceptions can't be swallowed by a thread that continued running after the function that spawned it
- automated resource cleanup is possible again (go/fork breaks this because the thread can outlive the using/with/finally block)
- cancellation is easier

See also go considered harmful which expands a lot of the points and at least to some extent introduced the idea.

TODO: investigate pi calculus in light of the considerations in this article. How does it stand up / what changes would be necessary to make a pi calculus supporting structured concurrency like this

## Swift Concurrency System
The swift concurrency system is strongly influenced by structured concurrency.

See the proposal that introduces it: https://github.com/apple/swift-evolution/blob/11a715544e82d118aab1a75910e9bc1f24a09090/proposals/0304-structured-concurrency.md
