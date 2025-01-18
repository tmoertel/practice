#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to interview problem: maximum value of each k-length subarray.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-04-11 (#18) and was classified as Hard.

  Reported source: Google.

  Given an array of integers and a number k, where 1 <= k <= length of
  the array, compute the maximum values of each subarray of length k.

  For example, given array = [10, 5, 2, 7, 8, 7] and k = 3, we should
  get: [10, 7, 8, 8], since:

  10 = max(10, 5, 2)
  7 = max(5, 2, 7)
  8 = max(2, 7, 8)
  8 = max(7, 8, 7)

  Do this in O(n) time and O(k) space. You can modify the input array
  in-place and you do not need to store the results. You can simply
  print them out as you compute them.

* Solution

The straightforward solution is to implement a direct translation of
the problem statement:

    def max_subarray_values(xs, k):
        return [max(xs[i:i+k]) for i in range(len(xs) - k + 1)]

This solution runs in O(n * k) time because it computes a fresh
maximum for each of the O(n) possible k-length slices of the array.

We can make the solution faster by exploiting the observation that as
we slide a k-length window over the array, if x is the newest element
in the window, no other window element y can ever contribute to the
maximum of the current window, or any future window containing x,
unless y is greater than x. Therefore, as soon as x enters the window,
it dominates all other window elements <= x, and we can eliminate them
from consideration.

For example, consider the input array [1, 0, 4, 3, 2, 1, 5] for k = 3.
Here are the k-length windows from left to right, where `start`
indicates the starting index of the window, and `end` indicates the
ending index. (We follow the Python convention that the window
contains all elements having indices i where start <= i < end).

   window
          x
   [1, 0, 4]  start=0 end=3 window_max=4
   [0, 4, 3]  start=1 end=4 window_max=4
   [4, 3, 2]  start=2 end=5 window_max=4
   [3, 2, 1]  start=3 end=6 window_max=3
   [2, 1, 5]  start=4 end=7 window_max=5

Now let's apply the rule that when x enters the window, it dominates
all lesser or equal elements, and we can cull them. Here I use a dash
to denote a culled element:

   window     culled
              window
          x          x
   [1, 0, 4]  [-, -, 4]  start=0 end=3 window_max=4
   [0, 4, 3]  [-, 4, 3]  start=1 end=4 window_max=4
   [4, 3, 2]  [4, 3, 2]  start=2 end=5 window_max=4
   [3, 2, 1]  [3, 2, 1]  start=3 end=6 window_max=3
   [2, 1, 5]  [-, -, 5]  start=4 end=7 window_max=5

Notice how the leftmost surviving element in each window is also its
maximum. This property is guaranteed by the fact that the surviving
elements must form a strictly decreasing sequence: For any two
positions i and j in the window, if i < j, then xs[i] must be greater
than xs[j] because, if it were not, then it would have been eliminated
when xs[j] entered the window.

This happy fact allows us to solve the problem in O(n) time for the
price of an k-length double-ended queue to maintain the surviving
elements of the window: Before we add an element x to the right end of
the window, we remove from that end any elements that are <= x. Once
we hit an element y > x, we can stop because we know that when y was
added, it eliminated all elements <= y and since x < y, all elements
<= x are also <= y. Therefore, we can be assured that each element in
the array will be added to the queue once, tested for removal at most
twice, and removed at most once. Additionally, the left end of the
queue will be read and popped n - k + 1 times. All of these are
O(1)-time operations, and we need O(n) of them, for an overall run
time of O(n).

"""

import collections
import itertools
import random

WindowEntry = collections.namedtuple("WindowEntry", "index value")


def max_subarray_values(xs, k):
    """Yields the maximum of each sequential k-length subarray of xs."""
    # Sanity check the problem instance.
    n = len(xs)
    if n == 0 or n < k:
        return
    assert 1 <= k <= n

    # Helpers to maintain a window of local maxima over a span of elements.
    window = collections.deque()

    def window_add(x, i):
        """Adds `x` to the end of a k-length window ending at index `i`."""
        # Remove any elements before the start of the current window.
        start = i - k
        while window and window[0].index < start:
            window.popleft()
        # Remove from the end of the window any elements that are dominated
        # by the new end element x.
        while window and window[-1].value <= x:
            window.pop()
        # Attach the new end element.
        window.append(WindowEntry(i - 1, x))

    def window_max():
        return window[0].value

    # Scan the entire array, adding the current element to the end of
    # the sliding window and emitting the per-window maxima once the
    # window spans a full k elements.
    for i, x in enumerate(xs, 1):
        window_add(x, i)
        if i >= k:
            yield window_max()


def test():
    def oracle(xs, k):
        return [max(xs[i : i + k]) for i in range(len(xs) - k + 1)]

    for soln in (max_subarray_values,):
        for i in range(7):
            for xs in itertools.permutations(list(range(i))):
                for k in range(1, i + 1):
                    xs = list(xs)
                    expected = oracle(xs, k)
                    print("\nsoln(xs={}, k={}) => {}".format(xs, k, expected))
                    observed = list(soln(xs, k))
                    assert observed == expected
