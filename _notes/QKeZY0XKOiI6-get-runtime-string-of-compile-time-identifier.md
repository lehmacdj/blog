---
layout: post
title: "get runtime string of compile-time identifier"
date: 2026-04-23 17:10 -0700
permalink: /QKeZY0XKOiI6/get-runtime-string-of-compile-time-identifier
redirect_from:
  - /QKeZY0XKOiI6
---

An underrated but surprisingly useful feature. Makes it easy to make sure that identifiers in strings get changed as the code does. Generally the identifier should need to be well scoped. This helps prevent typos too.

Related: [un-commented identifiers in comments](/HB74NSnSk0wa/un-commented-identifiers-in-comments)

## Examples
### C#
```csharp
string x = nameof(foobar)
```

### Swift DocC
