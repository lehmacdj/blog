---
layout: post
title: "until loop"
date: 2026-04-23 17:30 -0700
permalink: /n4l4TUphkC42/until-loop
redirect_from:
  - /n4l4TUphkC42
---

Opposite of [while loop](/sSiTDOesjtyI/while-loop).

This would be useful in Swift in combination with `if let` for unwrapping optionals, e.g.
```swift
unless let somethingThatMustBeNonNil {
  // try to initialize somethingThatMustBeNonNil
}
// it is now non-nil
```
