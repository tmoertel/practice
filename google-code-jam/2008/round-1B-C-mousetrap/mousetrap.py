#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-06-10

"""Solution to "Mousetrap" Code Jam problem
https://code.google.com/codejam/contest/32017/dashboard#s=p2&a=0

"""

from array import array
import collections
import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print('Case #%r: %s' % (i, s))

def solve(problem):
    K, n, ds = problem
    tree = mktree(K)
    for card, index in enumerate(loc_sequence(K), 1):
        assign_card(tree, index, card)
    soln = ' '.join(str(get_card(tree, K, index)) for index in ds)
    return soln

def loc_sequence(k):
    card = 0
    pos = 0
    while k:
        pos = (pos + card) % k
        yield pos + 1
        if pos == k - 1:
            pos = 0
        k -= 1
        card += 1

Tree = collections.namedtuple('Tree', 'left_count_heap index_heap val_heap')

def mktree(size):
    depth = 1
    while 2**depth - 1 < size:
        depth += 1
    zeroes = [0] * (2 ** depth + 1)
    left_counts = array('L', zeroes)
    indices = array('L', zeroes)
    def init(i, size, starting_value):
        if size == 0:
            return
        mid = size // 2
        init(2 * i, mid, starting_value)
        init(2 * i + 1, size - mid - 1, starting_value + mid + 1)
        left_counts[i] = mid + 1
        indices[i] = starting_value + mid
    init(1, size, 1)
    return Tree(left_counts, indices, array('L', zeroes))

def assign_card(tree, index, card):
    counts = tree.left_count_heap
    values = tree.val_heap
    i = 1  # start at root
    while True:
        c = counts[i]
        if c < index:
            (i, index) = (2 * i + 1, index - c)
        elif c == index and values[i] == 0:
            counts[i] -= 1
            values[i] = card
            break
        else:
            counts[i] -= 1
            i = 2 * i

def get_card(tree, size, index):
    i = 1  # start at root
    while True:
        mid = size // 2
        if index <= mid:
            (i, size) = (2 * i, mid)
        elif index == mid + 1:
            return tree.val_heap[i]
        else:
            (i, size, index) = (2 * i + 1, size - mid - 1, index - mid - 1)

def read_problems(lines):
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)

def read_problem(lines):
    K, = read_ints(lines)
    ds = read_ints(lines)
    n, ds = ds[0], ds[1:]
    return K, n, ds

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
