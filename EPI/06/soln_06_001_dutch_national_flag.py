#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-10-23

r"""Solution to "Dutch National Flag" problem, 6.1 from EPI.

    Write a function that takes an array A and an index i and
    rearranges the elements such that all elements less than A[i]
    appear first, followed by all elements equal to A[i], followed
    by elements greater than A[i].

Discussion.

This is the "Dutch National Flag" problem, which I have solved previously:

https://github.com/tmoertel/practice/blob/master/programming_praxis/dutch_national_flag.py

The idea is to maintain four partitions satisfying the following
invariant conditions w.r.t. the pivot x = A[i]:

    - an LT partition on the left for elements < x,
    - a GT partition on the right for elements > x,
    - a MID/EQ partition in the lift middle for elements = x, and
    - a MID/UNX partition in the right middle for unexamined elements.

Initially, the MID/UNX partition spans the entire array, and the other
partitions are empty.  But as we examine elements in MID/UNX, classify
them w.r.t. x, and swap them into their respective partitions, those
partitions will grow and the MID/UNX partition will shrink.  When
MID/UNX is finally empty, the invariant conditions on the other
partitions will ensure that the rearranged elements of A represent
a valid solution.

"""

def partition(A, i):
    """Rearrange A's elements into <, =, and > partitions on A[i]."""

    # Let the indices j, k, l give the start of MID/EQ, MID/UNX, and GT:
    #
    # 0123... j...    k...    l...
    # ||||    |       |       |
    # ======= ======= ======= =======
    # LT      MID/EQ  MID/UNX GT
    # A[ :j]  A[j:k]  A[k:l]  A[l: ]
    j, k, l = 0, 0, len(A)

    # make swap helper over A
    def swap(j, k):
        A[j], A[k] = A[k], A[j]

    # partition on x = A[i], maintaining invariant conditions
    x = A[i]
    while k < l:
        if A[k] < x:
            swap(k, j)
            j += 1
            k += 1
        elif A[k] == x:
            k += 1
        else:
            l -= 1
            swap(k, l)

    return A  # for convenient testing and chaining


def test():
    from nose.tools import assert_equal as eq
    from itertools import permutations
    def stable_partition(A, x):
        return ([a for a in A if a < x] +
                [a for a in A if a == x] +
                [a for a in A if a > x])
    for n in xrange(5):
        for A in permutations(range(n)):
            A = list(A)
            for i in xrange(n):
                x = A[i]
                AP = partition(A, i)
                eq(sorted(AP), sorted(A))  # must preserve all elems
                eq(AP, stable_partition(AP, x))  # must be a valid partition
