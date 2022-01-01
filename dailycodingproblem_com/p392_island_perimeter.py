#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find the perimeter of an island on a grid.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2020-04-19 (#392) and was classified as Hard:

  Reported source: Google.

  You are given a 2D matrix of 1s and 0s where 1 represents land and 0
  represents water.

  Grid cells are connected horizontally or vertically (not
  diagonally). The grid is completely surrounded by water, and there
  is exactly one island (i.e., one or more connected land cells).

  An island is a group is cells connected horizontally or vertically,
  but not diagonally. There is guaranteed to be exactly one island in
  this grid, and the island doesn't have water inside that isn't
  connected to the water around the island. Each cell has a side
  length of 1.

  Determine the perimeter of this island.

  For example, given the following matrix:

  [[0, 1, 1, 0],
   [1, 1, 1, 0],
   [0, 1, 1, 0],
   [0, 0, 1, 0]]

  Return 14.


* Solution

To help think about this problem, imagine that we are going to build a
perimeter wall around the island. This wall will protect the island
from the surrounding water. How many wall segments will we need?

The problem statement tells us that all water inside the island is
connected to the surrounding water. Thus we will need need to build
one wall segment between every land cell and every water cell. (If the
island had any interior lakes, we would need to identify them and not
build wall segments around them.)

With this in mind, the solution becomes straightforward: For each land
cell on the grid, count the number of neighboring water cells. We need
to be a little careful with the cells on the grid's border since the
grid itself is surrounded by water. Then report the sum of the counts
-- the total number of wall segments -- as the perimeter's length.

"""

import collections
import itertools
import random


def perimeter(grid):
    """Returns the perimeter of the islands in a 4-connected grid.

    REQUIRES that islands do not have interior lakes.
    """
    # Get the grid's size and verify that it is rectangular.
    row_count = len(grid)
    if row_count == 0:
        return 0
    col_count = len(grid[0])
    assert(all(len(row) == col_count for row in grid))
    if col_count == 0:
        return 0

    # Helper: Yields the values of a grid cell's 4-connected neighbors.
    def neighbor_values(row, col):
        for row_offset, col_offset in (0, 1), (-1, 0), (0, -1), (1, 0):
            row1 = row + row_offset
            col1 = col + col_offset
            if 0 <= row1 < row_count and 0 <= col1 < col_count:
                yield grid[row1][col1]
            else:
                yield 0  # The grid is surrounded by water.

    # Compute the perimeter.
    perimeter = 0
    for row, col in itertools.product(range(row_count), range(col_count)):
        if grid[row][col]:
            perimeter += 4 - sum(neighbor_values(row, col))
    return perimeter


# Tests.

from nose.tools import eq_, raises

def test_zero_size_sea_should_have_zero_perimeter():
    eq_(perimeter([]), 0)
    eq_(perimeter([[]]), 0)

def test_zero_size_island_should_have_zero_perimeter():
    for n in range (1, 5):
        empty_grid = [[0] * n] * n
        eq_(perimeter(empty_grid), 0)

def test_single_cell_island_should_have_4_perimeter():
    n = 5
    for row_count, col_count in itertools.product(range(1, n), range(1, n)):
        for row, col in itertools.product(range(row_count), range(col_count)):
            grid = [[0] * col_count for _ in range(row_count)]
            grid[row][col] = 1
            eq_(perimeter(grid), 4)

def test_soln_for_example_problem_should_match_given_soln():
    grid = [[0, 1, 1, 0],
            [1, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0]]
    eq_(perimeter(grid), 14)
