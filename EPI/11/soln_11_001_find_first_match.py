#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-11-15

"""Solution to "Find First Occurrence", problem 11.1 in EPI.

"Problem 11.1 : Write a method that takes a sorted array A and a key k
and returns the index of the first occurrence of k in A. Return -1 if
k does not appear in A."  Source: _Elements of Programming
Interviews._

Discussion.  This function requires a straightforward binary search.
The only wrinkle is that if a matching element is found, we cannot be
certain that it is the left-most matching element and must search
leftward.  This we could do with a linear search but, in the worst
case when all of the elements in the array match, this leads to
linear-time performance.  So it is best to use another binary search
to find the left-most match.  But this second search can be folded
into the first.  Compare the first and second implementations below to
see how it is done.  Both have the desired O(log N) runtime to find a
match within an array of length N.

"""


def find_first_1(A, k):
    """Find index of first instance of k in sorted array A, -1 if not found."""
    lo, hi = 0, len(A) - 1
    while lo <= hi:
        mid = lo + ((hi - lo) >> 1)
        if A[mid] < k:
            lo = mid + 1
        elif A[mid] > k:
            hi = mid - 1
        else:
            # found a match; now bisect to find first *first* match.
            # note that this subsearch can be folded into the outer
            # search (see version of find_first below)
            hi = mid
            while lo < hi:
                mid = lo + ((hi - lo) >> 1)
                if A[mid] < k:
                    lo = mid + 1
                else:
                    hi = mid
            return lo
    return -1  # not found


def find_first(A, k):
    """Find index of first instance of k in sorted array A, -1 if not found."""
    lo, hi = 0, len(A) - 1
    while lo <= hi:
        mid = lo + ((hi - lo) >> 1)
        if A[mid] < k:
            lo = mid + 1
        elif A[mid] > k:
            hi = mid - 1
        else:
            hi = mid
            if lo == hi:
                return lo
    return -1  # not found
