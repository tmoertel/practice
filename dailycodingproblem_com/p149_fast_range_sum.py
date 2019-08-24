#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: quickly compute range sums over an array.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-08-20 (#149) and was classified as Hard.

  This problem was asked by Goldman Sachs.

  Given a list of numbers L, implement a method sum(i, j) which
  returns the sum from the sublist L[i:j] (including i, excluding j).

  For example, given L = [1, 2, 3, 4, 5], sum(1, 3) should return
  sum([2, 3]), which is 5.

  You can assume that you can do some pre-processing. sum() should be
  optimized over the pre-processing step.

* Solution

This problem can be quickly solved in terms of running totals. As a
preprocessing step, we create a running-total array T whose ith
element is the sum of the elements in L whose index is less than i.
For example, T[2] = L[0] + L[1]. Since T[0] = 0 by definition and

  T[i] - T[i - 1] = L[i - 1]   for all i > 0,

we can build the entire array T in linear time by starting from T[0]:

  T[0] = 0
  T[i] = T[i - 1] + L[i - 1] for all i > 0

Once T is computed, we can compute sum(L[i:j]) in constant time for
any 0 <= i <= j < len(L):

  sum(L[i:j]) = T[j] - T[i].

"""

def make_fast_range_summer(xs):
    """Returns a function f such that f(i, j) = sum(xs[i:j])."""
    n = len(xs)
    # Preprocessing: compute the running totals of xs's elements.
    total = 0
    running_totals = [0]
    for x in xs:
        total += x
        running_totals.append(total)
    # Return a function that returns sum(xs[i:j]) in O(1) time.
    def range_sum(i, j):
        assert i <= j <= n
        return running_totals[j] - running_totals[i]
    return range_sum

def test():
    L = [1, 2, 3, 4, 5]
    f = make_fast_range_summer(L)
    for i in range(5):
        assert f(i, i) == 0
        assert f(i, i + 1) == L[i]
    assert f(1, 3) == 5

