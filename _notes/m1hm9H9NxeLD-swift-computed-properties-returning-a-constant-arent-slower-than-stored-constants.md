---
layout: post
title: "Swift computed properties returning a constant aren't slower than stored constants"
date: 2026-01-05 15:19 -0500
permalink: /m1hm9H9NxeLD/swift-computed-properties-returning-a-constant-arent-slower-than-stored-constants
redirect_from:
  - /m1hm9H9NxeLD
tags: [swift, optimization, recommended]
---

[Axel Le Pennec on Mastodon](https://iosdev.space/@alpennec/115729444379908949), noticed that using stored properties cause more recompilation when using Xcode Previews. In our discussion about this toot at work, a colleague suggested that while it's likely that incremental builds are faster for computed properties, this might come with a performance hit.

I had a hunch that the compiler should almost certainly optimize away any extra costs associated with a computed properties that returns a constant.

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

static output.Constants.storedProperty.getter : Swift.Int:
        mov     w0, #3
        ret
```

The computed property generates exactly the same code for accessing the property in both cases: just a single `mov` instruction. The `storedProperty` also has an `unsafeMutableAddressor` that is generated. I'm not exactly sure what it does, but a colleague suggested that it is used for Swift's `borrow` machinery, see e.g. [this thread](https://forums.swift.org/t/unsafeaddress-and-unsafemutableaddress/79804/3).
