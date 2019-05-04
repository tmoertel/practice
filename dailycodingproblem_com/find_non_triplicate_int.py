#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to interview problem: find the non-triplicate element in an array.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-05-03 (#40) and was classified as Hard.

  This problem was asked by Google.

  Given an array of integers where every integer occurs three times
  except for one integer, which only occurs once, find and return the
  non-duplicated integer.

  For example, given [6, 1, 3, 3, 3, 6, 6], return 1. Given [13, 19,
  13, 13], return 19.

  Do this in O(N) time and O(1) space.

* Solution

Given the problem's construction, the array's length must be 3N + 1
for some integer N. This fact suggests a solution based on logic
similar to that behind the famous quickselect algorithm:

If we partition the elements in the array such that all elements
before index i are <= x and the remaining elements are > x, then the
singleton element we seek must be in one of the two partitions, and
that partition's length modulo 3 must be 1. Therefore, we can find the
partition having this length and focus on it as a smaller instance of
the original problem. We repeat this process until we've narrowed the
problem down to a partition of length 1, which must contain the
element we seek.

** Performance analysis

Recall that we can partition an array of length N in O(N) time and
O(1) space. Our solution requires us to repeatedly partition the input
array into smaller and smaller partitions, halving the length each
time in expectation. Thus, doing a bit of hand-waving around a
more-detailed probabilistic analysis, the time needed to find the lone
element is given by a sum like this one:

  N * (1 + 1/2 + 1/4 + 1/8 + ...) = N * O(1).

Thus our solution runs in O(1) space and O(N) expected time.

"""

import itertools
import random

def find_non_triplicate_element(xs):
    """Finds the one element in xs that does not occur three times."""
    lo, hi = 0, len(xs)
    # Loop until we've narrowed xs[lo:hi] to a single element.
    while lo < hi - 1:
        # Partition the array about a random pivot element.
        pivot_value = xs[lo + random.randrange(hi - lo)]
        dividing_index = partition(xs, pivot_value, lo, hi)
        # Narrow to the partition containing the singleton element.
        if ((dividing_index - lo) % 3 == 1):
            hi = dividing_index
        else:
            lo = dividing_index
    return xs[lo]

def partition(xs, x, lo, hi):
    """Partitions xs[lo:hi] into elems <= x and > x; returns divider."""
    # We maintain three partitions as we shrink the region between lo and hi:
    #   - elements before lo are known to be <= x
    #   - elements in xs[lo:hi] are unclassified
    #   - elements after hi are known to be > x
    while lo < hi:
        while lo < hi and xs[lo] <= x:
            lo += 1
        while lo < hi and xs[lo] > x:
            xs[hi - 1], xs[lo] = xs[lo], xs[hi - 1]
            hi -= 1
    # The middle partition is now empty, so the remaining two
    # partitions must span the entire input array.
    return lo  # Index after first partition.

def test():
    # Start small and work toward larger problem instances.
    for n in range(1, 7):
        for seq in itertools.permutations(range(n)):
            # Make a random problem instance with a known solution.
            seq = list(seq)
            singleton = seq[0]     # The first value is the singleton.
            seq[1:] = seq[1:] * 3  # The others are the triplicates.
            random.shuffle(seq)
            print '\nans = {}, seq = {}'.format(singleton, seq)
            # The solver must identify the singleton element.
            assert find_non_triplicate_element(seq) == singleton
