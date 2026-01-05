---
layout: post
title: "Computed properties that return a constant are *more* performant than stored properties"
date: 2026-01-05 15:19 -0500
permalink: /89f52db5/computed-properties-that-return-a-constant-are-more-performant-than-stored-properties
redirect_from:
  - /89f52db5
tags: [swift, optimization, recommended]
---

I had a hunch that the compiler should almost certainly optimize away a computed property that returns a constant.

To make a fairer comparison for cross-module compilation situations (like in a large real world app), consider the assembly generated from [just this snippet](https://godbolt.org/z/evoqo5njz) (no main function, to simulate exposing this from a Framework):
```swift
public enum Constants {
    public static var computedProperty: Int { 3 }
    public static let storedProperty: Int = 3
}
```

Compiling with `-Osize` (optimize for executable size), we get the following relevant assembly:
```arm
static output.Constants.computedProperty.getter : Swift.Int:
        mov     w0, #3
        ret

output.Constants.storedProperty.unsafeMutableAddressor : Swift.Int:
        adrp    x0, (static output.Constants.storedProperty : Swift.Int)
        add     x0, x0, :lo12:(static output.Constants.storedProperty : Swift.Int)
        ret
```

The computed property is actually smaller/faster/more optimized! Just a single `mov` instruction, rather than loading a value from memory.
