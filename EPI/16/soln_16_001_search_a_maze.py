#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-11-18

"""Solution to "Searching a Maze", problem 16.1 from EPI v. 1.3.1.

"Problem 16.1: Given a 2D array of black and white entries
representing a maze with designated entrance and exit points, find a
path from the entrance to the exit, if one exists."  Source: _Elements
of Programming Interviews_, v. 1.3.1.

Discussion.  The first problem is how to represent a maze.  The
problem statement says that we will be given a 2D array of black and
white cells.  Presumably we are also given the identifiers of a source
cell and an exit cell.  So we will represent a maze as the triple

    (A, s, e)

where A is an array of Boolean values, in which True represents white
cells and False black, and s and e are the indices into the array
giving the source and destination cells.

The array A can be seen as representing a graph in which each white
cell is connected to its white neighbors.  A path from source to exit
exists in the maze iff there is a path from the source to the exit in
the graph.  To solve the problem then, I'll interpret the array A as a
graph and use a breadth-first search from s, looking for e.  Using BFS
ensures that no path of length N + 1 is considered before all paths of
length N have been exhausted.  From this property it follows that, if
the exit is encountered during the search, the path to it (given by
the search predecessor relationship) is minimal.

"""

from collections import deque


def find_maze_path(A, s, e):
    """Find path from s to e in A, or None if no such path exists."""

    # handle empty and pathless mazes
    if not A or not A[s[0]] or not A[s[0]][s[1]]:
        return None

    # define a helper to return the white neighbors of a cell
    def neighbors(xxx_todo_changeme):
        (i, j) = xxx_todo_changeme
        for i1, j1 in (i - 1, j), (i, j - 1), (i, j + 1), (i + 1, j):
            if 0 <= i1 < len(A) and 0 <= j1 < len(A[0]) and A[i1][j1]:
                yield i1, j1

    # use breadth-first search from s to find a shortest path to e
    seen = set([s])
    preds = {}
    frontier = deque([s])
    while frontier:
        v = frontier.popleft()  # change to pop for DFS instead of BFS
        if v == e:
            break  # found solution
        for u in neighbors(v):
            if u not in seen:
                seen.add(u)
                frontier.append(u)
                preds[u] = v
    else:
        return None  # can't reach exit by any path from start

    # trace predecessors from exit back to start
    backpath = []
    while v:
        backpath.append(v)
        v = preds.get(v)

    # the reverse gives our desired start-to-exit path
    return list(reversed(backpath))
