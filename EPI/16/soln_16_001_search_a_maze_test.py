from soln_16_001_search_a_maze import find_maze_path


def test_find_maze_path():
    from random import randrange
    from math import factorial

    # Empty mazes have no valid paths.
    assert find_maze_path([], (0, 0), (0, 0)) is None
    assert find_maze_path([[]], (0, 0), (0, 0)) is None

    # One-cell mazes have only trivial solutions.
    assert find_maze_path([[False]], (0, 0), (0, 0)) is None
    assert find_maze_path([[True]], (0, 0), (0, 0)) == [(0, 0)]

    N = 6
    white_row = [True] * N
    black_row = [False] * N

    def randcell():
        return randrange(N), randrange(N)

    # Check fundamental properties of solutions for mazes having them.
    A = [white_row] * N  # All-white maze.
    for _ in range(factorial(N)):
        s = randcell()
        e = randcell()
        P = find_maze_path(A, s, e)
        assert P is not None
        # If P = find_maze_path(A, s, e) and P is not None, then the
        # following properties must hold:
        assert P[0] == s  # The path must start at s...
        assert P[-1] == e  # ... and end at e.
        all(A[i][j] for (i, j) in P)  # Path cells must be white...
        all(
            abs(i - i1) + abs(j - j1) == 1  # ... and adjacent
            for ((i, j), (i1, j1)) in zip(P, P[1:])
        )

    # Solution must be None for mazes without valid paths.
    B = [white_row, black_row, white_row]  # Top and bottom separated by black.
    for sj in range(N):
        s = (0, sj)  # Start in top row.
        for ej in range(N):
            e = (2, ej)  # Exit in bottom row.
            assert find_maze_path(B, s, e) is None
