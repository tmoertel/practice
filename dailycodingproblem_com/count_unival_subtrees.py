#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Solve interview problem: count "univalued" subtrees in a binary tree.

This problem comes from Daily Coding Problem on 2019-04-01 and was
classified as Easy difficulty:

This problem was asked by Google.

  A unival tree (which stands for "universal value") is a tree where
  all nodes under it have the same value.

  Given the root to a binary tree, count the number of unival subtrees.

  For example, the following tree has 5 unival subtrees:

     0
    / \
   1   0
      / \
     1   0
    / \
   1   1

"""

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Solve the problem using divide-and-conquer recursion.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def count_unival_subtrees(tree):
    def process(tree):
        # Base case: empty tree.
        if tree is None:
            return False, None, 0
        # Base case: singleton tree.
        if tree.left is None and tree.right is None:
            return True, tree.val, 1
        # General case. We divide and conquer using recursion.
        is_unival_l, val_l, count_l = process(tree.left)
        is_unival_r, val_r, count_r = process(tree.right)
        if is_unival_r and is_unival_r and val_l == val_r == tree.val:
            return True, tree.val, count_l + count_r + 1
        return False, None, count_l + count_r
    return process(tree)[2]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fun exploration:
#
# Solve the problem using divide-and-conquer recursion in which the
# recursion has been factored out using functional-programming
# methods.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# These two functions are the fundamental building blocks of recursion.

def tree_fmap(f, tree):
    """Maps a function f over a tree."""
    if tree is None:
        return None
    return Node(tree.val, f(tree.left), f(tree.right))

def tree_fold(algebra, tree):
    """Reduces a tree to a value using a tree-term algebra."""
    def tree_fold_using_algebra(tree):
        return algebra(tree_fmap(tree_fold_using_algebra, tree))
    return tree_fold_using_algebra(tree)

# This example shows how to use them to count the nodes of a tree.

def count_nodes_algebra(tree):
    if tree is None:
        return 0
    return 1 + tree.left + tree.right

def count_nodes(tree):
    return tree_fold(count_nodes_algebra, tree)

# Now we solve the actual problem.

def count_unival_subtrees_algebra(tree):
    """Reduces a tree term to a value indicating its unival status.
    
    None, None, 0  = The tree is empty.
    True, v, c     = The tree is unival with value v and count of c.
    False, None, c = The tree is not unival but has a count of c.

    """
    # Base case: empty tree.
    if tree is None:
        return None, None, 0

    # General case.
    # Extract unival statuses of the subtrees.
    is_unival_l, val_l, count_l = tree.left
    is_unival_r, val_r, count_r = tree.right
    # If the left and/or right subtrees were empty, we consider them
    # to be unival with a value guaranteed to match the root's value.
    if is_unival_l is None:
        is_unival_l, val_l = True, tree.val
    if is_unival_r is None:
        is_unival_r, val_r = True, tree.val
    # Incorporate the root into the final unival status.
    if is_unival_l and is_unival_r and val_l == val_r == tree.val:
        return True, tree.val, count_l + count_r + 1
    return False, None, count_l + count_r

def count_unival_subtrees_functional_style(tree):
    fold_result = tree_fold(count_unival_subtrees_algebra, tree)
    return fold_result[2]


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Tests.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test():
    assert count_nodes(None) == 0
    assert count_nodes(Node(1)) == 1
    for soln in count_unival_subtrees, count_unival_subtrees_functional_style:
        print soln.__name__
        assert soln(None) == 0
        assert soln(Node('foo')) == 1
        tree = Node(0, Node(1), Node(0, Node(1, Node(1), Node(1)), Node(0)))
        assert soln(tree) == 5
