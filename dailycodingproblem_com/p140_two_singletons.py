#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: find the two singletons in an array of doubles.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-08-11 (#140) and was classified as Medium.

  Reported source: Facebook.

  In an array of integers in which two values occur once and every
  other value occurs twice, find the two integers that occur once.

  For example, given the array [1, 2, 3, 4, 5, 1, 3, 5], return 2
  and 4. (Order does not matter.)

  Follow-up: Can you do this in linear time and constant space?

* Solution

Since x XOR x equals zero for all integers x, if we take the "XOR sum"
of the input array, the resulting value must be the exclusive OR of
the two values that occur only once. Let x and y be those values.

Given z = x XOR y, how can we find x and y? We know that the set bits
in z will correspond to those bits that are set in either x or y but
not in both. So we can pick one of the set bits in z, say the least,
and partition the elements of the input array based on whether that
bit is set in them. This will give us two partitions: one containing x
and one containing y, and both containing some arbitrary number of
other elements, each replicated twice. We can then take the XOR sum of
each of these partitions to reveal x and y -- again, the twice-
replicated values will cancel out.

Computing an XOR sum requires O(n) time and O(1) space. Our solution
requires three XOR sums and a few additional cheap operations, for
an overall cost of O(n) time and O(1) space. It does not modify the
input array.

"""

from functools import reduce
import itertools
import operator
import random

def find_two_singletons(xs):
    """Returns the two values in `xs` that occur once.

    ASSUMES all other valures occur twice.
    """
    bits_in_only_one_singleton = selected_xor_sum(xs)
    partition_bit = lsb_mask(bits_in_only_one_singleton)
    singleton1 = selected_xor_sum(xs, lambda x: x & partition_bit)
    singleton2 = selected_xor_sum(xs, lambda x: not (x & partition_bit))
    return min(singleton1, singleton2), max(singleton1, singleton2)

def selected_xor_sum(xs, is_wanted=lambda _: True):
    """XORs the elems of `xs` for which `is_wanted` returns true."""
    return reduce(operator.__xor__, (x for x in xs if is_wanted(x)), 0)

def lsb_mask(x):
    """Returns the least significant bit of `x` that is set."""
    return x ^ (x & (x - 1))

def test():
    soln = find_two_singletons
    for n in range(2, 7):
        for seq in itertools.permutations(list(range(n))):
            # Make a random problem instance with a known solution.
            offset = random.randint(0, n)  # Allows for negative values.
            seq = [x - offset for x in seq]
            singletons = seq[:2]   # The first two values are the singletons.
            seq[2:] = seq[2:] * 2  # The others are the doubles.
            random.shuffle(seq)
            print('ans = {}, seq = {}'.format(singletons, seq))
            # The solver must identify the singleton elements.
            assert soln(seq) == tuple(sorted(singletons))
