---
layout: post
title: "surfacing semantic information about distributed behavior"
date: 2026-04-23 17:18 -0700
permalink: /dgmN2nnuWwRr/surfacing-semantic-information-about-distributed-behavior
redirect_from:
  - /dgmN2nnuWwRr
---

It would be useful if semantic information like reordering, retries, and serialization formats across network boundaries could be exposed to/enforced by the compiler without restricting what is possible.

This seems like it could be well represented as [coeffects / consumer effects](/mxPjuprza4i8/coeffects-consumer-effects). For example a message reordering coeffect could provide a default way of getting the message while discarding information about the order of the messages while one could also operate on the comonadic value to process the values as more of a stream.

From Distributed Programming has Stalled
