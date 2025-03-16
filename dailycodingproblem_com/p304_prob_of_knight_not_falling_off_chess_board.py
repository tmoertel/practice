#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find the probability that a knight stays on a chess board.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2020-01-22 (#281) and was classified as Hard:

  Reported source: Two Sigma.

  A knight is placed on a given square on an 8 x 8 chessboard. It is
  then moved randomly several times, where each move is a standard
  knight move. If the knight jumps off the board at any point,
  however, it is not allowed to jump back on.

  After k moves, what is the probability that the knight remains on
  the board?

* Solution 1: memoized recursion

Let's introduce the notation K(p, n) to represent the probability that
a knight, starting at position p on a standard, 8x8 chess board, can
make n random moves without falling off of the board.

For generality, let's assume that positions p are given in the form
(r, c) for integers r and c, and that the standard chess board has
been positioned on the 2-d integer lattice with its upper-left corner
at position (1, 1) and its lower-right corner at (8, 8). Then we can
define a predicate to determine whether any position is on the board:

  def on_board(p):
    r, c = p
    return 1 <= r <= 8 and 1 <= c <= 8

With these definitions in place, we can start to define our function
K. Let's start with the base cases.

We know from common sense that if the knight is initially placed off
the board, it will fall immediately, with no chance to remain on the
board.

  def K(p, n):
    if not on_board(p):
      return 0.0

Likewise, if n = 0, the probability that the knight will remain on the
board is the same as the probability that's it's already on the board.
Since we've already verified that the knight is on the board, that
probability must be 1:

    if n == 0:
      return 1.0

Now, what if the knight is on the board at position p and it has n > 0
moves to go? In that case, we can appeal to the law of total
probability. It says that the probability we seek is the probability
of the knight making a particular move times the corresponding
probability that the knight remains on the board given that it made
that move:

    return sum(K(p1, n - 1) for p1 in moves(p)) / 8.0

where moves(p) enumerates the eight possible moves from position p:

  def moves(p):
    r, c = p
    for rsign in -1, 1:
      for csign in -1, 1:
        for dr, dc = (1, 2), (2, 1):
          yield r + rsign * dr, c + csign * dr

And we now have a recursive solution to the problem!

One thing to note is that unless we're careful, we'll end up computing
K(p, n) repeatedely for many p and n. Consider K((1, 1), 3). A knight
at (1, 1) can reach two positions on the board: (3, 2) and (2, 3). And
from both of these positions the knight can return to (1, 1). Thus
when considering the knight's second jump, we'll end up computing
K((1, 1), 1) twice.

To avoid recomputing K(p, n), we can cache our K(p, n) result for each
(p, n) to avoid ever having to compute it again. (This is a standard
programming technique called memoization.)

** Performance

This solution runs in O(n) time and space,

TODO(tgm): Exploit symmetries to reduce problem size. Linear algebra.

"""

import functools


def memoize(f):
    """Makes a memoized version of f that returns cached results."""
    cache = {}

    @functools.wraps(f)
    def g(*args):
        ret = cache.get(args, cache)
        if ret is cache:
            ret = cache[args] = f(*args)
        return ret

    return g


def on_board(p):
    """Returns true iff p is on the chess board."""
    r, c = p
    return 1 <= r <= 8 and 1 <= c <= 8


@memoize
def prob_knight_stays_on_board(p, n):
    """Gets the prob that a knight at p remains on the board after n moves."""
    if not on_board(p):
        return 0.0
    if n == 0:
        return 1.0
    return sum(prob_knight_stays_on_board(p1, n - 1) for p1 in moves(p)) / 8.0


K = prob_knight_stays_on_board


def moves(p):
    """Yields the moves a knight can make from p."""
    r, c = p
    for rsign in -1, 1:
        for csign in -1, 1:
            for dr, dc in (1, 2), (2, 1):
                yield r + rsign * dr, c + csign * dr


# Tests.


# When a knight starts on the board and makes no moves, it is
# guaranteed to end on the board.
def test_knight_on_board_making_no_moves_must_stay_on_board():
    for r in range(1, 9):
        for c in range(1, 9):
            p = r, c
            assert K(p, 0) == 1.0


# When a knight starts off the board, it never ends on the board.
def test_knight_off_board_must_stay_off_board():
    for p in (0, 0), (1, 0), (0, 1), (9, 9), (-3, 2):
        for n in range(8):
            assert K(p, n) == 0.0


# When a knight starts in the middle of the board and makes only one
# move, it always ends on the board.
def test_knight_in_middle_making_one_move_must_stay_on_board():
    for p in (3, 3), (4, 4), (3, 4), (4, 3), (5, 3), (4, 5), (6, 6):
        assert K(p, 1) == 1.0


# When a knight starts on a corner of the board and makes a single move,
# that move will take it off the board 3/4 of the time.
def test_knight_on_corner_making_one_jump_stays_on_board_one_quarter_of_the_time():
    for r in 1, 8:
        for c in 1, 8:
            p = r, c
            assert K(p, 1) == 0.25
