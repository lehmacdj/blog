---
layout: post
title: "Haskell: the re-export module X pattern"
date: 2026-04-04 15:46 -0700
permalink: /rJylKYFWAsAP/haskell-the-re-export-module-x-pattern
redirect_from:
  - /rJylKYFWAsAP
tags: [haskell, programming-pattern, inkhaven]
---

Haskell's syntax for declaring module exports is clunky and second-class. Exports must be declared after the module header either by name, or re-exporting an entire module:
```haskell
module Foo
  ( bar,
    module Baz,
  )
where

import Baz

bar :: Int
bar = 42
```

This re-exports all of the identifiers exported by `Baz`. If instead you only wanted to re-export some of the identifiers, naively you would need to list them all out individually:
```haskell
module Foo
  ( bar,
    baz1
  )
where

import Bar
import Baz
```

Just reading the export list, it can be unclear which module the identifiers are being imported from: e.g. is `bar` actually exported by `Bar` or is it actually provided by `Baz`.

The **re-export module X pattern** is a simple trick to solve this problem. Instead of re-exporting identifiers individually, use a qualified import to say up front which identifiers you plan to re-export:
```haskell
module Foo
  ( module X,
  )
where

import Bar as X (bar)
import Baz as X (baz1)
```

This makes it easy to see which modules and which identifiers we are re-exporting identifiers from, no matter how many. `X` is conventionally used as the module name, i.e. e**X**port.

There's two primary scenarios where I reach for this pattern:
1. **building a custom prelude**: Custom preludes need to re-export lots of identifiers from lots of different modules. To provide some internal organization and make your prelude more discoverable it's often useful to break them into submodules, e.g. `MyPrelude.Effects`, `MyPrelude.MaybeEither`.
2. **building a utility module extending another module**: Maybe you have a custom combinator for operating on maps not provided by `Data.Map.Strict`. I like putting this kind of combinator in a `Utils.Map` module, and then also re-exporting everything I want to use from `Data.Map.Strict`. Then you can just `import qualified Utils.Map as Map` instead of needing to also `import qualified Data.Map.Strict as Map`.

The following example demonstrates a couple of important gotchas:
```haskell
module Foo
  ( module X,
  )
where

import Bar as X (bar)
import qualified Baz as X (baz1)

bar :: Int
bar = 42
```

Perhaps unexpectedly, this example exports `Bar.bar` instead of `Foo.bar`. Also, if you try using (e.g. `bar + 1`) or re-exporting (e.g. adding `bar` or `module Foo` to `Foo`'s export list) `bar` you'll get `Ambiguous occurrence ‘bar’`. You can disambiguate by exporting the fully qualified module name, i.e. adding `Foo.bar` or `Bar.bar` to the export list (instead of doing `import Bar as X (bar)`).

Additionally, though `Foo` looks like it might, it doesn't actually re-export `baz1`. In order for an identifier to be re-exportable, it must be imported unqualified.

Here's an example that demonstrates a couple of useful tricks:
```haskell
module Foo
  ( module X,
  )
where

import Bar
import Bar as X (bar)
import Baz as X hiding (bar2)
```

Note that you can have multiple imports of the same module, here `Bar`. This can be useful when you're providing some functions that work with the types in an existing module, but don't want to re-export the whole original module.

Finally, note that using `hiding` lets you re-export a whole module less some identifiers, here `Qux`. This can be useful when you want to re-export everything but one of your identifiers conflicts.
