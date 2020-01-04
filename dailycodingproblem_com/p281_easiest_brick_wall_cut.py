#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find the easiest place to cut a brick wall.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-12-30 (#281) and was classified as Medium:

  This problem was asked by LinkedIn.

  A wall consists of several rows of bricks of various integer lengths
  and uniform height. Your goal is to find a vertical line going from
  the top to the bottom of the wall that cuts through the fewest
  number of bricks. If the line goes through the edge between two
  bricks, this does not count as a cut.

  For example, suppose the input is as follows, where values in each
  row represent the lengths of bricks in that row:

  [[3, 5, 1, 1],
   [2, 3, 3, 2],
   [5, 5],
   [4, 4, 2],
   [1, 3, 3, 3],
   [1, 1, 6, 1, 1]]

  The best we can we do here is to draw a line after the eighth brick,
  which will only require cutting through the bricks in the third and
  fifth row.

  Given an input consisting of brick lengths for each row such as the
  one above, return the fewest number of bricks that must be cut to
  create a vertical line.


* Solution

First, it appears that there's a small error in the solution for the
example problem. I have put my suggested correction in brackets:

  "The best we can we do here is to draw a line [at 8 units from the
  left edge of the wall], ..."

Now, let's think about the problem. If we minimize the bricks cut by
our vertical line, we'll maximize the number of inter-brick edges that
the line traverses. So we can solve the problem by finding where the
most inter-brick edges line up. This we can do by building a map from
edge position to edge count, a task that will take O(n) time and space
for walls having n bricks. Then we just scan the map for the maximal
count and take the corresponding edge position, which we can do in
O(n) time and O(1) space. The problem statement asks for the number of
bricks that must be cut, and that's just the wall height in bricks
less the maximal count. Putting these three tasks together gives us a
complete solution taking O(n) time and space.

"""


import collections
import itertools


def minimal_vertical_cut_through_brick_wall(rows):
    """Finds a vertical cut that minimizes cut bricks in a brick wall.

    Returns (d, n) where d is the distance to cut from the left edge
    of the wall and n is the number of bricks that must be cut.

    """
    # Require that the wall not be empty.
    assert len(rows) > 0

    # Require that all bricks have sane widths.
    assert all(width > 0 for row in rows for width in row)

    # Require that all rows have the same total width > 0.
    row_widths = set(sum(row) for row in rows)
    assert len(row_widths) == 1
    for width in row_widths:
        assert width > 0

    # Count the edges at each distance from the left edge of the wall.
    edges = collections.Counter()
    for row in rows:
        distance = 0
        # Scan the inter-brick edges in the row, computing their
        # positions as the running total of brick widths. Note that
        # the final brick's width should not be included, as it
        # determines only the position of the wall's right edge, where
        # a cut has no effect.
        for i in range(len(row) - 1):
            distance += row[i]
            edges[distance] += 1

    # Handle the cases where there is a single column:
    if not edges:
        # We must cut all bricks, and we do so in the middle.
        return rows[0][0] / 2, len(rows)

    # Cut the wall at the least distance having a maximal number of edges.
    edge_count, negative_distance = max((edges[i], -i) for i in edges)
    wall_height = len(rows)
    return -negative_distance, wall_height - edge_count


# Tests.

from nose.tools import raises

@raises(AssertionError)
def test_degenerate_wall_with_no_rows_should_be_rejected():
    minimal_vertical_cut_through_brick_wall([])

@raises(AssertionError)
def test_degenerate_wall_with_zero_width_bricks_should_be_rejected():
    minimal_vertical_cut_through_brick_wall([[0]])

@raises(AssertionError)
def test_degenerate_wall_with_negative_width_bricks_should_be_rejected():
    minimal_vertical_cut_through_brick_wall([[-1]])

@raises(AssertionError)
def test_degenerate_wall_with_empty_rows_should_be_rejected():
    minimal_vertical_cut_through_brick_wall([[]])

@raises(AssertionError)
def test_degenerate_wall_with_unequal_row_widths_should_be_rejected():
    minimal_vertical_cut_through_brick_wall([[3], [4]])

def test_nondegenerate_walls_should_be_cut_where_fewest_bricks_are_broken():
    soln = minimal_vertical_cut_through_brick_wall

    # Solver should divide single-column walls in the middle.
    for wall_height in range(1, 5):
        for brick_width in range(1, 5):
            wall = [[brick_width] * 1] * wall_height
            assert soln(wall) == (brick_width / 2, wall_height)

    # Solver should take the first cut when there are multiple minimal cuts.
    for wall_height in range(1, 5):
        for bricks_per_row in range(3, 5):
            for brick_width in range(1, 3):
                wall = [[brick_width] * bricks_per_row] * wall_height
                assert soln(wall) == (brick_width, 0)

    # Solver should solve the example problem.
    example_problem = [[3, 5, 1, 1],
                       [2, 3, 3, 2],
                       [5, 5],
                       [4, 4, 2],
                       [1, 3, 3, 3],
                       [1, 1, 6, 1, 1]]
    assert soln(example_problem) == (8, 2)
