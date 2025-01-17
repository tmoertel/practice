# Suggested code may be subject to a license. Learn more: ~LicenseLog:2421117277.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:4087789386.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:1420993134.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:3504247023.
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Solve 8-puzzle game played on 3x3 grid.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2021-02-18 (#687) and was classified as Hard:

  An 8-puzzle is a game played on a 3 x 3 board of tiles, with the
  ninth tile missing. The remaining tiles are labeled 1 through 8 but
  shuffled randomly. Tiles may slide horizontally or vertically into
  an empty space, but may not be removed from the board.

  Design a class to represent the board, and find a series of steps to
  bring the board to the state [[1, 2, 3], [4, 5, 6], [7, 8, None]].


* Solution

First, let's size up this problem. We are given a 3x3 board of tiles
arranged into a permutation of the nine symbols 1 through 8 and None.
That means we have 9! = 362,880 possible board configurations. That
number is rather small by modern computing standards, suggesting that
search is a viable strategy for solving this problem.

Imagine an undirected graph with one vertex for each of the 9!
possible configurations and one edge between any two configurations
that can be reached by sliding a single tile. Since there are at most
4 tiles that can be slid into the board's single empty space,
regardless of the configuration, each node has at most 4 edges.

In this graph, a solution to the puzzle looks like a path from the
vertex representing the given starting configuration, which we'll call
the "start," to the vertex representing the desired final state, which
we'll call the "end." We can find such a path by searching the graph
from the start until we reach the end.

Using a breadth-first search (BFS) will guarantee that we find a
minimal sequence of moves to solve the puzzle. If we created a
suitable distance heuristic, we could even use a directed search such
as A* to reduce the cost of the search. For now, we'll just use a
simple BFS.


* Implementation

Now let's think about options for representing a game board. The
obvious thing would be to represent it as a 3x3 array of values drawn
from the set {1, 2, ..., 9, None}. That will work but is not a
particularly compact representation. Another issue is that one of the
most important things about a board is the position of its empty tile,
and this representation requires us to scan the tiles to find it.

So let's think about more compact, more useful representation. There
are only 9 positions on the board; let's number them 0 through 8. Each
can be in only one of 9 states, which is less than 4 bits of
information. Hence, one intriguing option is to represent the board as
9 x 4 bits = 36 bits. We could use another 4 bits to record the
position of the empty tile for convenient access. That gives us a
40-bit representation that easily fits into a 64-bit machine integer.

Board        Internal representation = 40-bit unsigned integer

a  b  c      i    h    g    f    e    d    c    b    a    None
d  e  f      ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
g  h  i      xxxx xxxx xxxx xxxx xxxx xxxx xxxx xxxx xxxx xxxx


Example:

Board        Internal representation

3  5  9      i    h    g    f    e    d    c    b    a    None
1  8  2      ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
4  6         0000 0110 0100 0010 1000 0001 1001 0101 0011 1000 binary
                0    6    4    2    8    1    9    5    3    8 decimal

With this representation of the board, it's straightforward to code up
the required BFS. I've done so below. Note that I never actually have
to create the graph. Rather, I search over it implicitly.

Although the problem statement asks for a class, I have opted for a
library of related functions that act on a board representation. This
approach makes for a more composable set of board primitives that
could be reused for other purposes.

"""

import collections


def matrix_to_board(matrix):
    """Returns the board representation for a 3x3 tile matrix."""
    board = 0
    for row, cells in enumerate(matrix):
        for col, tile in enumerate(cells):
            tile = tile or 0  # Convert None to 0.
            board = set_tile(board, row, col, tile)
    return board


def get_empty_position(board):
    """Gets (row, col) giving the position of the empty tile."""
    index = board & 0xF
    row = index // 3
    col = index % 3
    return row, col


def get_tile(board, row, col):
    """Gets the board tile at row and col (0 indexed)."""
    return (board >> (4 * (3 * row + col + 1))) & 0xF


def set_tile(board, row, col, tile):
    """Sets the board tile at row and col (0 indexed)."""
    shift = 4 * (3 * row + col + 1)
    mask = ~(0xF << shift)
    shifted_tile = tile << shift
    board &= mask
    board |= shifted_tile
    # If we set the empty tile, record its position.
    if not tile:
        board &= ~0xF
        board |= 3 * row + col
    return board


def neighbors(board):
    """Gets the boards we can reach by moving one tile on `board`."""
    row, col = get_empty_position(board)
    positions_adjacent_to_empty = (
        # Return neighbors in lexical order.
        (row - 1, col),
        (row, col - 1),
        (row, col + 1),
        (row + 1, col),
    )
    for nrow, ncol in positions_adjacent_to_empty:
        if not (0 <= nrow <= 2 and 0 <= ncol <= 2):
            continue
        tile_to_move = get_tile(board, nrow, ncol)
        new_board = set_tile(board, nrow, ncol, 0)
        new_board = set_tile(new_board, row, col, tile_to_move)
        yield new_board


def solve_eight_tile_puzzle(puzzle_matrix):
    """Returns a minimal solution for a given 3x3 8-tile puzzle matrix.

    The solution is given as a series of moves for the empty tile.
    When there are multiple solutions of minimal length, we return
    the one that is lexically least.

    """
    start_board = matrix_to_board(puzzle_matrix)
    path = search(start_board, END_BOARD)
    return path


def search(start_board, end_board):
    """Returns the lexically least minimal path from start to end."""
    # Prepare the ingredients we need for a breadth-first search.
    seen = {}
    frontier = collections.deque()

    def explore(board, parent_board=None):
        """Ensure that `board` is explored and its parent recorded."""
        if board not in seen:
            seen[board] = parent_board
            frontier.append(board)

    # Search from the start board to the end board (breadth first).
    explore(start_board)
    while frontier:
        board = frontier.popleft()
        if board == end_board:
            break
        for neighbor_board in neighbors(board):
            explore(neighbor_board, board)
    # We found the end board. Trace back the path to the start board.
    back_path = []
    board = end_board
    while board != start_board:
        back_path.append(get_empty_position(board))
        board = seen[board]
    # The solution is the reversed path back.
    return back_path[::-1]


# The desired end configuration of the board.
END_MATRIX = [[1, 2, 3], [4, 5, 6], [7, 8, None]]
END_BOARD = matrix_to_board(END_MATRIX)


# Tests.


# fmt: off
def test_solving_an_already_solved_puzzle_should_give_an_empty_path():
    assert solve_eight_tile_puzzle(END_MATRIX) == []

def test_solutions_for_one_move_puzzles_should_be_one_move():
    assert solve_eight_tile_puzzle([[1, 2, 3],
                                    [4, 5, 6],
                                    [7, 0, 8]]) == [(2, 2)]
    assert solve_eight_tile_puzzle([[1, 2, 3],
                                    [4, 5, 0],
                                    [7, 8, 6]]) == [(2, 2)]

def test_solutions_for_two_move_puzzles_should_be_two_moves():
    assert solve_eight_tile_puzzle([[1, 2, 3],
                                    [4, 5, 6],
                                    [0, 7, 8]]) == [(2, 1), (2, 2)]
    assert solve_eight_tile_puzzle([[1, 2, 3],
                                    [4, 0, 6],
                                    [7, 5, 8]]) == [(2, 1), (2, 2)]
    assert solve_eight_tile_puzzle([[1, 2, 0],
                                    [4, 5, 3],
                                    [7, 8, 6]]) == [(1, 2), (2, 2)]
    assert solve_eight_tile_puzzle([[1, 2, 3],
                                    [4, 0, 5],
                                    [7, 8, 6]]) == [(1, 2), (2, 2)]

def test_solutions_for_three_move_puzzles_should_be_three_moves():
    assert solve_eight_tile_puzzle([[1, 2, 3],
                                    [0, 5, 6],
                                    [4, 7, 8]]) == [(2, 0), (2, 1), (2, 2)]
    assert solve_eight_tile_puzzle([[1, 2, 3],
                                    [0, 4, 6],
                                    [7, 5, 8]]) == [(1, 1), (2, 1), (2, 2)]
    assert solve_eight_tile_puzzle([[1, 0, 2],
                                    [4, 5, 3],
                                    [7, 8, 6]]) == [(0, 2), (1, 2), (2, 2)]
    assert solve_eight_tile_puzzle([[1, 0, 3],
                                    [4, 2, 5],
                                    [7, 8, 6]]) == [(1, 1), (1, 2), (2, 2)]

def test_zero_or_none_can_be_used_to_represent_the_empty_tile():
    for E in 0, None:
        assert solve_eight_tile_puzzle([[1, 2, 3],
                                        [4, 5, 6],
                                        [7, E, 8]]) == [(2, 2)]
# fmt: on
