---
layout: post
title: "Against foolproof software"
date: 2026-04-16 23:37 -0700
permalink: /YLwRkdcbZJyA/against-foolproof-software
redirect_from:
  - /YLwRkdcbZJyA
  - /YLwRkdcbZJyA/what-makes-a-good-spaced-repetition-system-against-foolproof-software
tags: [language-learning, recommended, spaced-repetition, inkhaven, product-design]
---

*If you're familiar with spaced repetition systems, this should work as a standalone post. This is the last post of a 3 post series. The first two posts explain [WaniKani](/v8mH7WGj5fNz/what-makes-a-good-spaced-repetition-system-wanikani) and [jpdb.io](/0THf60NuwInF/what-makes-a-good-spaced-repetition-system-jpdbio) in more detail.*

WaniKani tries very hard to make learning Japanese foolproof. They don't let you grade yourself or undo mistakes [they want to protect you](https://knowledge.wanikani.com/wanikani/undo-button/) from "the illusion of knowing". [They don't offer](https://knowledge.wanikani.com/wanikani/skip-content/) the ability to blacklist or permanently mark cards as known.

These design decisions probably make WaniKani more effective for the user profiles they think about the most. WaniKani's testimonials highlight two kinds of users:
- **Japanese residents**, who likely either need Japanese for work, e.g. "My job requires me to work with a number of Japanese companies.", or strong intrinsic motivation, e.g. "I've lived in Japan for eight years". For this kind of person, it's easy to dedicate 1-2 hours every day to learning Japanese.
- **self-learners**, with a lot of time to dedicate to learning Kanji. My friends who made it through much more of WaniKani than me, all fit into this category. Even for me, WaniKani worked well at first, before betraying my expectations in a couple of important ways.

First, WaniKani ended up growing into a much larger time commitment than I assumed from my first few weeks using it. WaniKani doesn't claim how many hours per day it will take to learn Japanese in just over a year. But, because early on WaniKani's mechanics for unlocking lessons prevented me from investing the ~30 minutes per day I wanted to, I assumed that the workload would continue to be manageable. Then, when reviewing flashcards from the past 4 months, the workload became overwhelming. jpdb.io's better spaced repetition algorithm lets you build it into your schedule more consistently from the start, while also adapting better if you're willing to commit less time in the future.

Second, WaniKani promised to teach me "2,000 kanji, hand-picked and cleverly ordered" plus "6,000 Japanese words, all carefully validated by a human to be common or useful". Of course, I didn't have a good sense of what vocabulary I wanted to learn, so this was part of what appealed to me when I chose WaniKani. If I'd been willing to commit the time to mine songs and texts for vocabulary I cared about, I probably would have started with Anki. But over time, the rigidity of the curriculum started to frustrate me. I longed to be able to exclude words, even considering a Firefox extension for WaniKani that would autofill the correct answer for words that I didn't want to review.

Both of these problems were mostly a misalignment between my goals and knowledge, and the needs WaniKani's developers assume their users have. But WaniKani is designed to be foolproof, without options or configuration that would make it less effective for certain kinds of users.

Aiming for foolproof makes a lot of sense when designing a product. Less options, configuration, and variables to consider makes the product simpler. This has huge dividends for scalability. A simpler product is easier to explain, optimize, market, and sell without needing to consider the needs of individual users.

But I wasn't interested in WaniKani as a mindless consumer, I was interested in a tool to help me learn Japanese. Instead of aiming to be foolproof, jpdb.io trusts its users to accomplish their goals. This unlocks the possibility for it to be better tailored to any individual user's specific goals.

Not everyone will carefully tweak all the configuration options to figure out what works the best for them. Good defaults will make sure that the average user still has a good experience. But almost everyone has specific complaints about the products they use or things they would want tweaked. It's worth building a configuration option for at least the most common ones.

Even if users want something that you think would make the product worse, they're probably trying to act in their own best interest. Sometimes, as the designer, you really do know better. But, at other times you don't understand the user's complaint well enough. If enough people request a setting you find confusing, perhaps it's worth exercising some intellectual humility and adding it anyways, along with an explanation for why you think they shouldn't use it[^jpdb-io-does-this]. If you trust that your users are acting in their own best interest, they're probably motivated enough to try to understand your reasoning.

[^jpdb-io-does-this]: jpdb.io's settings page actually does this several times. I haven't changed any of the settings it recommends against.

Most users don't need to be protected from themselves. Instead of making your software foolproof for your assumed user, design it to adapt to the needs of your specific users.
