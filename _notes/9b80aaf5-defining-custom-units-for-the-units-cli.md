---
layout: post
title: "Defining custom units for the units CLI"
date: 2026-02-01 01:37 -0500
permalink: /9b80aaf5/defining-custom-units-for-the-units-cli
redirect_from:
  - /9b80aaf5
---

I recently started using a Glowforge Aura to laser cut stuff. So far I made a copy of the game Hex, designed an organizer for Kingdom Builder's tiny hexagons that are a pain to sort, and plan to also try my hand at creating custom Jig-Saw Puzzles.

While designing the Kingdom Builder organizer, I needed to measure game pieces using callipers and then cut out pieces of EVA foam with the correct size. Through a little bit of trial and error I determined that a 1151px square SVG exported from Figma (vector editing) was the largest size that didn't get resized when importing it into the Glowforge software and corresponded to the complete size of the Glowforge Aura's available cutting bed which is a 1ft / 304.8mm square.

Performing these conversions using a calculator was annoying.

I just discovered the [units CLI](https://lehmacdj.github.io/df5a7476/performing-unit-conversions-on-the-cli), and it makes it makes it pretty easy to define custom units. I defined a `gf` / `glowforge` unit which represents 1 pixel in Figma's coordinate space:
```
# Figma pixels to millimeters conversion for Glowforge Aura
glowforge			304.8|1151 millimeter
gf		glowforge
```

I couldn't figure out how to get the `units` to combine my custom units with its existing definitions, but it was easy to define an alias that combined the system library with my custom definitions:
```
units() {
  command units -f <(cat /usr/share/misc/units.lib "$DOTFILES/custom-units.lib") "$@"
}
```

Now I can do `units '25 mm' gf` to see that I should make my design 94.406168px in Figma.
