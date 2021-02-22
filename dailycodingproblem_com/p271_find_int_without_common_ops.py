#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: binary search without common operations.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-12-20 (#271) and was classified as Hard.

  This problem was asked by Netflix.

  Given a sorted list of integers of length N, determine if an element
  x is in the list without performing any multiplication, division, or
  bit-shift operations.

  Do this in O(log N) time.


* Solution

A binary search finds the element in O(log N) time, but the standard
implementation halves the range of interest by computing its midpoint
using a division:

  mid = lo + (hi - lo) // 2.

In this problem, division is verboten, so we must use another method
to find the midpoint:

  mid = lo + find_midpoint(hi - lo)

What possible implementations are there? Here are some that I came up
with:

1. Log transform. Since n = exp(log(n)) for all n > 0, and since division
becomes subtraction under a log transform, we can compute n/2 as follows:

  def divide_by_two_via_log_transform(n):
      # For n > 0, n / 2 == exp(log(n) - log(2)).
      if n == 0:
          return 0
      return int(math.exp(math.log(n) - math.log(2)) + 0.5)

2. Random guess. Don't find the midpoint: just select a random index
in the range 0 through n, inclusive:

  def guess_half(n):
      return random.randint(0, n)

A binary search using this method of finding the midpoint still runs
in O(lg N) expected time because, on average, we'll be able to discard
a quarter of the active range in at most two iterations, limiting the
number of iterations to O(log(n)/log(4/3)) = O(log n), just as in the
quickselect algorithm with random pivots.

3. Probable midpoint. Improving on the random guess, we could take several
guesses and return the one that is the most central:

  def probabilistic_half(n, guesses=3):
      best_guess = best_inbalance = None
      for _ in range(guesses):
          guess = guess_half(n)
          inbalance = abs((n - guess) - guess)
          if best_inbalance is None or inbalance < best_inbalance:
              best_inbalance = inbalance
              best_guess = guess
      return best_guess

Note that when guesses=1, probabilistic_half becomes guess_half. As
`guesses` increases, the returned "halves" become more tightly
clustered around the true half.

However, better guesses don't really buy us much in this case because
the additional complexity of taking another guess is about the same as
iterating again in the binary search, so we're better off doing the
latter as that approach ensures that the active search range is always
reduced with each additional guess.

Nevertheless, all of these midpoint strategies allow us to perform
the binary search in expected O(lg N) time and O(1) space.

"""

import math
import random

# A generic binary search that lets us replace the normal midpoint
# selection method, dividing by two, with one of our choosing.

def divide_by_two(n):
    return n // 2

def find_value(xs, x, find_midpoint=divide_by_two):
    """Finds the index of a value x in a sorted list xs."""
    lo, hi = 0, len(xs) - 1
    while lo <= hi:
        mid = lo + find_midpoint(hi - lo)
        y = xs[mid]
        if x < y:
            hi = mid - 1
        elif x > y:
            lo = mid + 1
        else:
            return mid
    return None


# Some alternative strategies for finding the midpoint of the
# range 0 to n, inclusive. We can use them to replace division
# by two in our binary search.

def divide_by_two_via_log_transform(n):
    # For n > 0, n / 2 == exp(log(n) - log(2)).
    if n == 0:
        return 0
    return int(math.exp(math.log(n) - math.log(2)) + 0.5)

def guess_half(n):
    return random.randint(0, n)

def probabilistic_half(n, guesses=3):
    best_guess = best_inbalance = None
    for _ in range(guesses):
        guess = guess_half(n)
        inbalance = abs((n - guess) - guess)
        if best_inbalance is None or inbalance < best_inbalance:
            best_inbalance = inbalance
            best_guess = guess
    return best_guess

MIDPOINT_IMPLEMENTATIONS = (
    divide_by_two,
    divide_by_two_via_log_transform,
    guess_half,
    probabilistic_half)


# Tests: Show that all of the midpoint methods work in the search.

def test():
    for find_midpoint in MIDPOINT_IMPLEMENTATIONS:
        print 'testing half={}'.format(find_midpoint.__name__)

        # Create a binary search using our midpoint method.
        def find(xs, x):
            return find_value(xs, x, find_midpoint)

        # Now test the search.

        # For all x, we can't find x in an empty list.
        for x in range(10):
            assert find([], x) == None

        # For all x, we can't find x in a list of ints < x.
        for x in range(10):
            for n in range(10):
                assert find(list(range(x)), x) == None

        # For all x, we can't find x in a list of ints > x.
        for x in range(10):
            for n in range(10):
                assert find(list(range(x + 1, x + n + 1)), x) == None

        # For all x, x is always at index 0 of [x].
        for x in range(10):
            assert find([x], x) == 0

        # For all x and natural numbers n > 0, x's indices in [x] * n
        # must be in the semi-closed range [0, n).
        for _ in range(100):
            n = random.randint(1, 10)
            assert find([x] * n, x) in range(0, n)

        # For all x and natural numbers n > 0, x's indicies in
        # sorted(ℕ*i) are in the semi-closed range [x*n, (x+1)*n),
        # where ℕ is a list of the natural numbers 0, 1, 2, ....
        natural_numbers = list(range(10))  # Approximate :-)
        for n in range(1, 10):
            xs = sorted(natural_numbers * n)
            for x in range(10):
                assert find(xs, x) in range(x * n, (x + 1) * n)
