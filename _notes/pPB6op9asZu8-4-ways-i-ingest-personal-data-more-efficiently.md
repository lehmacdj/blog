---
layout: post
title: "4 ways I ingest personal data more efficiently"
date: 2026-04-17 23:36 -0700
permalink: /pPB6op9asZu8/4-ways-i-ingest-personal-data-more-efficiently
redirect_from:
  - /pPB6op9asZu8
tags: [inkhaven]
---

AI agents are getting to be really useful for analyzing giant dumps of unorganized data. But AI can only have access to the data that has already been collected. But AI agents promises to make it easier to get insights from the data I collect, either through custom vibe-coded tooling or agentic search.

I used to want to keep all the data I collect in inside of a single system, sorted with a unified tags, hierarchy, and such. I thought a unified system would make collecting metadata more efficient. I even went so far as building a custom tool for storing stuff with hierarchical tags in a graph like structure[^custom-tool] in pursuit of this goal. But rather than make the collection of more detailed metadata more efficient, this mostly added friction which prevented me from collecting nearly as much info in practice.

[^custom-tool]: You can find the tool in question at https://github.com/lehmacdj/graph. The most interesting thing it has is a regular expression inspired graph query language.

I now optimize for different principles. It should be as easy as possible to jot something down in as much detail as I want to. I need to be able to capture data from my phone. Data I collect needs to at minimum be associated with the data/time it was taken, and ideally as much automatically collectable metadata like location as possible. Critically to actually use the data, I need to be able to get the data onto my computer so that I can transform / ingest / sort / analyze it using Claude Code or whatever.

These methods have stuck around the longest:
- **Using photo captions**: Apple's photos app makes it easy to add captions to a photo, just by swiping up on it. It's really easy to take a screenshot or photo and then write a few sentences describing something I found interesting. Photos are automatically associated with the time and location they were taken, which makes it easy to sort through them later. iCloud drive syncs photos in an end-to-end encrypted way if you have Advanced Data Protection enabled.
- **Putting more stuff in daily notes**: My daily notes in my Zettelkasten used to mostly be a journal of what I did, plus how I felt. Instead of forcing myself to sort interesting articles or longer thoughts into separate notes, I just dump them in my daily notes now. It's easy to associate thoughts with subjects or thesis I'm developing through backlinks.
- **Using [How We Feel](https://howwefeel.org/)** to track emotions: This is a free app funded by a non-profit dedicated to researching emotions. It provides a grid that nicely sorts emotions, and easily lets you pick them and associate them with a little journal entry plus what you were doing, who you were with, and where you are. You can export everything as a giant json blob. This is just a better interface for entering information about how I felt about doing something than writing it in my daily notes or journal.
- **Recording voice memos**: Voice memos help me get ideas out of my head quickly. With transcription models getting good, it's easy to skim them later and figure out if the thoughts were valuable. I just use Apple's Voice Memos app because it syncs between my devices, and I can assign it to my action button.

These methods have helped me start to collect a lot more data. I kind of still want to create software to unify all of my data into one interface, but by ensuring that I have access to the data on my computer, I'm confident that I'll be able to do that later when I need to.
