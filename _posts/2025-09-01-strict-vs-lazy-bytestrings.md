---
layout: post
title: Strict vs Lazy `ByteString`
date: 2025-09-01 00:35 -0400
tags: haskell
---

The Haskell ecosystem's preferred way of representing binary data is the `ByteString` type. The [`bytestring`](https://hackage-content.haskell.org/package/bytestring-0.12.2.0) introduces its two variants like so:
> - Strict `ByteString`s keep the string as a single large array. This makes them convenient for passing data between C and Haskell.
> - Lazy `ByteString`s use a lazy list of strict chunks which makes it suitable for I/O streaming tasks.

Otherwise it has little to preference to express between strict `ByteString`s and lazy `ByteString`s.

The broader library ecosystem often offers functions for working with both lazy and strict `ByteString`s. For example, in `aeson` exposes [`decode`](https://hackage.haskell.org/package/aeson-2.2.3.0/docs/Data-Aeson.html#v:decode) which decodes a json value from a lazy `ByteString` in addition to a strict variant [`decodeStrict`](https://hackage.haskell.org/package/aeson-2.2.3.0/docs/Data-Aeson.html#v:decodeStrict). From this, it's reasonable to assume that lazy `ByteString` is the default, because `aeson` exposes it unqualified, while relegating strict to a section with "Variants for strict bytestrings".

However, as a general rule, I recommend sticking to strict `ByteString`s as a default:
- more memory efficient: lazy `ByteString`s include extra bookkeeping overhead for maintaining its list of strict `ByteString` chunks.
- reads are faster: in a strict `ByteString`, reading any position in the string is just reading from an offset in memory. For a lazy `ByteString` its necessary to follow pointers for values later in the bytestring.
- `O(1)` conversion to lazy `ByteString`s: converting a lazy `ByteString` to a strict one is `O(n)`, requiring copying the lazy `ByteString`'s chunks into a single contiguous block of memory. Strict `ByteString`s don't need to be split into smaller chunks, the existing memory reused.
- avoid lazy IO: while often convenient seeming, lazy IO leads to hard to diagnose bugs, like `IOException`s being thrown from pure code. You're generally better off using a streaming framework like `conduit`, `pipes` or `streamly` together with strict `ByteString`s.

Output oriented APIs, like serialization, are the one scenario where lazy `ByteString`s make a good amount of sense:
- builders produce lazy `ByteString`s: `Data.ByteString.Builder` only exposes [`toLazyByteString`](https://hackage-content.haskell.org/package/bytestring-0.12.2.0/docs/Data-ByteString-Builder.html#v:toLazyByteString) for converting a `Builder` into an actual `ByteString`. It takes [an `O(n)` conversion](https://hackage-content.haskell.org/package/bytestring-0.12.2.0/docs/Data-ByteString.html#v:toStrict) to turn the result into a strict `ByteString`.
- concatenation of lazy `ByteString`s is more efficient: lazy `ByteString`'s list of chunks allows appending new chunks without copying entire buffers of data. Use a builder instead of concatenating lazy `ByteString`s directly to avoid creating lots of small inefficient chunks if possible though!
- APIs for encoding/serializing often produce lazy `ByteString`s: because of the above its common for serialization operations like `aeson`'s [`encode`](https://hackage.haskell.org/package/aeson-2.2.3.0/docs/Data-Aeson.html#v:encode) to only expose versions producing a lazy `ByteString`.
