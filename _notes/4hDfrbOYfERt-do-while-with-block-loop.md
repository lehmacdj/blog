---
layout: post
title: "do while with block loop"
date: 2026-04-23 17:31 -0700
permalink: /4hDfrbOYfERt/do-while-with-block-loop
redirect_from:
  - /4hDfrbOYfERt
---

When doing imperative programming, a surprising amount of the time I find myself wishing for a loop that might look something like this:
```
do {
  // initialization logic to be executed each loop
} while (<condition>) {
  // logic to be executed each loop if the condition is met
}
```

This is useful when you have code that makes sense as a do while loop but requires a condition before executing some logic that's required for the next iteration. This can be emulated in most imperative programming languages using:
```
// initialization logic
while (<condition>) {
  // logic to be executed each loop if the condition is met
  // initialization logic for next loop iteration
}
```

But this requires duplicating the initialization logic which is disappointing.
