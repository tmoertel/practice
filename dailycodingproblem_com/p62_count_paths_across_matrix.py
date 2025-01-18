#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: count the monotonic paths across a matrix.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-05-25 (#62) and was classified as Medium.

  Reported source: Facebook.

  There is an N by M matrix of zeroes. Given N and M, write a function
  to count the number of ways of starting at the top-left corner and
  getting to the bottom-right corner. You can only move right or down.

  For example, given a 2 by 2 matrix, you should return 2, since there
  are two ways to get to the bottom-right:

  Right, then down
  Down, then right

  Given a 5 by 5 matrix, there are 70 ways to get to the bottom-right.


* Solution

The problem statement asks us to cross an NxM matrix from the
upper-left corner to the lower-right corner via a series of one-cell
steps limited to the down and right directions. Note that steps down
only change the current row, and steps right only change the current
column. Therefore, any valid path must comprise N - 1 down steps and
M - 1 right steps.

How many ways are there to construct such a path? Here's a recipe to
construct one arbitrarily:

  Choose, from the N + M - 2 steps in the path, the locations of
  the N - 1 down steps.

  Fill in the remaining locations with right steps.

Recall from combinatorics that the number of ways to do the "choose"
step is given by

  C(N + M - 2, N - 1)

where C(n, k) is a binomial coefficient.

The solution, then, is to compute the binomial coefficient
corresponding to the problem instance we are given. We can do this in
O(min(M, N)) time and O(1) memory by exploiting the recurrence
C(n, k) = n * C(n - 1, k - 1) / k.

"""


def choose(n, k):
    """Returns the number of ways to choose k items from n items."""
    if k > n:
        return 0
    # Since C(n, k) = C(n, n - k), find C(n, n - k) if it's quicker.
    if k > n - k:
        k = n - k
    # We exploit the recurrence C(n, k) = n * C(n - 1, k - 1) // k,
    # working up from the base case C(n - k, 0) = 1.
    n -= k
    ways = 1
    for k in range(1, k + 1):
        n += 1
        ways = n * ways // k
    return ways


def count_corner_to_corner_paths(n, m):
    """Counts the ways to cross an n-by-m matrix via down and right steps."""
    return choose(n + m - 2, n - 1)


def test():
    assert count_corner_to_corner_paths(2, 2) == 2
    assert count_corner_to_corner_paths(5, 5) == 70
