#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find an element in a sorted array using limited ops.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2021-01-23 (#661) and was classified as Hard:

  This problem was asked by Netflix.

  Given a sorted list of integers of length N, determine if an element
  x is in the list without performing any multiplication, division, or
  bit-shift operations.

  Do this in O(log N) time.


* Solution

The obvious solution to this problem would be a binary search, were
there no restrictions on the operations we could employ. But since we
can't use multiplications, divisions, or bit shifts, it's tricky to
implement the division by 2 that lies at the heart of a binary search.

** Division by 2 without division

However, there are still ways we can divide by 2 without using any of
the forbidden operators. For example, division on the positive real
numbers maps to subtraction if we first transform the reals by the
logarithm function. Thus we can find i/2 as exp(log(i) - log(2)) for
all i > 0. We have to be careful about 0, since it maps to negative
infinity under logarithm, but dividing 0 by 2 is just 0, so it's easy
to handle as a special case.

Since these operations can all be performed in O(1) time and space,
using them to implement division by 2 in a standard binary search
preserves the search's low O(1) space and O(lg n) time costs.

** Pseudobinary search

Another option that springs to mind is to forego the division
altogether and *randomly* choose where to split the search space. It's
less obvious that this strategy preserves the low O(lg n) time cost,
but it does (in expectation). Proving it is a little tricky, however.

My proof will follow Kleinberg and Tardos's analysis of quickselect
in their book _Algorithmn Design_. The basic idea is to express the
overall runtime in phases. We start in phase 0 and enter phase 1 as
soon as the algorithm has reduced the search space by 25%. We enter
phase 2 as soon as we've reduced this smaller search space by another
25%, and so on. Thus in phase j, the active range of the array will
be between (3/4)^j and (3/4)^(j+1) of its original size. For an array
of size n, there can be at most k = ceil(log(n)/log(4/3)) phases. So,
if we let X[j] denote the time the algorithmn spends in phase j, then
the expected overall running time is given by

  T = E[ X[0] + X[1] + ... X[k-1] ]

which, because expectation is linear, is equal to

  T = E[X[0]] + E[X[1]] + ... E[X[k-1]].

Since the algorithmn doesn't care what phase it's in, all of the X[j]
terms have the same expectation. We can estimate the expected run time
of one X[j] by observing that if the algorithm chooses a random pivot
within the middle 50% of elements, which occurs with probability 1/2,
then even if the algorithm ends up discarding the smaller "half" of
the active range, the range will have been reduced by 25%. If we let
Y be the expected number of iterations before we randomly select a
middle-50% pivot, we have

   Y = 1 + (1/2) * 0 + (1/2) * Y

Solving for Y gives us Y = 2. Hence, the expected number of
iterations in each phase is at most 2. And since the work done in each
iteration is constant time, X[j] ≤ 2 * c for some constant c. Thus the
overall running time is given by

  T = E[X[0]] + E[X[1]] + ... E[X[k-1]]
    ≤ 2 * c * k
    = 2 * c * log(n) / log(4/3),

which is in O(log n). QED.


"""

import math
import random


# The logarithm of 2. We'll subtract this from log(x) to "divide" x by 2.
LOG2 = math.log(2)


def half(i):
    """Returns the int nearest i/2."""
    # The logarithm of 0 is negative infinity, so we handle 0 as a special case.
    if i == 0:
        return 0
    # For the general case, we rely on the fact that a/b = exp(log(a) - log(b))
    # for all a, b > 0.
    return int(math.exp(math.log(i) - LOG2) + 0.5)


def binary_search(x, xs, split=half):
    """Finds an index of x in the sorted list xs; returns -1 if x is not in xs.

    The `split` argument gives the strategy for splitting the search space.
    Given a distance bewteen index endpoints, it must return the distance
    at which to make the split. For a vanilla binary search, we would set
    `split` to a function that divides by 2.

    """
    lo = 0
    hi = len(xs) - 1

    while lo <= hi:
        pivot = lo + split(hi - lo)
        y = xs[pivot]
        if y < x:
            lo = pivot + 1
        elif y > x:
            hi = pivot - 1
        else:
            return pivot
    return -1


def random_split(size):
    return random.randint(0, size)


def pseudobinary_search(x, xs):
    return binary_search(x, xs, split=random_split)


# Tests.


from nose.tools import eq_, raises


def test_binary_search():
    _test(binary_search)


def test_pseudobinary_search():
    _test(pseudobinary_search)


def _test(soln):
    # Edge case: We can never find the value if the list is empty.
    eq_(soln(1, []), -1)

    # General case: Generate random trials for increasing problem sizes.
    for problem_size in range(1, 7):
        print(f'Trying problems of size {problem_size}.')
        for _ in range(2 * math.factorial(problem_size)):
            # Construct a random sorted array of ints.
            xs = sorted(random.randint(-problem_size, problem_size)
                        for _ in range(problem_size))

            # Find a random value in the array.
            an_x_in_xs = xs[random.randrange(problem_size)]
            # The solution should find an index of that value.
            index = soln(an_x_in_xs, xs)
            eq_(xs[index], an_x_in_xs)

            # Now find a random value that's not in the array.
            while True:
                an_x_not_in_xs = random.randint(
                    -2 * problem_size, 2 * problem_size)
                if an_x_not_in_xs not in xs:
                    break
            # The solution should not find any corresponding index.
            eq_(soln(an_x_not_in_xs, xs), -1)
