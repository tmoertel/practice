# Suggested code may be subject to a license. Learn more: ~LicenseLog:1317266528.
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find the depth of a serialized binary tree.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2020-08-30 (#520) and was classified as Hard:

  Reported source: LinkedIn.

  You are given a binary tree in a peculiar string representation. Each node
  is written in the form (lr), where l corresponds to the left child and r
  corresponds to the right child.

  If either l or r is null, it will be represented as a zero.
  Otherwise, it will be represented by a new (lr) pair.

  Here are a few examples:

  A root node with no children: (00)
  A root node with two children: ((00)(00))
  An unbalanced tree with three consecutive left children: ((((00)0)0)0)

  Given this representation, determine the depth of the tree.


* Solution

Although the problem is classified as "hard," it has a simple, optimal
solution that occurred to me straight away. Think of a tree's string as
specifying a series of numbers, where '(' is +1, '0' is 0, and ')' is -1.
Then scan the numbers left to right, computing the running total along the
way. This is equivalent to performing a depth first search on the tree and
keeping track of the depth at each point. The solution, then, is the maximum
value encountered.

Proof: We'll now prove that the solution is correct by induction on the
depth of the tree that underlies the string.

Case: Tree of depth 0 (empty tree). If the tree is empty, its string form is
"0", and our algorithm will convert it into a series of numbers [0]. The
running totals of this series are also [0]. The maximum of the running
totals is 0. This maximum, as expected, is the depth of an empty tree.

Case: Tree of depth n > 0. We will assume that the algorithm works for
depths less than n as our induction hypothesis, and prove that it works for
depths of n.

Since the tree isn't empty, its string form must be "(lr)", where l and r
are the string forms of the tree's left and right subtrees. Our algorithm
will convert this string into a series of numbers [1, ln..., rn..., -1],
where ln... represents the numbers for l, and rn... for r. Next, our
algorithm will compute the running totals of this series. The totals must be
[1, 1 + (running totals of ln...), 1 + (running totals of rn...), 0].  (This
follows from the fact that the string form of a tree has an equal number of
opening and closing parentheses, and thus its numeric series has an equal
number of opening +1 values and closing -1 values.) By our induction
hypothesis, we know that our algorithm, if run on l alone and then r alone,
would produce the correct depths d_l for l and d_r for r. Therefore, d_l and
d_r must occur as maxima in the running totals of ln... and rn...,
respectively. But in the running totals for our entire tree, these depths
will be replaced with 1 + d_l and 1 + d_r since they follow the +1 that
results from the root node's opening parenthesis. When our algorithm takes
the maximum of these totals as its final step, it will return 1 + max(d_l,
d_r).  Since d_l and d_r are the depths of the subtrees of a tree of depth
n, the largest of them must be n - 1. Therefore, 1 + max(d_l, d_r)
simplifies to 1 + (n - 1), which is just n, the depth of the original tree,
as we want. QED

"""

import itertools

VALUE_MAP = {"(": 1, "0": 0, ")": -1}


def value(c):
    """Maps a serialized-tree char to its corresponding numeric value."""
    return VALUE_MAP[c]


def serialized_tree_depth(serialized_tree):
    """Finds the depth of a serialized binary tree."""
    return max(itertools.accumulate(value(c) for c in serialized_tree))


# Tests.


def test_simple_cases():
    S = serialized_tree_depth
    assert S("0") == 0
    assert S("(00)") == 1
    assert S("(0(00))") == 2
    assert S("((00)0)") == 2


def test_exhaustively_up_to_depth_n():
    n = 5
    for depth in range(n):
        for serialized_tree in serialized_trees(depth):
            assert serialized_tree_depth(serialized_tree) == depth


def serialized_trees(depth):
    """Exhaustively yield all serialized trees of a given depth."""
    if not depth:
        yield "0"
    depth_pairs = itertools.chain(
        itertools.product([depth - 1], list(range(depth))),
        itertools.product(list(range(depth)), [depth - 1]),
    )
    for left_depth, right_depth in depth_pairs:
        for serialized_left_subtree in serialized_trees(left_depth):
            for serialized_right_subtree in serialized_trees(right_depth):
                yield f"({serialized_left_subtree}{serialized_right_subtree})"
