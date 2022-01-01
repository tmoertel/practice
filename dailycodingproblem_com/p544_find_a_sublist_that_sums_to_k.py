#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find a sublist that sums to k.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2020-09-22 (#544) and was classified as Hard:

  Reported source: Google.

  Given a list of integers S and a target number k, write a function
  that returns a subset of S that adds up to k. If such a subset
  cannot be made, then return null.

  Integers can appear more than once in the list. You may assume all
  numbers in the list are positive.

  For example, given S = [12, 1, 61, 5, 9, 2] and k = 24, return [12,
  9, 2, 1] since it sums up to 24.


* Solution


"""

def subset_sum(vals, k):
    """Returns a subset of `vals` summing to `k` or None if not possible.

    REQUIRES that all values in `vals` are non-negative.

    """
    return sublist_sum(set(vals), k)


def sublist_sum(vals, k):
    """Returns a sublist of `vals` summing to `k` or None if not possible.

    REQUIRES that all values in `vals` are non-negative.

    """
    # Special case: the empty sublist is the preferred way to sum to zero.
    if k == 0:
        return []

    # Search for sums we can reach by adding (or not) each of the given values.
    reachable_sums = {0: None}
    def search_for_sublist_summing_to_k():
        for val in vals:
            if val == 0:
                continue  # There's no reason to include 0 in a sum.
            for reachable_sum in list(reachable_sums):
                new_reachable_sum = val + reachable_sum
                if new_reachable_sum > k:
                    continue  # We can never reach k from sums exceeding k.
                reachable_sums.setdefault(new_reachable_sum, val)
                if new_reachable_sum == k:
                    return  # We found a sublist that sums to k! Exit the search.
    search_for_sublist_summing_to_k()

    # Can we reach the target value k?
    if k not in reachable_sums:
        return None  # Nope.

    # Yes, trace back the path that sums to k.
    back_path = []
    while True:
        val = reachable_sums[k]
        if val is None:
            break
        back_path.append(val)
        k -= val
    # Return the reversed path back. It will be the first sublist of
    # `vals` that sums to `k`.
    return list(reversed(back_path))


# Tests.

from nose.tools import eq_, raises

def test_base_cases():
    eq_(sublist_sum([], 0), [])
    eq_(sublist_sum([], 1), None)
    eq_(sublist_sum([1], 1), [1])
    eq_(sublist_sum([1, 1], 1), [1])
    eq_(sublist_sum([1, 1], 2), [1, 1])
    eq_(subset_sum ([1, 1], 2), None)
    eq_(sublist_sum([1, 2], 0), [])
    eq_(sublist_sum([1, 2], 1), [1])
    eq_(sublist_sum([1, 2], 2), [2])
    eq_(sublist_sum([1, 2], 3), [1, 2])
