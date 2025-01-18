#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-10-23

"""Solution to "Merge Two Sorted Lists", 7.1 in EPI.

Problem: Write a function to merge, in ascending order, two singly
linked lists containing numbers in ascending order.

Discussion.

Note that the goal is to modify the input lists to create a new,
merged list, instead of creating a new list of new cells.  Also note
that, since the input lists are already sorted, we can simply compare
their heads to find the globally least value.  This we can then remove
and append to the output list by changing pointers.  If we repeat this
procedure until both input lists have been consumed, the output list
will contain all of the input elements in sorted order, and this is
exactly the result we seek.

Implementation notes.

Since Python doesn't let us use pointers directly, we can use Cons
cells as pointers.  For example, if P is such a "pointer", then

    P represents the address of the pointer, and
    P.tail represents the value of the pointer.

In the code below, there are two such pointers. The first, ``anchor``,
points to the start of the output list.  The second, ``prev``, points
to the final cell of the output list.  (This second pointer makes
appending to the output list a constant-time operation since we always
know which cell will be previous to the new node and can update its
tail directly.)

"""


class Cons(object):
    """Cons cell for a singly linked list."""

    __slots__ = "head tail".split()

    def __init__(self, head, tail=None):
        self.head = head
        self.tail = tail


def merge(xs, ys):
    """Merge nodes of two sorted singly linked lists."""

    # use a cons cell to anchor the merged list we'll build
    anchor = prev = Cons(None)

    # consume the least element and append it to the output list;
    # repeat until one (or both) of the input lists is empty
    while xs and ys:
        if xs.head <= ys.head:
            prev.tail = xs
            xs, prev = xs.tail, xs
        else:
            prev.tail = ys
            ys, prev = ys.tail, ys

    # handle any remaining input elements (if any)
    prev.tail = xs or ys

    # the merged result hangs from the anchor's tail
    return anchor.tail
