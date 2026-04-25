---
layout: post
title: "I don't want your skills"
date: 2026-04-24 21:03 -0700
permalink: /aFKl86BhaWNX/i-dont-want-your-skills
redirect_from:
  - /aFKl86BhaWNX
tags: [recommended, agentic-programming, inkhaven]
---

I often notice people advertising their custom skills as a solution to your agentic programming problems. They'll provide you some genuinely useful advice, then cap it off by offering you skills that operationalizes their advice.

I found the failure modes and tips identified in [Software Fundamentals Matter More Than Ever](https://www.youtube.com/watch?v=v4F1gFy-hqg) insightful. I never thought about having a glossary of shared vocabulary to make communication with AI agents more effective. AI agents outrunning their headlights by doing way too much autonomously provides metaphor for my common experience of having AI agents do underspecified work. Focusing on building deeper modules with a lot of functionality hiding behind a small interface, is a pattern I've been thinking around, but haven't yet been able to put words to.

But following the insight with skills that will "solve" the problem for you, is the equivalent to giving a tutorial on how to implement [nanoGPT](https://github.com/karpathy/nanogpt) and then capping it off by saying: but you can just use <https://chatgpt.com>[^disclaimer].

[^disclaimer]: Andrey Karpathy does not do this.

Yes, it does seem helpful to have my AI agent `/grill-me` — asking detailed questions instead of providing corrections to plans reflecting a fundamental misunderstanding of the problem over and over again. Of course, I'd love to `/improve-codebase-architecture`  modularizing my codebase. But running a skill won't help you understand how it works.

These skills probably work in simpler codebases. But simpler codebases are also the best environment to understand the principles behind the skills and learn how to build them yourself. And without understanding the principles, you won't necessarily understand that or how the skill failed in a more complex codebase.

I've noticed this pattern before in discussions with other engineers. I explained to another engineer: just giving Claude Sonnet 4.5 our feature flag documentation plus a list of files that needed to modify was enough for it to make the changes fully autonomously. They responded by asking if I could package that up into an `/add-feature-flag` skill.

I didn't see the point. The skill would just be 1-2 sentences of text and a list of files that needed to be modified in order to make changes to the feature flags. The skill would encapsulate nothing but the fact that this task was now easy to automate.

My recommendation is to engage with content that offers you skills, but try to learn the principles behind the skills instead of using the skills themselves. Try to prompt your AI agent to solve the problem yourself.

Doing this, I've found that after a while, I want to abstract my prompt into my own skill.

I remember reading an article about adding comments to plan documents inline, instead addressing them one by one in Claude Code's prompt. I liked this technique and after trying it, ended up building produced [this skill](https://github.com/lehmacdj/.dotfiles/blob/main/llm/address-comments.symskill/SKILL.md). Though I've provided a link, I recommend not clicking it.

Downloading skills won't make you a good AI engineer. Understanding why they work and operationalizing the principles behind them will.
