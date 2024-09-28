#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find the minimum element of a rotated sorted list.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2020-12-28 (#636) and was classified as Medium:

  Reported source: Uber.

  Suppose an array sorted in ascending order is rotated at some pivot
  unknown to you beforehand. Find the minimum element in O(log N)
  time. You may assume the array does not contain duplicates.

  For example, given [5, 7, 10, 3, 4], return 3.


* Solution

Consider an array A of length n containing distinct values sorted into
ascending order. Now suppose that we rotate A to the left by k positions to
form the rotated array R = A[k:] + A[:k]. Note that R is formed from two
ascending sequences:

  S1 = A[k:], containing the greatest elements from A
  S2 = A[:k], containing the least elements from A

Also, we should be aware that S2 will be empty when k = 0. With this in
mind, we can find the least element of R as follows:

1. If S2 is empty, which is the case if and only if S1 spans all of R and
   thus R[0] <= R[n - 1], we know that min(R) = R[0], and we're done.

2. Otherwise, S2 must be nonempty and min(R) = S2[0]. But we have to find
   where S2 begins!

To find S2 in R, recall that S1 precedes S2, and all values in S1 are
greater than all values in S2. Thus, for any range of elements R[i:j+1], if
R[i] > R[j], we know that the range must contain some trailing part of S1
followed by some leading part of S2. And, since the first element of S2 is
R's minimum, we know the minimum must reside in R[i:j+1].

With this fact in mind, we can employ a binary search strategy over R,
repeatedly narrowing into whichever half contains the minimum until we've
resolved the range to a single element.


* Performance analysis

I offer two implementations below, one recursive and one iterative. Both
implement a binary search and thus run in O(lg n) time. The recursive
implementation runs in O(lg n) space. (It would run in O(1) space were
Python to guarantee tall-call elimination, as all its recursive calls are
tail calls.) The iterative implementation runs in O(1) space: it uses only a
constant number of O(1)-size variables to do its work.

"""

def find_min_of_rotated_sorted_distinct_elements_recursive(xs):
    """Finds the min element in a rotated sorted array of distinct values."""
    if not xs:
        raise ValueError
    # Use a recursive binary search for the minimum element.
    def search(start, end):
        # If the series is nondecreasing, its first element is its minimum.
        # (Note that this test is always true if we've narrowed the range
        # to a single element and serves as a base case to terminate our
        # binary search.)
        if xs[start] <= xs[end]:
            return xs[start]
        # Otherwise, bisect the series and eliminate the half that does not
        # contain the minimum. (In the case when the series has been
        # narrowed to just two elements, we'll end up comparing the first
        # element to itself and eliminating it. This is always correct,
        # however, because the previous if statement ruled out the
        # possibility that the series is ascending; thus, the the second
        # element must be the minimum.)
        mid = start + (end - start) // 2
        if xs[start] > xs[mid]:
            # The first half decreases somewhere, so the minimum must be in it.
            return search(start, mid)
        else:
            # Otherwise, the minimum must be in the second half.
            return search(mid + 1, end)

    # Initiate the search over the entire input sequence.
    return search(0, len(xs) - 1)


# This is an iterative implementation of the recursive algorithm given
# in the preceding function. I created it by translating the recursive
# algorithm using the methods I describe in this blog post:
# http://blog.moertel.com/posts/2013-05-11-recursive-to-iterative.html
def find_min_of_rotated_sorted_distinct_elements(xs):
    """Finds the min element in a rotated sorted array of distinct values."""
    if not xs:
        raise ValueError
    start = 0
    end = len(xs) - 1
    while start <= end and xs[start] > xs[end]:
        mid = start + (end - start) // 2
        if xs[start] > xs[mid]:
            end = mid
        else:
            start = mid + 1
    return xs[start]


# Tests.


from nose.tools import eq_, raises


def test_base_cases():
    for soln in (find_min_of_rotated_sorted_distinct_elements,
                 find_min_of_rotated_sorted_distinct_elements_recursive):
        raises(ValueError)(soln)([])
        eq_(soln([1]), 1)
        eq_(soln([1, 2]), 1)
        eq_(soln([2, 1]), 1)
        eq_(soln([1, 2, 3]), 1)
        eq_(soln([2, 3, 1]), 1)
        eq_(soln([3, 1, 2]), 1)


def test_soln_finds_minumum_of_a_rotated_sorted_list_of_distinct_values():
    for soln in (find_min_of_rotated_sorted_distinct_elements,
                 find_min_of_rotated_sorted_distinct_elements_recursive):
        for size in range(1, 10):
            sorted_range = list(range(size))
            for pivot in range(size):
                rotated_sorted_range = sorted_range[pivot:] + sorted_range[:pivot]
                eq_(soln(rotated_sorted_range), 0)
