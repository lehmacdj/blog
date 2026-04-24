---
layout: post
title: "type safe dates/times/durations"
date: 2026-04-23 17:24 -0700
permalink: /9q45qzJgPaIz/type-safe-dates-times-durations
redirect_from:
  - /9q45qzJgPaIz
---

It is good if delay functions, etc. use type safe dates instead of just a long amount of milliseconds or microseconds or something similar. Especially because `threadDelay` or `delay` or `Thread.sleep` in different programming languages often have different dimensions. All that is required to do this is to use a custom type for the delay.

This is one area where [Haskell](/QYuhQ9ILhtzg/haskell)'s time library tends to fall a bit short. Because it allows expressing time without units and infers them to be seconds when using the overloaded `Num` instance and because `threadDelay` doesn't even take a `NominalDiffTime` as an argument it is a little bit easy to get this kind of thing wrong.

Swift does this pretty well as of fairly recent versions. There is a `Duration` type which is linked to a specific type of clock and is initialized using enum like `static func` constructors named after units. For example you write `try await Task.sleep(for: .seconds(3))`.
