#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find minimal moves to unlock a combination lock.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2020-01-31 (#313) and was classified as Hard:

  Reported source: Citrix.

  You are given a circular lock with three wheels, each of which
  display the numbers 0 through 9 in order. Each of these wheels
  rotate clockwise and counterclockwise.

  In addition, the lock has a certain number of "dead ends", meaning
  that if you turn the wheels to one of these combinations, the lock
  becomes stuck in that state and cannot be opened.

  Let us consider a "move" to be a rotation of a single wheel by one
  digit, in either direction. Given a lock initially set to 000, a
  target combination, and a list of dead ends, write a function that
  returns the minimum number of moves required to reach the target
  state, or None if this is impossible.

* Solution

It's natural to model the problem space as an undirected graph -- a
10x10x10 cube of vertices, with the vertex at coordinates (x, y, z)
representing the combination xyz, and with edges connecting adjacent
vertices along the x-, y-, and z-axes, and "wrap-around" edges between
0s and 9s. Every vertex is thus connected to six neighbors.

To deal with dead ends, we can just remove the corresponding vertices
from the graph.

With this representation, we can solve the problem by finding the
shortest path from 000 to the target combination. A simple breadth
first search will suffice. The length of the shortest path is the
answer we seek -- the minimum number of moves to reach the target
state.

If there are no dead ends, a much faster and easier solution is
available. We can just compute the Manhattan distance from 000 to the
target combination. Of course, since we can roll each digit from 9
over to 0, we need to compute a "toroidal" Manhattan distance.

But this problem says there will be dead ends, and I will assume that
in the worst case an adversary is choosing them. So I'll go with a
search to find the path. Using a breadth first search guarantees that
any path we find is of minimal length, but a BFS is pretty expensive
because it considers all paths of length N before considering any
paths of length N + 1. A directed search like A* offers the same
guarantee with lower cost. However, in this problem, there are only
10^3 = 1000 possible vertices to search, so I'll stick with a simple
BFS as "good enough."

"""

import collections
import itertools
import random


STARTING_COMBINATION = 000


# We'll use ints to represent combinations. For times when it's
# more convenient to use a sequence of digits, these conversion
# helpers will let us move between the two representations.

def int_to_3_digits(i):
    chars = f'{i:03d}'
    return [ord(c) - ord('0') for c in chars]

def digits_to_int(digits):
    place_value = 1
    total = 0
    for i in 2, 1, 0:
        total += digits[i] * place_value
        place_value *= 10
    return total


def neighbors(combination):
    """Yields all combinations one move from a combination."""
    digits = int_to_3_digits(combination)
    up = lambda digit: (digit + 1) % 10
    down = lambda digit: (digit - 1) % 10
    for i, digit in enumerate(digits):
        for new_digit in up(digit), down(digit):
            new_digits = digits.copy()
            new_digits[i] = new_digit
            yield digits_to_int(new_digits)


def minimal_combination_moves(target_combination, dead_end_combinations=None):
    """Returns min number of moves to reach the target from 000."""
    dead_end_combinations = set(dead_end_combinations or [])
    frontier = collections.deque()
    seen = set()
    def schedule(combination, distance):
        if combination not in seen and combination not in dead_end_combinations:
            seen.add(combination)
            frontier.append((combination, distance))
    schedule(STARTING_COMBINATION, 0)
    while frontier:
        combination, distance = frontier.popleft()
        if combination == target_combination:
            return distance
        for neighboring_combination in neighbors(combination):
            schedule(neighboring_combination, distance + 1)
    return None


# Tests.

from nose.tools import eq_, raises


def toroidal_manhattan_distance(a, b):
    """Returns the distance between points on a 10x10x10 torroidal lattice."""
    a = int_to_3_digits(a)
    b = int_to_3_digits(b)
    def digit_distance(from_digit, to_digit):
        least_digit = min(from_digit, to_digit)
        greatest_digit = max(from_digit, to_digit)
        return min(greatest_digit - least_digit,
                   10 + least_digit - greatest_digit)
    return sum(itertools.starmap(digit_distance, list(zip(a, b))))


def test_without_dead_spots_min_moves_should_equal_manhattan_distance():
    for combination in range(0, 1000):
        eq_(minimal_combination_moves(combination),
            toroidal_manhattan_distance(000, combination))


def test_when_the_start_is_a_dead_end_no_moves_suffice():
    for combination in range(0, 1000):
        eq_(minimal_combination_moves(combination, [000]), None)


def test_when_the_end_is_a_dead_end_no_moves_suffice():
    for combination in range(0, 1000):
        eq_(minimal_combination_moves(combination, [combination]), None)
