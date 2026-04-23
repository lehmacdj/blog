---
layout: post
title: "My Neovim configuration"
date: 2026-04-22 23:02 -0700
permalink: /LylN8Ju8BGfr/my-neovim-configuration
redirect_from:
  - /LylN8Ju8BGfr
tags: [vim, recommended, inkhaven, wiki]
---

I use Neovim for 95%+ of my writing, both prose and code. I originally picked Vim over Emacs because I liked its modal text editing. Over the following years I've honed it to my preferences, building up over ~4000 lines of configuration. I've flirted with switching to Emacs with evil-mode for a better plugin ecosystem, but Vim is too deeply engraved in my muscle memory to move away from.

## Lua vs Vimscript
I don't have a strong preference for Lua/Vimscript. Historically, Vimscript was the only language for configuring Vim[^which-are-bad] . I generally assume that I will always use Neovim nowadays. Neovim makes Lua a first class language for configuring Vim. In fact, in addition to bridging all of Vim's APIs to Lua, new APIs (such as `vim.lsp`) are often only offered through Lua.

[^which-are-bad]: There also were remote plugins. But they require installing language runtimes, and have a more limited API than exposed through Vimscript.

Rewriting all of my configuration in Lua just to lose support for Vim completely seems like a waste of time, so I still keep a lot of my configuration in Vimscript. I tend to prefer Vimscript's syntax for [mappings](https://github.com/lehmacdj/.dotfiles/blob/623ba890da5afff964d72010ab28214edf53e4b7/nvim.symconfig/init.vim#L241-L242) and [autocommands](https://github.com/lehmacdj/.dotfiles/blob/623ba890da5afff964d72010ab28214edf53e4b7/nvim.symconfig/init.vim#L214-L218) to [Lua's](https://github.com/lehmacdj/.dotfiles/blob/af7972a429a12a86649b5671c66a4ecf267b09de/nvim.symconfig/plugin/lsp.lua#L46-L48) anyways. Lua's feels a little bit too verbose, and is harder to understand quickly in my opinion.

Neovim makes it very easy to mix Lua and Vimscript, which makes it possible to maintain interoperability even while maintaining configuration in both.

## Escape key
Because the escape key is far in the top left corner of modern keyboards, mapping `jj` or `jk` to escape in insert mode is fairly common. I used to do this. At some point I learned that Vim and most Vim plugins for other text editors treat `<C-[>` as escape. Rebinding caps lock to control system wide, made it possible to press `<C-[>` with my two pinkies simultaneously. An escape key mapping was previously the only configuration I truly couldn't do without so this has the added benefit of letting me use Vim-mode plugins in other editors (or Vim itself through SSH) well enough without needing to configure them.

## Modularization
Because my config has grown quite large, I need to keep it modularized for it to stay maintainable.

Mostly I rely on the runtime directory structure which allows loading a lot of files flexibly:
- `init.vim` has logic that needs to run before other configuration, plus a bunch of stuff that I've been too lazy to move elsewhere
- `plugins.vim` is sourced from `init.vim` and loads plugins. I have this separated out because I use a lot of plugins
- `ftsyntax` directories for autocommands improving file type detection, or adding new
- `ftplugin/after` directories house language specific configuration to prevent needing to define autocommands for them
- `autoload` directories store "library" functions that I use from other pieces of my configuration
- `lua/my` modules serve the same purpose, but for Lua code
- `plugin` directories for configuration insensitive to loading order

## Plugins
I still use vim-plug to manage my plugins because it works well enough, and well written plugins lazy load by design, thus not requiring anything fancier.

I'm a heavy plugin user so I'll only go through my favorite plugins. The most notable category is plugins that add generic cross language features to the editor without conflicting with default keybindings:
- `tpope/vim-repeat` makes it possible to use `.` with custom actions provided by other plugins. This should really just be a built in Vim feature.
- `tpope/vim-sleuth` makes indentation behave sanely by default.
- `tpope/vim-surround` adds a truly essential `ys`/`cs`/`ds` text editing verbs for adding/changing/deleting surrounding text
- `tommcdo/vim-exchange` provides a very useful `cx` text editing verb for swapping text
- `wellle/targets.vim` adds extra text objects (e.g. for function arguments) and makes existing text objects more flexible (e.g. selecting the next instance of a text object if you aren't already inside of it)

I use `overcache/NeoSolarized` for my color scheme because it's the most modern true color Solarized color scheme that I could find. I use `nvim-lualine/lualine` + `nvim-tree/nvim-web-devicons` to make the UI a bit prettier.

For more IDE like features, I mostly rely on language servers, but some extra support is provided by plugins.
- `hrsh7th/nvim-cmp` for autocomplete though I'm considering switching off this because it is now unmaintained
- `LuaSnip` for snippets

Other than that, there's pretty much just a bunch of syntax plugins.

I've also factored bits of my config as plugins (e.g. [vim-magic-link-paste](/Rna31XL7OHqU/vim-magic-link-paste)) plus a syntax plugin for moss-lang. A way to keep it easy to edit these even though they are no longer in my dotfiles repo is to branch on whether the repository exists on my computer:
```vim
if isdirectory($HOME.'/src/vim-magic-link-paste')
  Plug $HOME.'/src/vim-magic-link-paste'
else
  Plug 'lehmacdj/vim-magic-link-paste'
endif
```

This way, vim-plug won't clone them, and I can edit the source and have it stay up to date automatically.

## Making changes to configuration
I find being able to quickly navigate to a specific bit of configuration that I want to tweak important so that I'm able to fix problems / add new configuration without breaking my flow.

I use mappings that open up a configuration file in a split:
```vim
" Edit vimrc
nnoremap <Leader>ev <Cmd>split $MYVIMRC<CR>
" Edit plugins
nnoremap <Leader>ep <Cmd>split $VIMHOME/plugins.vim<CR>
```

My favorite is my one for editing language specific tweaks, it directly opens up the appropriate file for the current file type:
```vim
" Edit filetype file
nnoremap <expr> <Leader>ef '<Cmd>split '.$VIMHOME.'/after/ftplugin/'.&filetype.'.vim<CR>'
```

## Language specific tweaks
I most frequently edit my language specific configuration when I'm learning a language, or using a language I haven't edited in a while. Most commonly, language specific configuration is overrides for my global vim config like [not converting tabs into spaces for Makefile](https://github.com/lehmacdj/.dotfiles/blob/d360d71f7811664994519ca10f18254743364c2e/nvim.symconfig/after/ftplugin/make.vim#L1-L3) or [setting up soft wrapping for Markdown](https://github.com/lehmacdj/.dotfiles/blob/9b6a637f5c17bb9f9895f8fe03d96d4be480a8b4/nvim.symconfig/after/ftplugin/markdown.vim#L39). I also include custom keybindings that are only relevant for particular file types, like [publishing a note from my wiki](https://github.com/lehmacdj/.dotfiles/blob/9b6a637f5c17bb9f9895f8fe03d96d4be480a8b4/nvim.symconfig/after/ftplugin/markdown.vim#L67-L68).

## Wiki specific stuff
For my notes specifically I have a [custom language server](https://github.com/lehmacdj/wiki-language-server) that I use providing autocomplete + title transclusion from random ids + go to definition for navigating between notes. I rely heavily on conceal to keep markdown syntax hidden while reading notes in Neovim.
