#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find the longest Collatz sequence start.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2020-09-15 (#537) and was classified as Easy:

  Reported source: Apple.

  A Collatz sequence in mathematics can be defined as
  follows. Starting with any positive integer:

  if n is even, the next number in the sequence is n / 2
  if n is odd, the next number in the sequence is 3n + 1

  It is conjectured that every such sequence eventually reaches the
  number 1. Test this conjecture.

  Bonus: What input n <= 1000000 gives the longest sequence?



* Solution


"""

def collatz_search(max_seed, max_iterations=10000):
    """Returns a dict from each integer seed i to its Collatz sequence's length.

    Params:
      max_seed: The maximum seed i to guarantee is included in the dict.
      max_iterations: The maximum number of iterations to search for a seed's
        corresponding length before giving up.
    """
    collatz_sequence_lengths = {1: 1}
    for seed in range(1, max_seed + 1):
        path = []
        start = seed
        while len(path) <= max_iterations:
            if seed in collatz_sequence_lengths:
                break
            path.append(seed)
            if seed % 2 == 0:
                seed //= 2
            else:
                seed = 3 * seed + 1
        if len(path) > max_iterations:
            raise ValueError(f'Search for {start} exceeded {max_iterations}')
        length = collatz_sequence_lengths[seed]
        while path:
            seed = path.pop()
            length += 1
            collatz_sequence_lengths[seed] = length
    return collatz_sequence_lengths


def max_collatz_sequence_length(max_seed, max_iterations=10000):
    """Returns the least i <= max_seed having the longest Collatz sequence."""
    collatz_sequence_lengths = collatz_search(max_seed)
    return -max((length, -seed)
                for seed, length in collatz_sequence_lengths.items()
                if seed <= max_seed)[1]



# Tests.

from nose.tools import eq_

def test_simple_cases():
    eq_(collatz_search(1)[1], 1)
    eq_(collatz_search(2)[2], 2)
    eq_(collatz_search(3)[3], 8)

def test_collatz_sequence_length_for_2_to_the_n_should_be_n_plus_one():
    max_power = 15
    collatz_sequence_lengths = collatz_search(2**max_power)
    for n in range(max_power + 1):
        eq_(collatz_sequence_lengths[2**n], n + 1)

def test_max_collatz_sequence_with_seed_not_exceeding_one_million_is_X():
    eq_(max_collatz_sequence_length(1000000), 837799)
