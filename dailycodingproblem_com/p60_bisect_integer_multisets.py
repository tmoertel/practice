#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: partition a list of integers into two lists of equal sums.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-05-23 (#60) and was classified as Medium.

  Reported source: Facebook.

  Given a multiset of integers, return whether it can be partitioned
  into two subsets whose sums are the same.

  For example, given the multiset {15, 5, 20, 10, 35, 15, 10}, it
  would return true, since we can split it up into {15, 5, 10, 15, 10}
  and {20, 35}, which both add up to 55.

  Given the multiset {15, 5, 20, 10, 35}, it would return false, since
  we can't split it up into two subsets that add up to the same sum.

"""

import functools
import random

def is_bisectable(xs):
    """Returns True iff xs can be partitioned into 2 multisets of equal sums."""
    # Compute facts about the input.
    xs = sorted(xs)
    end = len(xs)
    total = sum(xs)

    # Define a helper function that our solution will require.
    @memoize
    def has_subset_sum(subset_sum, start=0):
        """Returns true iff any subset of xs[start:] has a given sum."""
        # An empty list can only sum to zero.
        if start == end:
            return subset_sum == 0
        # A non-empty list xs[start:] has a first element x, and x can
        # be included in the subset sum or not.
        x = xs[start]
        if x >= 0 and subset_sum < 0:
            return False
        return (has_subset_sum(subset_sum, start + 1) or
                has_subset_sum(subset_sum - x, start + 1))

    # If xs can be partitioned into two multisets of equal sums, the
    # total of its elements must be 2*n for some integer n, and some
    # subset of the elements must sum to n (as must the remaining
    # elements). Therefore, if the total of all elements is even and
    # we can find some subset of elements summing to half the total,
    # then xs can be partitioned as desired.
    return total % 2 == 0 and has_subset_sum(total // 2)

def memoize(f):
    """Makes a memoized version of f that returns cached results."""
    cache = {}
    @functools.wraps(f)
    def g(*args):
        ret = cache.get(args, cache)
        if ret is cache:
            ret = cache[args] = f(*args)
        return ret
    return g

def test():
    assert is_bisectable([])
    assert is_bisectable([0])
    assert is_bisectable([0, 0])
    assert is_bisectable([-1, -1])
    assert is_bisectable([-1, 0, -1])
    # Property: For all sets of integers xs, and even n >= 0, the
    # multiset formed by n copies of xs is bisectable.
    for size in range(7):
        for n in range(0, 7, 2):
            xs = random.sample(list(range(-10, 11)), size)
            assert is_bisectable(xs * n)
    # Some non-bisectable cases.
    assert not is_bisectable([1])
    assert not is_bisectable([0, 1])
    assert not is_bisectable([1, 3])
    # Cases from the problem statement.
    assert is_bisectable([15, 5, 20, 10, 35, 15, 10])
    assert not is_bisectable([15, 5, 20, 10, 35])
