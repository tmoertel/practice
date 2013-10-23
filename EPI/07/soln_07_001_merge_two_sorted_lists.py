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
    if not xs and not ys:
        return None
    elif not xs:
        return ys
    elif not ys:
        return xs
    elif xs.head <= ys.head:
        xs.tail = merge(xs.tail, ys)
        return xs
    else:
        ys.tail = merge(xs, ys.tail)
        return ys


# testing apparatus

def test():
    from nose.tools import assert_equals as eq
    for m in xrange(5):
        xs = range(m)
        for n in xrange(5):
            ys = range(n)
            for xs_sub in powerset(xs):
                for ys_sub in powerset(ys):
                    spec = sorted(xs_sub + ys_sub)
                    result = merge(from_seq(xs_sub), from_seq(ys_sub))
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
