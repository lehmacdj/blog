---
layout: post
title: "My quest to materialize my thoughts on my computer"
date: 2026-04-29 23:50 -0700
permalink: /1nWDiPLwMooh/my-quest-to-materialize-my-thoughts-on-my-computer
redirect_from:
  - /1nWDiPLwMooh
tags: [inkhaven, knowledge-management]
---

File systems are the default categorization system for personal information on a computer. They make it easy to store files, notes, repositories, or whatever in hierarchies.

But hierarchies are limiting. A file can only exist at a single path[^hardlinks-symlinks].

Information in our minds doesn't work like this. When speaking we reference the same entity in lots of different ways. Whether I have a layover in "San Francisco", am going to "the airport" to fly home, or am entering "SFO" on Google Flights to book a ticket, I'm referencing the same entity.

[^hardlinks-symlinks]:
  Symlinks try to achieve this, but are fragile. If the original copy moves the symlink breaks and it is often isn't easy to find the original copy.

  [Hardlinks](/hbbzJ0lZT8Tc/hardlinks) are closer you map multiple paths to the same underlying data. However, hardlinks suffer from [challenging edge cases](/FzO9RP3zvyBM/problems-with-hardlinks), and generally don't support directories.

The internet promised to solve this problem. Hyperlinks let people reference and categorize things however they want, right?

Take YouTube for example. It's trivial to create a playlist of videos. If you want to categorize your playlists into a hierarchy, YouTube won't let you do that, you just need to save them into a folder of bookmarks, or as links in a note.

Personal knowledge management tools like Notion, Obsidian, Logseq, or Roam Research attempt to make keeping bookmarks, links, notes, and research easier. These are great, I use my Zettelkasten of markdown notes with Obsidian sometimes[^mostly].

[^mostly]: In practice, I mostly edit my notes using Neovim with [custom language server](https://github.com/lehmacdj/wiki-language-server) for completion, transclusion, and jumping to links.

These systems make me sad that I can't associate metadata with arbitrary data — YouTube videos, Wikipedia articles, songs, and so on. Often they support fancier features like canvases, PDF clippings, and even database like rows, once you leave the domain of markdown, metadata starts being stored in private formats.

But I find it too risky to invest heavily into these systems, because building or maintaining a replacement that supports whatever custom features I use would be non-trivial.

What I really want is a personal ontology that operates like [Wikidata](https://www.wikidata.org/wiki/Wikidata:Introduction). I hope that Web3 (not the crypto kind) projects like [Solid](https://solidproject.org/) are steps in this direction, but they're still very immature, and I don't want to couple myself to shifting standards.

Pretty much the only satisfying option seems to be building it from scratch myself.

---

When I was ~10 I remember my uncle asking me how I thought my brain worked. I described it as a point of light bouncing around a network of memories.

I'm hoping that someday I can bring that network of connections into the real world and interact with my computer the same way I interact with my mind.

I want to build a system in which my mind can wander safely to the information it wants, while knowing that it contains only information that I put or chose to be there. Perhaps someday I will achieve this dream.
