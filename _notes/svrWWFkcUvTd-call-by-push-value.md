---
layout: post
title: "call by push value"
date: 2026-04-23 17:20 -0700
permalink: /svrWWFkcUvTd/call-by-push-value
redirect_from:
  - /svrWWFkcUvTd
---

Came across this a fairly long time ago and it is pretty cool. You basically separate types into values + computations, with the ability to convert between them (thunking turns a computation into a frozen value and returning allows embedding a value into a computation). It provides a nice way of reasoning about algebraic effects and possibly also other benefits.

I recently came across this article too: https://thunderseethe.dev/posts/bet-on-cbpv/
