---
layout: post
title: "coeffects / consumer effects"
date: 2026-04-23 17:18 -0700
permalink: /mxPjuprza4i8/coeffects-consumer-effects
redirect_from:
  - /mxPjuprza4i8
---

See this neat interactive article for a high level explanation: http://tomasp.net/coeffects/

Coeffects or consumer effects describe requirements:
- purity e.g. like Recovering Purity with Comonads and Capabilities
- requirement to store past versions of variables
- [external dependency requirement coeffect](/Jnv3qiL1AYiP/external-dependency-requirement-coeffect)
- [the context co-effect](/UymtcOEMxlBk/the-context-co-effect)
- consumer choice
- [surfacing semantic information about distributed behavior](/dgmN2nnuWwRr/surfacing-semantic-information-about-distributed-behavior) seems like a pretty good fit
- implementing metaprogramming as a coeffect
- perhaps, but not exactly sure if so yet, more general coalgebraic coeffects
- perhaps static-ness/reflectability makes a good co-effect; e.g. thinking of the difference between `dynamicReadFile :: k FilePath String` and `staticReadFile :: FilePath -> k () String`. Maybe in a language with arrows for all function arguments, a coeffect on a parameter could specify whether the argument is consumed dynamically or statically
