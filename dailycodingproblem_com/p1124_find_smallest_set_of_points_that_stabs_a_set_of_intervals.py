#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find the smallest point set that "stabs" given intervals.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2022-06-11 (#1124) and was classified as Hard:

  Reported source: Microsoft.

  Given a set of intervals on the real line, return the smallest set
  of points such that every interval contains at least one point.

  For example, given the intervals [(0, 4), (4, 6), (8, 9), (9, 11)],
  you should return [4, 9].


* Solution

At first this might seem like a ridiculously difficult problem: it
asks for a set covering! But a couple of observations show this
particular instance of the problem to be much easier.

The first observation is that a minimal set of covering points can
always be constructed from the terminal points of the given intervals.
For proof, assume that you have a minimal set of covering points, and
some of those points are not terminal points. Then you can always
convert this set into another minimal set by nudging each non-terminal
point rightward until it hits the nearest terminal point. Thus all
minimal sets are equivalent to a minimal set composed of terminal
points. This observation means that our problem simplifies to just
choosing which of the terminal points to include in our minimal set.

The second observation is that we must add the smallest terminal point
to our minimal set. If we don't, then the other terminal points could
be greater and thus unable to cover the interval terminated by the
smallest terminal point. This observation implies that if we have
sorted our terminal points, we must include the first one into our
minmial set. Then we can remove any interval that contains it from
further consideration. This leaves us with a smaller instance of our
original problem, for which the same observations still hold.

Thus we can repeatedly add the smallest remaining terminal point to
our minimal set, remove any intervals that the point covers, and
repeat until no terminal points remain. Since we will have covered
all intervals, and have done so with a minimal set of points, that
final set is the solution we want!


* Implementation

We can sort n terminal points in O(n lg n) time and scan them in O(n)
time. But when we induct a terminal point into our minimal set, how
can we quickly find the intervals that contain it and remove them
from the problem?

What I've done is to sort all of the endpoints, initial as well as
terminal. Then we can scan the endpoints from left to right. When we
hit an initial point, we can record that its interval has been opened
by adding its index to an opened set. When we hit a terminal point, we
can record that its interval -- and all other opened intervals -- are
now covered by moving them from the opened set into a covered set. In
this way, we can process all n of the enpoints in O(n) time: the set
operations are each O(1) time, and we never need to add or remove an
interval from a set more than once.

Thus our implementation's run time is dominated by the cost of sorting
the endpoints and runs in O(n lg n) time.

"""

def smallest_set_of_covering_points(intervals):
    # Sort the endpoints of the intervals so that we can scan them
    # from from left to right. When one interval ends at the same
    # point that another opens, we will order the opening point first.
    # This policy ensures that, at any point in the scan, we will have
    # opened all possible intervals before closing any intervals.
    points = []
    for i, (initial_point, terminal_point) in enumerate(intervals):
        points.extend([(initial_point, 0, i), (terminal_point, 1, i)])
    points.sort()
    # Scan end points from smallest to largest.
    opened_intervals = set()
    covered_intervals = set()
    covering_points = []
    for x, _, i in points:
        if i in opened_intervals:
            # This point x terminates an interval that we've opened
            # but not yet covered. If we don't include it as a
            # covering point, we cannot cover its interval. Therefore,
            # we must include it. Since our sort order guarantees that
            # all intervals which contain x have already been opened,
            # we can remove all intervals that x covers from further
            # consideration by copying `open_intervals` into
            # `covered_intervals`.
            covering_points.append(x)
            covered_intervals.update(opened_intervals)
            opened_intervals.clear()
        elif i in covered_intervals:
            # We can ignore intervals we've already covered.
            continue
        else:
            # This point doesn't belong to an interval we've opened or
            # covered; therefore it must open an interval.
            opened_intervals.add(i)
    # After we've processed all endpoints, we have a complete and
    # minimal set of covering points.
    return covering_points


# Tests.

from nose.tools import eq_, raises

def test_solution_for_example_must_be_correct():
    intervals = [(0, 4), (4, 6), (8, 9), (9, 11)]
    eq_(smallest_set_of_covering_points(intervals), [4, 9])

def test_empty_intervals_is_covered_by_empty_points():
    intervals = []
    eq_(smallest_set_of_covering_points(intervals), [])

def test_single_point_intervals_are_covered_by_their_sole_points():
    intervals = [(1, 1), (2, 2), (3.1, 3.1)]
    eq_(smallest_set_of_covering_points(intervals), [1, 2, 3.1])
