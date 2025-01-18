#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-06-04

"""Solution to "Crop Triangles" Code Jam problem
https://code.google.com/codejam/contest/32017/dashboard

The key insight for this problem is that for any three distinct trees
at (x1, y1), (x2, y2), and (x3, y3) the center of the triangle formed
by those trees will be at a grid point whenever the x coordinates sum
to a multiple of 3 and the y coordinates sum to a multiple of 3, that
is, when

    (x1 + x2 + x3) % 3 == 0 and (y1 + y2 + y3) % 3 == 0.

Since we only care about congruence to 0 (mod 3), we need not store
the entire grid of trees but rather a 3x3 grid of buckets into which
we will insert trees based on their coordinates (mod 3).

Then, to compute the count of triangles satisfying the test, we
examine all combinations of three buckets (with possible repetition)
having coordinates satisfying the test.  For each combination, we
compute the number of triangles that can be created by drawing three
distinct trees, one from each bucket.  Without an ordering condition
on the trees, each triangle gets counted 3! = 6 times, so we divide
by 6 to get the final count.


"""

import fileinput
import itertools


def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print("Case #%r: %r" % (i, s))


def solve(problem):
    n, A, B, C, D, x0, y0, M = problem
    tree_counts_on_mod3_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    x, y = x0, y0
    for _ in range(n):
        tree_counts_on_mod3_grid[x % 3][y % 3] += 1
        x = (A * x + B) % M
        y = (C * y + D) % M
    count = 0
    for x1, x2, x3, y1, y2, y3 in itertools.product(list(range(3)), repeat=6):
        if (x1 + x2 + x3) % 3 == 0 and (y1 + y2 + y3) % 3 == 0:
            c1 = tree_counts_on_mod3_grid[x1][y1]
            c2 = tree_counts_on_mod3_grid[x2][y2]
            c3 = tree_counts_on_mod3_grid[x3][y3]
            if (x1, y1) == (x2, y2):
                c2 = max(0, c2 - 1)
            if (x1, y1) == (x3, y3):
                c3 = max(0, c3 - 1)
            if (x2, y2) == (x3, y3):
                c3 = max(0, c3 - 1)
            count += c1 * c2 * c3
    return count / 6


def read_problems(lines):
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)


def read_problem(lines):
    n, A, B, C, D, x0, y0, M = read_ints(lines)
    return n, A, B, C, D, x0, y0, M


def read_ints(lines):
    return [int(s) for s in lines.next().split()]


if __name__ == "__main__":
    main()
