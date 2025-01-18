#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Count the ways to roll a dice total.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-12-21 (#272) and was classified as Medium.

  Reported source: Spotify.

  Write a function, throw_dice(N, faces, total), that determines how
  many ways it is possible to throw N dice with some number of faces
  each to get a specific total.

  For example, throw_dice(3, 6, 7) should equal 15.

"""

import functools
import sys


def memoize(f):
    """Make a memoized version of f that returns cached results."""
    cache = {}

    @functools.wraps(f)
    def g(*args):
        ret = cache.get(args, cache)
        if ret is cache:
            ret = cache[args] = f(*args)
        return ret

    return g


# Memoized recursive version. Takes O(N*total) time and space.
@memoize
def throw_dice(N, faces, total):
    """Counts how many ways we can roll N dice to reach a total."""
    if N < 1:
        return 0
    if N == 1:
        return 1 if 0 < total <= faces else 0
    return sum(
        throw_dice(N - 1, faces, total - face)
        for face in range(1, 1 + min(faces, total))
    )


# Dynamic programming version. Takes O(N*total) time and O(total) space.
def throw_dice_dp(N, faces, total):
    """Counts how many ways we can roll N dice to reach a total."""
    if N < 1:
        return 0
    ways = [1 if 0 < i <= faces else 0 for i in range(total + 1)]
    for _ in range(1, N):
        new_ways = [
            sum(ways[j] for j in range(max(1, i - faces), i)) for i in range(total + 1)
        ]

        ways = new_ways
    return ways[total]


# Tests.


def test():
    for soln in throw_dice, throw_dice_dp:
        assert soln(3, 6, 7) == 15
        for faces in range(1, 10):
            for total in range(1, faces + 1):
                assert soln(1, faces, total) == 1
