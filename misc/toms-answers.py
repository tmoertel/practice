#!/usr/bin/env python

import itertools
import operator
from functools import reduce


def find_odd_occurring_int(xs):
    """Return integer that occurs an odd number of times."""
    return reduce(operator.xor, xs)

def find_even_occurring_int(xs):
    """Return elem that occurs and even number of times."""
    counts = dict()
    for x in xs:
        counts.setdefault(x, 0)
        counts[x] += 1
    for x, count in counts.items():
        if count % 2 == 0:
            return x



### Generate all permutations of a string

def selections(xs):
    """Generate all the ways of selecting an element from a list."""
    for i, x in enumerate(xs):
        yield (x, xs[:i] + xs[i + 1:])

def permutations(xs):
    """Generate the permutations of a list or string."""
    if not xs:
        yield []
    else:
        for x, xs in selections(xs):
            for ys in permutations(xs):
                yield [x] + ys


### Given a string, check that ()s, []s, and {}s are balanced.
### Assume the string contains no characters other than brackets.

closing_brackets = {'(': ')', '{': '}', '[': ']'}

def is_balanced(xs):
    stack = []
    for x in xs:
        closer = closing_brackets.get(x)
        if closer:
            stack.append(closer)
        elif stack == [] or x != stack.pop():
            return False
    return stack == []


### Emit the levels of a binary tree, top down, one line per level.

def bt_levels_top_down(tree):
    levels = itertools.groupby(bfs_w_depth(tree), operator.itemgetter(0))
    return [list(map(operator.itemgetter(1), xs)) for _, xs in levels]

def bt_levels_bottom_up(tree):
    return list(reversed(bt_levels_top_down(tree)))

def bfs_w_depth(tree):
    """Search a binary tree breadth first and return depth-annotated values."""
    visited = []
    frontier = [(0, tree)]
    while frontier:
        depth, tree = frontier.pop(0)
        if tree is not None:
            visited.append((depth, tree[0]))
            frontier.append((depth + 1, tree[1]))
            frontier.append((depth + 1, tree[2]))
    return visited


t0 = None
t3 = (2, (1, None, None), (3, None, None))
t7 = (0, t3, t3)




### Given an array [a1, a2, ..., aN, b1, b2, ..., bN, c1, c2, ..., cN]
### convert it to [a1, b1, c1, a2, b2, c2, ..., aN, bN, cN] in-place
### using constant extra space

def convert_array(xs):
    n = len(xs) / 3
    def map_index(i):
        return n * (i % 3) + i / 3
    for i in range(len(xs)):
        j = map_index(i)
        while j < i:
            j = map_index(j)
        xs[i], xs[j] = xs[j], xs[i]
    return xs
