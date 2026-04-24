---
layout: post
title: "dedicated syntax for specific effects"
date: 2026-04-23 17:14 -0700
permalink: /vwO1Erpqe9jg/dedicated-syntax-for-specific-effects
redirect_from:
  - /vwO1Erpqe9jg
---

Imperative programming languages nowadays often have [async/await](/lNKqn420Niw4/async-await) for concurrency. Though strictly less general than do notation it is kind of nice that it explicitly specifies which effect is being managed at the use site whereas otherwise effects could be harder to notice visually. Another example of this is Swift's `try/throws` syntax for `Either` like exceptions.

Consider this Swift example:
```swift
async let access1 = readFileAsync(url: url1)
async let access2 = readFileAsync(url: url2)
let (contents1, contents2) = try await (access1, access2)
let newContents = contents1 + contents2
try await writeFileAsync(url: url3)
```

`try`/`async`/`await` clearly de-mark where effects occur. In a naive Haskell implementation of this they might not be.
