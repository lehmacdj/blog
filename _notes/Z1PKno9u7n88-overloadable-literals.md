---
layout: post
title: "overloadable literals"
date: 2026-04-23 17:12 -0700
permalink: /Z1PKno9u7n88/overloadable-literals
redirect_from:
  - /Z1PKno9u7n88
---

As in Haskell `-XOverloadableStrings`, `-XOverloadableLists` or even its default handling of numeric literals.

Things that it would be useful to have literals for are:
- numbers
- strings and other string like things
- collections (i.e. lists, maps, sets, etc.)
- regexes
- http status codes (very specific but it would be nice to compile 500 into a http status code type enum maybe)

There are two approaches:
1. allow stealing arbitrary syntax to make literals, this is possibly necessary to do regexes for example if we want to have `/i am a regex/` syntax because it doesn't seem valuable to have a specific overload for that available
2. have specific syntaxes that are overloadable
   - [Haskell](/QYuhQ9ILhtzg/haskell) does this with type classes like `FromString` + `OverloadableStringLiterals`, `FromInteger`, etc.
   - Swift also does this with protocols like `ConvertibleFromNilLiteral`, `ConvertibleFromStringLiteral`, `ConvertibleFromArrayLiteral`, though it generally discourages implementing these from anything other than the standard library

In approach two sometimes we want to define literals for which not every value in the syntax is a valid value of the type that the literal produces. For example consider natural numbers in Haskell. `-3 :: Natural` type checks, but is a value that is essentially `undefined`. It would be really nice to be able to enforce this code to run at compile time or be otherwise impossible. [compile time execution of code assertion / baking code](/8BHXL4aXonrC/compile-time-execution-of-code-assertion-baking-code) offers an approach for doing this.

## Pitfalls with overloaded literals
As the following blog post shows there are some problems with having overloaded literals, namely they tend to make error messages more difficult to generate in a good way: https://www.thecodedmessage.com/posts/haskell-gripe/. This is because it might be possible for the code to compile given some particular strange type for a given thing. For example `1 + []` could compile given an instance of `Num [Int]` where `fromInteger 1 = [1]` and addition is defined by lifting functorially.
