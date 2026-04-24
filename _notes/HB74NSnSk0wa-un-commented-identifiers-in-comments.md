---
layout: post
title: "un-commented identifiers in comments"
date: 2026-04-23 17:10 -0700
permalink: /HB74NSnSk0wa/un-commented-identifiers-in-comments
redirect_from:
  - /HB74NSnSk0wa
---

Swift DocC offers syntax for this in the form of "\`\`", e.g.:
```swift
/// Some documentation that talks about ``foo``.
func foo() {}
```

This allows such references to be clicked with go to definition as well.

Swift does not offer syntax for [get runtime string of compile-time identifier](/QKeZY0XKOiI6/get-runtime-string-of-compile-time-identifier).
