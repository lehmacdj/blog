---
layout: post
title: vim-magic-link-paste
date: 2025-09-08 01:30 -0400
tags: [vim, wiki]
---

I'm releasing [vim-magic-link-paste](https://github.com/lehmacdj/vim-magic-link-paste) today. When pasting a link over visually selected markdown text it creates markdown syntax for a link. See the video for an example of what the plugin can do:
<video width=400 controls alt="A video that demos using the plugin in vim">
  <source src="/images/vim-magic-link-paste-demo.mov" />
</video>

I originally built this functionality because I wanted a GitHub/Slack/Discord-like experience while adding links to my notes/blog posts. I've found it to be a huge quality of life improvement, and it encourages me to add more links.

Though already having the functionality working made it pretty easy to package this as a plugin, the work to "productionize" the plugin was more significant than I expected:
- My original mapping depended on [vim-surround](https://github.com/tpope/vim-surround) using `S]` to surround the visual selection with square brackets. Replacing this was pretty easy. The marks `` `< `` and `` `> `` indicate the beginning/end of the most recent visual selection. It's easy to jump to the end of the visual selection then insert `]` followed by jumping to the beginning of the visual selection and inserting `[`.
- I wrote a vim help file, to provide `:h` documentation for my plugin. Conveniently, you can get example syntax for any help page just by doing `set conceallevel=0`.
- A little extra boilerplate ended up being to make sure the plugin doesn't load twice + offer a way for users to opt out of key mappings.
- Supporting [vim-repeat](https://github.com/tpope/vim-repeat) ended up being a bit trickier than I expected.
