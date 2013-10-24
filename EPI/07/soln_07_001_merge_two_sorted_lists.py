#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-10-23

"""Solution to "Merge Two Sorted Lists", 7.1 in EPI.

Problem: Write a function to merge, in ascending order, two singly
linked lists containing numbers in ascending order.

Discussion.

The goal is to modify the nodes in the lists to create a new, merged
list, instead of creating a new list of new nodes.

"""

class Cons(object):
    """Cons cell for a singly linked list."""
    def __init__(self, head, tail=None):
        self.head = head
        self.tail = tail

def merge(xs, ys):
    """Merge nodes of two sorted singly linked lists."""
    anchor = prev = Cons(None)

    # consume elements until at least one list empties
    while xs and ys:
        if xs.head <= ys.head:
            prev.tail = xs
            xs, prev = xs.tail, xs
        else:
            prev.tail = ys
            ys, prev = ys.tail, ys

    # handle any partially remaining lists
    prev.tail = xs or ys

    return anchor.tail


# testing apparatus

def test():
    from nose.tools import assert_equals as eq
    for xs in powerset(range(7)):
        for ys in powerset(range(7)):
            spec = sorted(xs + ys)
            result = merge(from_seq(xs), from_seq(ys))
            eq(to_pylist(result), spec)

def powerset(xs):
    if not xs:
        yield []
    else:
        x, rest = xs[0], xs[1:]
        for ys in powerset(rest):
            yield [x] + ys
        for ys in powerset(rest):
            yield ys

def from_seq(xs):
    """Make a linked list from a Python sequence."""
    head = None
    for x in reversed(xs):
        head = Cons(x, head)
    return head

def to_pylist(xs):
    """Convert a linked list into a Python list (array)."""
    ys = []
    while xs:
        ys.append(xs.head)
        xs = xs.tail
    return ys
