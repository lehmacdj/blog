---
layout: post
title: "Performing unit conversions on the CLI"
date: 2026-02-01 01:37 -0500
permalink: /80ez771I2kAJ/performing-unit-conversions-on-the-cli
redirect_from:
  - /80ez771I2kAJ
tags: [cli, recommended]
---

I recently discovered[^how-I-discovered-it] the `units` CLI tool which installed by default on macOS/Linux and comes with a ton of builtin conversions. For example you can do:
```
❯ units '12 tablespoons' cups
	* 0.75
	/ 1.3333333
```

This tells you that 12 tablespoons is 0.75 cups, or that a cup is approximately 1.3333333 times 12 tablespoons. I don't really have any idea why it also shows the latter, but it's easy enough to ignore.

It also has an interactive mode that reduces the need for quoting shell arguments, e.g.:
```
❯ units
753 units, 62 prefixes
You have: 190 degC
You want: degF
	374
```

It also handles compound units seamlessly:
```
❯ units '10 m/s' mph
	* 22.369363
	/ 0.044704
```

One gotcha you have to watch out for is that numbers need to be separated from units by spaces, otherwise you get a conformability error and a gibberish result:
```
❯ units 10mm cm
conformability error
	10
	0.01 m
❯ units '10 mm' cm
	* 1
	/ 1
```

One of the most amazing things is the file containing the builtin unit definitions. On macOS 26 it is located at `/usr/share/misc/units.lib`. It starts out simple defining primitive units and prefixes:
```
# primitive units

m			!a!
kg			!b!
sec			!c!
[...]

# prefixes

[...]
kilo-			1e3
hecto-			1e2
deka-			1e1
deca-			deka
deci-			1e-1
centi-			1e-2
milli-			1e-3
micro-			1e-6
[...]
```

But it also contains a lot of (at least to me) extremely obscure units. For example, did you know that it takes 16 US feet make 15 French feet?
```
frenchfoot		16|15 ft
```

You also can [define your own custom conversions](/EaF5QphkhxlD/defining-custom-units-for-the-units-cli) for your own unique use cases.

I frequently find it convenient to use `bc` as a calculator on the command line in my dropdown terminal instead of using a browser/search engine, so I imagine I'll use `units` in the future when remembering or typing the conversion into `bc` is too inconvenient.

[^how-I-discovered-it]: I read the short story [500 Miles](https://web.mit.edu/jemorris/humor/500-miles) and was intrigued / didn't get the punchline because I'd never heard of `units`. To my surprise, it just existed.
