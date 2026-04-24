---
layout: post
title: "Implicit Conversions Between Effects"
date: 2026-04-23 17:17 -0700
permalink: /kX1jiVaBymWv/implicit-conversions-between-effects
redirect_from:
  - /kX1jiVaBymWv
---

In a language predominated by effects it will be necessary to have "implicit" conversions between some of them. In order to facilitate this it will probably be useful to have a system defined set of handlers/cohandlers that can be automatically applied at any position in the code. If we have this feature it is essential that the programmer be able to override/change it in different scopes depending on what is required in a particular domain, because it is probably impossible to find a single set of (co)handlers that will satisfy every programmer in every situation.

Here a couple of examples to illustrate why this might be a desirable feature. Consider a conversion `{Error e} -> {Fail}`. It might be nice to allow this implicitly in most contexts because it would allow converting an error condition into a more general failure implicitly without writing this boilerplate. It might even be desirable (but fairly dangerous) to have an implicit conversion `{Fail} -> {}` in some contexts to allow aborting to allow less explicit code, for example when prototyping. Then later to introduce better error handling all that would be necessary would be to remove the implicit conversion and chase down type errors.
