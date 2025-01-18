#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find fixed-point in sorted array of integers.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-12-22 (#273) and was classified as Easy.

  Reported source: Apple.

  A fixed point in an array is an element whose value is equal to its
  index. Given a sorted array of distinct elements, return a fixed
  point, if one exists. Otherwise, return False.

  For example, given [-6, 0, 2, 40], you should return 2. Given [1, 5,
  7, 8], you should return False.


* Solution

Rather than returning just True or False, my solution will offer proof
of its claim that a fixed point exists by returning the fixed point's
index.

The obvious approach is to scan the sorted input array, let's call it
A, looking for any index i such that A[i] = i. We can do this in O(n)
time and O(1) space, where n = len(A).

Can we do better?

We are told that A is a sorted array of distinct elements. Therefore,
we can think of A as a strongly monotonic function defined on the
integer values between 0 and len(A) - 1. As i increases, A[i] also
increases. If we plot A[i] vs. i, we'll get a series of points that
moves up and to the right.

Now let's superimpose the line for the function f(i) = i onto our
plot. Any point A[i] that lands on that line must be a fixed point,
because at that point A[i] = i. Therefore, to find a fixed point of A,
we need only to find where A[i] intersects the line.

To find an intersection (if one exists), let's pick an arbitrary value
of i.  If A[i] = i, then we've found a fixed point and are done. If
A[i] < i, then we know that A[i - 1] < i - 1 as well (because A is
strictly monotonic) and, going further, for all j < i, A[j] < j.
Therefore, we can eliminate i and everything to its left from
consideration in our search for the intersection. Likewise, if A[i] >
i, we can eliminate i and everything to its right.

These facts suggest that we can use a binary search to rapidly exclude
irrelevant halves of graph from our search and find an intersection in
O(lg n) time if it exists.

"""

import random


# O(n) time and O(1) space.
def find_fixed_point(A):
    """Finds an i in A such that A[i] = i; or None if no such i exists."""
    for i, a in enumerate(A):
        if i == a:
            return i
    return None


# O(lg n) time and O(1) space.
def fast_find_fixed_point(A):
    """Finds an i in A such that A[i] = i; or None if no such i exists."""
    lo = 0
    hi = len(A) - 1
    # Binary search.
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        a = A[mid]
        if a < mid:
            lo = mid + 1
        elif a > mid:
            hi = mid - 1
        else:
            return mid
    return None


# Tests.


def test():
    for soln in find_fixed_point, fast_find_fixed_point:
        print("testing {}".format(soln.__name__))

        # Cases from the problem statement.
        assert soln([-6, 0, 2, 40]) == 2
        assert soln([1, 5, 7, 8]) is None

        # Empty case.
        assert soln([]) is None

        # Singleton cases.
        for i in range(1, 10):
            assert soln([-i]) is None
            assert soln([0]) == 0
            assert soln([i]) is None

        # On-the-fixed-point-line cases.
        for n in range(1, 10):
            assert soln(list(range(n))) in range(n)

        # Single intersection cases.
        for i in range(10):
            # Try 100 random sequences that intersect at i.
            for _ in range(100):
                # Make i into a point of intersection.
                A = [0] * 10
                A[i] = i
                # Build steep monotonic sequences around i to fill out A.
                for offset in range(1, 10):
                    j = i + offset
                    if j < len(A):
                        A[j] = A[j - 1] + random.randint(2, 5)
                    j = i - offset
                    if j >= 0:
                        A[j] = A[j + 1] - random.randint(2, 5)
                assert soln(A) == i  # The solver must find the intersection.

        # Monotonic sequences above and below the fixed-point line
        # have no fixed points.
        for i in range(10):
            assert soln(list(range(i - 10, i))) is None
            assert soln(list(range(i + 10, i + 20))) is None
