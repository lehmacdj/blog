---
layout: post
title: "Lambda with receiver"
date: 2026-04-23 17:13 -0700
permalink: /2glFqLPSCCmX/lambda-with-receiver
redirect_from:
  - /2glFqLPSCCmX
---

Feature in Kotlin: https://kotlinlang.org/docs/lambdas.html#function-types

Maybe not actually that groundbreaking but allows for some pretty cool
meta-programming / DSL construction, such as Kotlin's builders. For example:
```kotlin
val map = HashMap().apply {
  put(0, "0")
  for (i in 1..10) {
      put(i, "$i")
  }
}
```
put is an instance method of the HashMap but we can call it implicitly without
prefixing this allowing for a fairly terse syntax.
