---
layout: post
title: "closed vs open types"
date: 2026-04-23 17:20 -0700
permalink: /48FOjJ7COOaX/closed-vs-open-types
redirect_from:
  - /48FOjJ7COOaX
---

Both sum and product types have closed and open variations:

|        | Product                             | Sum                             |
|--------|-------------------------------------|---------------------------------|
| Closed | structs/record types                | coproducts / variants / enums   |
| Open   | row types (i.e. extensible records) | polymorphic variants            |

Interestingly I don't think it is possible to define open variants of the dependent product / dependent sum. Without a specific domain to scope over, dependent types seem fairly ill scoped.
