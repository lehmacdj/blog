---
layout: post
title: "contextual keywords"
date: 2026-04-23 17:13 -0700
permalink: /gSlE0WOhgelG/contextual-keywords
redirect_from:
  - /gSlE0WOhgelG
---

Contextual keywords allow more things to be used as valid identifiers. Swift allows overriding some keywords when defining using backticks and then at some use sites the identifier can be used without backticks. For example:
```swift
enum Variants {
  case foo
  case bar
  case baz

  static var `default`: Self { foo }
}

// this is legal syntax despite `default` being used in switch statement syntax
Variants.default
```
