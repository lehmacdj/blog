---
layout: post
title: "allowing statements to be used as expressions"
date: 2026-04-23 17:31 -0700
permalink: /T2LKKGgNsdGW/allowing-statements-to-be-used-as-expressions
redirect_from:
  - /T2LKKGgNsdGW
---

Rust allows most statements to be used as expressions.
```rust
let x = if isTrue {
  println!("hi");
  3
} else {
  4
}
```

Swift allows statements to be used as expressions if they only contain a single expression in their bodies.
```swift
var isEnabled = switch {
case .enabled: true
default: false
}
```

In Haskell and many functional programming languages all control flow statements are expressions.

Generalization of if expressions.
