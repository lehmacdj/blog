---
layout: post
title: "external dependency requirement coeffect"
date: 2026-04-23 18:47 -0700
permalink: /Jnv3qiL1AYiP/external-dependency-requirement-coeffect
redirect_from:
  - /Jnv3qiL1AYiP
---

Requirement that certain external dependencies be satisfied. Suggested as a possible coeffect in https://web.archive.org/web/20220620130750/http://tomasp.net/coeffects/ (search for "in cross-platform code").

There are several possible implementations of this co-effect, which might be viable depending on how hard it is to check that a particular external dependency is satisfied:
- compile-time check: an interpreter could verify at compile-time (or typecheck-time) that a check is satisfied if that is possible
- runtime check: we might be able to check at runtime if we can't check at compile-time[^why-not-compile-time]
- dumb prompt: if we don't have a viable way of checking at runtime, we can always offer a prompt to the user to confirm that the requirement is satisfied
- ignore/assume satisfied: we can also offer an interpreter that assumes the dependency is satisfied. The coeffect is still providing a benefit because we need to assume the criteria is met at some point in our code, and can include a comment at that use site.

[^why-not-compile-time]: For example, might not be able to check at compile time if we're concerned with the schema of a database. The schema could be changed with external user commands.
