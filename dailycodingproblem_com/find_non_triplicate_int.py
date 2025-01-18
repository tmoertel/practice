#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to interview problem: find the non-triplicate element in an array.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-05-03 (#40) and was classified as Hard.

  Reported source: Google.

  You are given an array of integers in which each distinct integer
  occurs three times except for a lone integer which occurs only once.
  Return the lone integer.

  For example, given [2, 4, 1, 3, 3, 3, 4, 2, 2, 4], return 1.
  Given [13, 23, 13, 13], return 23.

  Do this in O(N) time and O(1) space.

* Solution 1

Given the problem's construction, the array's length must be 3N + 1
for some integer N. This fact suggests a solution based on logic
similar to that behind the famous quickselect algorithm:

If we partition the elements in the array such that all elements
before index i are <= x and the remaining elements are > x, then the
singleton element we seek must be in one of the two partitions, and
that partition's length modulo 3 must be 1. Therefore, we can find the
partition having this length and focus on it as a smaller instance of
the original problem. We repeat this process until we've narrowed the
problem down to a partition of length 1, which must contain the
element we seek.

I've implemented this solution in `find_non_triplicate_element_1`.

** Performance analysis

Recall that we can partition an array of length N in O(N) time and
O(1) space. Our solution requires us to repeatedly partition the input
array into smaller and smaller partitions, halving the length each
time in expectation. Thus, doing a bit of hand-waving around a
more-detailed probabilistic analysis, the time needed to find the lone
element is given by a sum like this one:

  N * (1 + 1/2 + 1/4 + 1/8 + ...) = N * O(1),

since the sum is a falling geometric series. Thus, our solution runs
in O(1) space and O(N) expected time.

* Solution 2

Our earlier observation, that an array containing N triplicate values
and one singleton value must have length 3N + 1, can be generalized.
Let P be an arbitrary predicate taking integers to booleans. If P is
true for the singleton, then it must be true for 3M + 1 of the array's
elements, for some integer M. Therefore, we can learn whether P is
true for the singleton by counting the number of times it is true for
*all* of the array's elements and checking whether the count modulo 3
is 1. Here's a sketch implementation in Python:

  def is_true_for_singleton(P, xs):
      '''Returns whether P is true for the singleton in array xs.'''
      true_count_mod_3 = 0
      for x in xs:
        if P(x):
          true_count_mod_3 = (true_count_mod_3 + 1) % 3
      return true_count_mod_3 == 1

Knowing whether a predicate is true for the singleton reveals one bit
of information about the singleton. For example, consider a predicate
P_odd that is true for odd integers and false otherwise. If we learn
that P_odd is true for the singleton, we have also learned that the
least significant bit in the singleton's binary representation is 1;
otherwise, it must be 0.

Continuing this thinking, what if we create a family of 64 related
predicates P[i] for i = 0..63, such that P[i] is true when a value's
ith bit is set, and false otherwise? Then we could apply this family
to the array to determine the full binary representation of the
singleton (assuming it fits into 64 bits).

This solution requires 64 passes through the array and a 64-bit
accumulator to hold the bits of the singleton as we determine them.
But 64 is a constant, which washes out in big-O analysis! So this
solution actually runs in O(N) time and O(1) space. I've implemented
this solution below in `find_non_triplicate_element_2`.

In practice, however, making 64 passes through the array is pretty
expensive. Is there a way to do the work in just one pass?

For inspiration, consider that the counts we accumulate while scanning
the array are over integers modulo 3, and thus only take on the values
0, 1, and 2, each of which will fit into a 2-bit register.

So one possible solution would be to accumulate counts in 64 of those
2-bit registers, one for each bit position, while we scan the array
just once. Further, we can implement the 64 2-bit registers using 2
64-bit registers: the first register, `ones`, will hold the bits in
the ones positions of all of the 2-bit registers, and the second
register, `twos`, will hold the bits in the twos positions. That is,
the 2-bit count for bit position i is given in terms of `twos`
and `ones` by this formula:

  count[i] = 2 * (bit i of `twos`) + (bit i of `ones`).

To make use of this trick, we can't use normal arithmetic operators to
accumulate our counts. They're not designed to interpret two 64-bit
integers as 64 separate 2-bit integers. Instead, we'll have to use
bitwise operators to implement bitwise-parallel addition (mod 3).

Here's how we want the addition to work when a new bit `x` is added to
one of the 2-bit counts within `twos` and `ones`:

  incoming bit  +  count (mod 3) =  new count (mod 3)

  x                twos ones        twos ones

  0                0    0           0    0
  0                0    1           0    1
  0                1    0           1    0
  1                0    0           0    1
  1                0    1           1    0
  1                1    0           0    0

To derive boolean formulas for the new values of `twos` and `ones`
when we count a new bit `x`, we can create Karnaugh maps:

  New value of `twos`     New value of `ones`

  x     twos ones         x     twos ones
        --------------          --------------
        00  01  11  10          00  01  11  10
  --------------------    --------------------
  0     0   0   -   1     0      0   1   -   0
  1     0   1   -   0     1      1   0   -   0

From these maps, we can drive the needed formulas:

  new twos = (~x & twos) | (x & ones)
  new ones = (~x & ones) | (x & ~twos & ~ones)

