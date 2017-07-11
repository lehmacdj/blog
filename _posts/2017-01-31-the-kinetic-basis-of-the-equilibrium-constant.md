---
layout: post
title: The Kinetic Basis of the Equilibrium Constant
date: 2017-01-31 19:09 -0400
tags: chemistry
---

[Reaction equilibrium][equilibrium] was one of the most mystifying concepts when
I was first learning chemistry. The rules for deriving the equilibrium formula
for a reaction seemed counter intuitive although straightforward and easy to
learn. Here is a simple hypothetical reaction between gases A and B that we
will examine to determine the equilibrium constant:

$$ 2A + B \rightleftharpoons A_2B $$

Any astute chemistry student will know that the equilibrium constant is written
as follows:

$$ K = \frac{[A_2B]}{[A]^2[B]} $$

An interesting observation is that what used to be addition in the reaction
equation is now multiplication, and the right side of the reaction is divided by
the left.

This transformation might seem arbitrary but it is a fairly obvious consequence
of reaction kinetics. Recall that we can write a [rate equations][rate_equation]
for the forward reaction like so:

$$ r_f = k_f[A]^2[B] $$

$$ r_r = k_r[A_2B] $$

where $$ r_f $$ and $$ r_r $$ are the forward and reverse reaction rates and $$
k_f $$ and $$ k_r $$ are the rate constants for those reactions. We can make the
same observation for these equations as we did when calculating the equilibrium
constant: adding reagents together manifests itself in the rate equation as
multiplication.

Now why is this the case? Well, what the rate equation is trying to describe is
the amount that the particles collide with one another to combine and form the
product. Since all of the particles must be near one another this problem can be
seen as the probability that 2 As and 1 B are near one another. Now since
concentration is similar to the probability that the particles, $$ [A]^2[B] $$
is similar to the probability that the reagents will be near one another. An
additional constant is needed to account for the difficulty for particles to
combine once they are actually near one another.

The equilibrium constant can be seen as the tendency of the reagents and
products of the reaction to be on the right side of the equation. Since the
reaction rate defines how fast the reagents turn into their products one can
observe that a good notion of the equilibrium constant might be to simply divide
the reverse reaction rate by the forward reaction rate like so:

$$ \frac{r_r}{r_f} = \frac{k_r[A_2B]}{k_f[A]^2[B]} $$

You might notice that this is very similar to the equilibrium constant that we
wrote down earlier. This is no coincidence. In fact, the two rate constants are
the same, which means that $$ K = \frac{r_r}{r_f} $$. To figure out why
$$ k_r = k_f $$ we need to first understand the [principle of microscopic
reversibility][reversibility]. This states that all processes are symmetrical
with respect to time; the consequence of this is that the forward and reverse
reactions proceed by the same mechanism and therefore take the same time and
proceed at the same rate with the same reaction coefficients at equilibrium.

I brushed over quite a few details that might be a problem in more difficult
chemical reactions but the concept is quite simple. At least for me figuring out
this connection made equilibrium constants much more intuitive and helped me
understand how to apply them better.

[equilibrium]: https://en.wikipedia.org/wiki/Equilibrium_constant
[rate_equation]: https://en.wikipedia.org/wiki/Rate_equation
[reversibility]: https://en.wikipedia.org/wiki/Microscopic_reversibility
