---
layout: post
title: "defer statement"
date: 2026-04-23 17:30 -0700
permalink: /dn7y1F0E7gIR/defer-statement
redirect_from:
  - /dn7y1F0E7gIR
---

Nice way of co-locating cleanup code together with initialization code + a way to make sure that cleanup code gets run.

## Tricky Scoping Issues
It isn't obvious what should happen in a code block like this:
```swift
var y = -1
do {
    var x = 0
    defer { y = x }
    x = 1
}
print(y)
```

Naively in many functional programming languages `x` would be captured immutably causing the print statement to print `0`; in Swift this prints 1, the `defer` block effectively being copied to occur at the end of the scope. This seems like the most sensible thing to do in my opinion.