Once we've accumulated counts for all of the elements in the array
using the formulas above, we can determine which bits are set in the
singleton by finding the bit positions that have counts (mod 3) of
exactly 1. These correspond to the 2-bit registers in which the `ones`
bit is set and the `twos` bit is not. But, since in integers (mod 3),
a `ones` bit being set guarantees that the corresponding `twos` bit
cannot be set, the formula simplifies to just this:

  singleton = ones & ~twos = ones

And that logic gives us another solution that runs in O(N) time and
O(1) space! This solution has low constant factors, too. I've
implemented it below in `find_non_triplicate_element_2_optimized`.

"""

import itertools
import random

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Solution 1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def find_non_triplicate_element_1(xs):
    """Finds the one element in xs that does not occur three times."""
    lo, hi = 0, len(xs)
    # Loop until we've narrowed xs[lo:hi] to a single element.
    while lo < hi - 1:
        # Partition the array about a random pivot element.
        pivot_value = xs[lo + random.randrange(hi - lo)]
        dividing_index = partition(xs, pivot_value, lo, hi)
        # Narrow to the partition containing the singleton element.
        if (dividing_index - lo) % 3 == 1:
            hi = dividing_index
        else:
            lo = dividing_index
    return xs[lo]


def partition(xs, x, lo, hi):
    """Partitions xs[lo:hi] into elems <= x and > x; returns divider."""
    # We maintain three partitions as we shrink the region between lo and hi:
    #   - elements before lo are known to be <= x
    #   - elements in xs[lo:hi] are unclassified
    #   - elements after hi are known to be > x
    while lo < hi:
        while lo < hi and xs[lo] <= x:
            lo += 1
        while lo < hi and xs[lo] > x:
            xs[hi - 1], xs[lo] = xs[lo], xs[hi - 1]
            hi -= 1
    # The middle partition is now empty, so the remaining two
    # partitions must span the entire input array.
    return lo  # Index after first partition.


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Solution 2: slow version.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def find_non_triplicate_element_2(xs):
    """Finds the one integer >= 0 in xs that does not occur three times."""
    # This solution doesn't work when the array contains negative
    # integers. (We could make it work by converting negative integers
    # into their twos-complement representation for a suitably large
    # base and then converting back after the singleton is found.)
    assert all(0 <= x for x in xs)

    # Reconstruct the singleton integer bit by bit, starting with bit 0.
    bit_mask = 1  # Mask corresponding to bit 0.
    singleton_bits = 0  # We start with the singleton's bits all set to 0.

    # Continue testing bits until the mask is large enough to cover
    # the largest integer in the array.
    xs_max = max(xs)
    while bit_mask <= xs_max:
        # Construct a predicate for the current bit we're checking.
        def is_bit_set(x):
            return (x & bit_mask) != 0

        # If the bit is set in the singleton, set our copy of that bit.
        if is_true_for_singleton(is_bit_set, xs):
            singleton_bits |= bit_mask
        # Shift the mask to the next bit position.
        bit_mask <<= 1
    # The bits we've set are now exactly those that are set in the
    # singleton value; hence, we've found the singleton value itself!
    return singleton_bits


def is_true_for_singleton(P, xs):
    """Returns whether P is true for the singleton in array xs."""
    true_count_mod_3 = 0
    for x in xs:
        if P(x):
            true_count_mod_3 = (true_count_mod_3 + 1) % 3
    return true_count_mod_3 == 1


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Solution 2: fast version.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def find_non_triplicate_element_2_optimized(xs):
    """Finds the one integer >= 0 in xs that does not occur three times."""
    # This solution doesn't work when the array contains negative
    # integers. (We could make it work by converting negative integers
    # into their twos-complement representation for a suitably large
    # base and then converting back after the singleton is found.)
    assert all(0 <= x for x in xs)

    # Accumulate bitwise counts (mod 3) across the entire array of
    # n-bit integers, using `ones` and `twos` as n parallel 2-bit
    # accumulators where the count for bit i is given by
    #   count[bit i] = 2 * (bit i of twos) + (bit i of ones).
    ones = twos = 0
    for x in xs:
        # Accumulate x's bits into the running counts.
        twos, ones = ((~x & twos) | (x & ones), (~x & ones) | (x & ~twos & ~ones))

    # Only the bits having counts (mod 3) of 1 are set in the singleton.
    # Thus the singleton is the integer with precisely those bits set.
    return ones


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Tests.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_find_non_triplicate_int():
    for soln in (
        find_non_triplicate_element_1,
        find_non_triplicate_element_2,
        find_non_triplicate_element_2_optimized,
    ):
        print("\n>>> Checking {}".format(soln.__name__))
        _check_solution(soln)


def _check_solution(soln):
    # Start small and work toward larger problem instances.
    for n in range(1, 7):
        for seq in itertools.permutations(list(range(n))):
            # Make a random problem instance with a known solution.
            seq = list(seq)
            singleton = seq[0]  # The first value is the singleton.
            seq[1:] = seq[1:] * 3  # The others are the triplicates.
            random.shuffle(seq)
            print("ans = {}, seq = {}".format(singleton, seq))
            # The solver must identify the singleton element.
            assert soln(seq) == singleton
