---
layout: post
title: "representing types as just namespaces"
date: 2026-04-23 17:22 -0700
permalink: /Crx6jhw9TK7r/representing-types-as-just-namespaces
redirect_from:
  - /Crx6jhw9TK7r
---

*This is old, and I'm not sure that it makes much sense.*

Types seem to be little more than a name assignable to things that match certain criteria. These operations are defined within the namespace of that type. So every type is associated with a namespace inherently. Operations are relations, because they may be partial in general.

See also: Calculus of Names a note I wrote that extends this idea out to be a little more complete.

For example (using caps for existential variables and lowercase for universal):
```
Monoid {
  unit {
    unit = X
  }

  mul {
    mul x y = Z
    mul x (mul y z) = mul (mul x y) z
  }

  Monoid.unit, Monoid.mul {
    mul x unit = x
    mul unit x = x
  }
}
```

Defines a monoid, by giving its operations as members of the module, and the laws as properties satisfied by its operations.

The operation
```
name {
  body
}
```

Is to be interpreted as, with `name` in scope all of the equations within are true and recursively for any recursive name declaration within.

Notice that since we were able to define associativity as an equation associated with `mul`, the `mul` operation is exactly the same as the operation for semigroups.

We can define #import to include namespaces in other namespaces bringing them into scope.

Its possible that we don't even need universal/existential variables, if we get the proper understanding of what variables mean. It seems intuitive that they should mean something like, anything that is all of the dominating names, however this doesn't work for mul for example.
