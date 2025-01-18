#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to interview problem: estimate pi using a Monte Carlo method.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-04-07 and was classified as Medium.

  Reported source: Google.

  The area of a circle with radius r is defined to be πr^2.
  Use a Monte Carlo method to Estimate π to 3 decimal places.

* Solution

The area of a circle of radius r is given by area = pi * r^2, so

  pi = area * r^(-2).

If we consider the unit circle, that is r = 1, the equation simplifies
to pi = area.

To estimate pi, then, we can simply estimate the area of a unit
circle. To estimate the area, consider a unit circle at the origin.
Now circumscribe that circle with a square. An arbitrary point within
that square is within the circle with probability

  p = (area of circle) / (area of square).

We can estimate p by throwing n random darts uniformly at the square
and counting the number of darts that landed within the circle. If m
darts land within the circle, then m/n is an estimate for p that gets
better as we throw more darts.

  pi = (area of circle) = (area of sqare) * p = 4 * p.

** Implementation notes

Since both the circle and square are symmetric about the x- and y-axes,
we can estimate p by considering only one of the 4 quadrants, and we
choose the positive-positive quadrant (I) for convenience.

To avoid potential bias from random floating-point numbers not being
uniformly distributed, we use random integers instead, and instead of
a radius of 1.0 we use 2^32.

"""

import random

RADIUS = 1 << 32
RADIUS_SQUARED = RADIUS * RADIUS


def estimate_pi(iterations):
    hits = 0
    for _ in range(iterations):
        x = random.randrange(RADIUS)
        y = random.randrange(RADIUS)
        if x * x + y * y <= RADIUS_SQUARED:
            hits += 1
    return 4.0 * hits / iterations


def test_estimate_pi():
    random.seed(123)  # Ensure stability of tests.
    assert abs(estimate_pi(1000000) - 3.1415927) < 0.001
