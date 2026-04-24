---
layout: post
title: "local type declarations"
date: 2026-04-23 17:30 -0700
permalink: /F4TTPLipKTSS/local-type-declarations
redirect_from:
  - /F4TTPLipKTSS
---

It's sometimes useful to define a data type locally. This is often useful for similar reasons to why a local function declaration is useful. It naturally limits the scope of the type, so the programmer doesn't need to worry about where-else the type can escape to.

Most modern programming languages provide some version of this though often with limitations (e.g. no protocols / types can't escape their scope), e.g.
```swift
// this is semantic gibberish, but shows a use example
func f() {
  struct Proxy {}
  func bar() -> Proxy {
    print("hello")
    return proxy
  }
  let x = bar()
  return
}
```

This goes well with [scoped typeclasses or implicits](/TChq81fMCv9p/scoped-typeclasses-or-implicits) in contexts where [confluent instance resolution](/3nJYq6q6JOEA/confluent-instance-resolution) is important.

See also [this GHC proposal](https://github.com/treeowl/ghc-proposals/blob/e65674db941474db03b9cc6b58f016d427e9f922/proposals/0000-local-types.md).
