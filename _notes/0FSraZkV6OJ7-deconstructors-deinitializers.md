---
layout: post
title: "deconstructors / deinitializers"
date: 2026-04-23 17:30 -0700
permalink: /0FSraZkV6OJ7/deconstructors-deinitializers
redirect_from:
  - /0FSraZkV6OJ7
---

Feature found in a lot of programming languages.

Universally tends to have a fairly large number of sharp edges:
- in Swift `deinit` is always nonisolated which makes it annoying in Swift Concurrency contexts and often requires spawning a task
- timing of when a deconstructor runs is unpredictable in garbage collected languages due to it being hard to know when the garbage collector will garbage collect the type after it is no longer being referenced
