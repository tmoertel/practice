#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: find the max of two numbers w/o comparisions, etc.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-11-27 (#248) and was classified as Hard.

  Reported source: Nvidia.

  Find the maximum of two numbers without using any if-else
  statements, branching, or direct comparisons.


* Solution

I'll solve this problem by simulating a comparison in terms of
arithmetic, logical, and indexing operations.

A comparison, in effect, is a subtraction followed by a sign test of
the resulting difference. Since subtraction is an arithmetic
operation, it's allowed by the problem statement. But we're not
allowed to branch based on the sign test. Therefore, I'll use array
indexing based on the most-significant bit of the difference, which in
twos-complement integers is 1 if the difference is negative.

That is, instead of:

  diff = y - x
  return y if diff > 0 else x

I'll write:

  diff = y - x
  return [y, x][msb_of(diff)]

In Python, negative numbers have an effective infinite number of bits,
so there's no actual most-significant bit. There's just some bit
position i after which all bit positions j > i have the value 1. So
I'll let the caller decide how many positions to allow in the integer
arguments to our `mymax` function, with 64 being the default, to
establish the maximal position i. Then I'll read position j = i + 1 as
the least possible j.

"""


def msb_of(x, int_bits):
    """Returns the msb of a twos-complement integer of `int_bits` bits."""
    x >>= int_bits  # Shift the bit beyond the msb into the 1s position.
    return x & 1


def mymax(x, y, int_bits=64):
    """Returns the max of two twos-complement integers of `int_bits` bits."""
    diff = y - x
    return [y, x][msb_of(diff, int_bits)]


# Test our solution using Python's `max` as a reference.
def test_max_without_comparisons():
    for x in range(-128, 127):
        for y in range(-128, 127):
            xymax = mymax(x, y, int_bits=8)
            assert xymax == max(x, y)
