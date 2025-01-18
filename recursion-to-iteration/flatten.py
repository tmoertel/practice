#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-11-07

"""Example of converting recursion into iteration: flatten a binary tree.
See http://blog.moertel.com/posts/2013-06-03-recursion-to-iteration-3.html.

"""

import collections

Node = collections.namedtuple("Node", "val left right")


# original recursive algorithm
def flatten(bst):
    # empty case
    if bst is None:
        return []
    # node case
    return flatten(bst.left) + [bst.val] + flatten(bst.right)


# final iterative version
def flatten(bst):
    left = []
    parents = []
    while True:
        while bst is not None:
            parents.append(bst)
            bst = bst.left
        if not parents:
            break
        bst = parents.pop()
        left.append(bst.val)
        bst = bst.right
    return left


# test code

# some sample trees having various node counts
tree0 = None  # empty tree
tree1 = Node(5, None, None)
tree2 = Node(7, tree1, None)
tree3 = Node(7, tree1, Node(9, None, None))
tree4 = Node(2, None, tree3)
tree5 = Node(2, Node(1, None, None), tree3)


def check_flattener(f):
    assert f(tree0) == []
    assert f(tree1) == [5]
    assert f(tree2) == [5, 7]
    assert f(tree3) == [5, 7, 9]
    assert f(tree4) == [2, 5, 7, 9]
    assert f(tree5) == [1, 2, 5, 7, 9]
    print("ok")


check_flattener(flatten)  # ok
