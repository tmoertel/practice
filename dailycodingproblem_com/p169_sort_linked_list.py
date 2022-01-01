#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: sort a linked list in O(1) space.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-09-09 (#169) and was classified as Medium.

  Reported source: Google.

  Sort a linked list in O(n log n) time and constant space.

  For example, the linked list

    7 -> -3 -> 0 -> 99

  sorts to

    -3 -> 0 -> 7 -> 99.

* Solution

We use the classic Lisp representation of lists: singly linked "cons"
cells.

Since the lists don't support efficient random access, we choose to
sort them using a mergesort. Mergesorts need only sequential scans
and were often used for disk-based sorting in the days before
solid-state drives.

Our implementation does O(lg n) passes in which we merge sublists
whose length doubles each pass. Each pass takes O(n) time.

Example:

Input list:     5 -> 3 -> 4 -> 1 -> 2

Iteration 1:    [5] merge [3]
                then
                [4] merge [1]
                then
                [2] merge []

             =  3 -> 5 -> 1 -> 4 -> 2

Iteration 2:    [3 -> 5] merge [1 -> 4]
                then
                [2] merge []

             =  1 -> 3 -> 4 -> 5 -> 2

Iteration 3:    [1 -> 3 -> 4 -> 5] merge [2]

             =  1 -> 2 -> 3 -> 4 -> 5   (Final result).

This solution runs in O(1) space and O(n lg n) time.

"""

# We start with a classic linked-list representation based on cons
# cells, as in Lisp. In this representation, a list is either empty
# (represented by None) or given by a cell having a value and a
# tail. The tail points to another linked list representing the
# remaining values.

class Cons(object):
    """A cell in a singly linked list."""
    def __init__(self, value, tail=None):
        self.value = value
        self.tail = tail

# The sorting logic.

def merge(xs, ys):
    """Merges two sorted linked lists into a sorted linked list.

    Returns the first and last cells of the resulting linked list.
    """
    cell = first_cell = last_cell = None
    while xs or ys:
        # Select the next cell in the sorted sequence.
        if not ys or (xs and xs.value < ys.value):
            cell = xs
            xs = xs.tail
        else:
            cell = ys
            ys = ys.tail
        # Append the cell to the sorted list we're building.
        if first_cell is None:
            first_cell = cell
        if last_cell:
            last_cell.tail = cell
        last_cell = cell
    # Terminate the sorted list (unless it's empty).
    if cell:
        cell.tail = None
    return first_cell, last_cell

def take(llist, n):
    """Take n cells from a linked list. Returns (taken, remaining) lists."""
    taken_cells = llist
    while n and llist:
        n -= 1
        next_llist = llist.tail
        if n == 0:
            llist.tail = None
        llist = next_llist
    return taken_cells, llist

def llist_len(llist):
    """Returns the length of a linked list."""
    n = 0
    while llist:
        n += 1
        llist = llist.tail
    return n

def sort_linked_list(llist):
    """Sorts a linked list, rewriting links as needed."""
    # Lists less than length 2 are already sorted.
    n = llist_len(llist)
    if n < 2:
        return llist
    # Mergesort. We iterate for i = 1, 2, ..., ceil(lg(n)). For each
    # iteration, we scan the list into paired sublists of size 2^(i-1)
    # and merge the pairs, appending them to the list that will be
    # used in the next iteration.
    merge_len = 1  # Start by merging sublists of length 1.
    while merge_len < n:
        next_unmerged_cell = llist
        last_cell = llist = None
        while next_unmerged_cell:
            xs, next_unmerged_cell = take(next_unmerged_cell, merge_len)
            ys, next_unmerged_cell = take(next_unmerged_cell, merge_len)
            merged_first_cell, merged_last_cell = merge(xs, ys)
            if llist is None:
                llist = merged_first_cell
            else:
                last_cell.tail = merged_first_cell
            last_cell = merged_last_cell
        merge_len *= 2  # The merged sublists are twice as long.
    return llist


# Tests.

# Some helper functions to convert between linked and Python lists.
# We use them only for testing.

import math
import random

def to_linked_list(sequence):
    """Converts a Python list into a linked list."""
    cells = map(Cons, sequence)
    cells.append(None)
    for i in range(len(cells) - 1):
        cells[i].tail = cells[i + 1]
    return cells[0]

def from_linked_list(llist):
    """Converts a linked list into a Python list."""
    sequence = []
    while llist:
        sequence.append(llist.value)
        llist = llist.tail
    return sequence

# Test our solution using Python's `sorted` as an oracle. We are
# testing this property: For all sequences of ints `xs`, the solution
# must agree with `sorted`.
def test():
    # Start with small cases and work toward larger.
    for size in range(20):
        # For each size, generate a good number of random sequences `xs`.
        for _ in range(min(120, math.factorial(size))):
            xs = [random.randint(-size, size) for _ in range(size)]
            expected = sorted(xs)
            print '### trying {}'.format(xs)
            actual = from_linked_list(sort_linked_list(to_linked_list(xs)))
            assert actual == expected
