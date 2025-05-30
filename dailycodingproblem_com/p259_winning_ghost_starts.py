#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find the winning starts for a game of Ghost.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-12-08 (#259) and was classified as Hard.

  Reported source: Two Sigma.

  Ghost is a two-person word game where players alternate appending
  letters to a word. The first person who spells out a word, or
  creates a prefix for which there is no possible continuation,
  loses. Here is a sample game:

  Player 1: g
  Player 2: h
  Player 1: o
  Player 2: s
  Player 1: t [loses]

  Given a dictionary of words, determine the letters the first player
  should start with, such that with optimal play they cannot lose.

  For example, if the dictionary is ["cat", "calf", "dog", "bear"],
  the only winning start letter would be b.


* Solution

First, let's note that the problem statement contains an error. In the
example, it claims that the only winning start letter is b:

  Player 1: b
  Player 2: e
  Player 1: a
  Player 2: r [loses]

But c would also be a guaranteed win for Player 1:

  Player 1: c
  Player 2: a [player 2's only option]
  Player 1: l [player 1 can't choose t because it would lead to loss]
  Player 2: f [player 2 loses, therefore player 1 wins]

Now let's think about the problem. Let's visualize the example
dictionary as a prefix tree. A game of Ghost can be seen as a path
from the root of the tree (^) to a word end ($), with Player 1
choosing the nodes at odd depths, and Player 2 at even depths.

      1   2   3   4   5

  ^---b---e---a---r---$
    |-c---a---l---f---$
    |       `-t---$
    `-d---o---g---$

Player 1 goes first. Assume that Player 1 chooses a node x that
guarantees a win. This implies that x has no child y that Player 2 can
choose to prevent Player 1 from winning. Thus, ALL of x's children
must be guaranteed wins for Player 1. Now assume that Player 2 has
chosen node y. Since we know that Player 1 must win, we know that
least one of y's children must lead to a guaranteed win for Player 1
(and Player 1 will choose just such a child).

Let's formalize this logic by introducing some notation. Let W(x) be a
predicate that indicates whether Player 1 wins when x is chosen by
whomever is the current player. When it's Player 1's turn, we have

  W(x) = all(W(y) for y in children(x))  # If P1's turn.

When it's Player 2's turn, we have

  W(x) = any(W(y) for y in children(x))  # If P2's turn.

This is a recursive formula. To terminate the recursion, we need base
cases. Fortunately, we know that when a player reaches a word end ($),
that player wins because the previous player must have played the
final letter of a word and lost.

  W($) = True if P1's turn; False otherwise.

This recursive formula is all we need to solve the problem.

For a dictionary of N letters, we can build the prefix tree in O(N)
time and space, and we can process the tree to arrive at a solution in
O(N) time and space in the worst case.

"""


# We create a unique value, rather than the literal '$', to represent
# word ends. This lets us use '$' in dictionary words.
class WORD_END:
    def __repr__(self):
        return "$"


WORD_END = WORD_END()


def prefix_tree(words):
    """Creates a prefix tree from the given words."""
    root = {}
    for word in words:
        node = root
        for char in word:
            node = node.setdefault(char, {})
        node.setdefault(WORD_END, {})
    return root


# Solve the problem using a prefix tree of the dictionary words.


def winning_starts(words):
    """Returns the starting letters that guarantee Ghost wins for Player 1."""
    initial_choices = list(prefix_tree(words).items())
    return sorted(child[0] for child in initial_choices if is_win(child, 1))


def is_win(node, depth):
    """Returns true iff P1 wins when `node` is on the game path at `depth`."""
    is_p1_turn = bool(depth % 2)
    value, children = node
    if value is WORD_END:
        return is_p1_turn
    rule = all if is_p1_turn else any
    return rule(is_win(child, depth + 1) for child in list(children.items()))


# Tests.


def test_empty_dict_must_give_empty_winning_starts():
    soln = winning_starts([])
    assert soln == []


def test_dict_with_empty_word_must_give_word_end_as_sole_winning_start():
    soln = winning_starts([""])
    assert soln == [WORD_END]


def test_example_soln_must_be_correct():
    d = "cat calf dog bear".split()
    soln = winning_starts(d)
    assert soln == ["b", "c"]
