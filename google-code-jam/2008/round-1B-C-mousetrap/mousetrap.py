#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-06-10

"""Solution to "Mousetrap" Code Jam problem
https://code.google.com/codejam/contest/32017/dashboard#s=p2&a=0

"""

import fileinput



def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %s' % (i, s)

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

# binary tree = None | Node(left_count val left right)
class Node(object):
    def __init__(self, left_count, val, left, right):
        self.left_count = left_count
        self.val = val
        self.left = left
        self.right = right
    def __repr__(self):
        def f(t, indent=0):
            if t is None:
                return '  ' * indent + '*'
            left = f(t.left, indent + 1)
            right = f(t.right, indent + 1)
            return '\n'.join(['  ' * indent +
                              ('%r (%r)' % (t.left_count, t.val)),
                              left, right])
        return f(self)

def mktree(size, starting_val=1):
    if size == 0:
        return None
    if size == 1:
        return Node(1, starting_val, None, None)
    mid = size // 2
    left = mktree(mid, starting_val)
    right = mktree(size - mid - 1, starting_val + mid + 1)
    return Node(mid + 1, starting_val + mid, left, right)

def assign_card(tree, index, card):
    if tree.left_count < index:
        assign_card(tree.right, index - tree.left_count, card)
    elif tree.left_count > index:
        tree.left_count -= 1
        assign_card(tree.left, index, card)
    else:
        tree.left_count -= 1
        if not isinstance(tree.val, tuple):
            tree.val = (tree.val, card)
        else:
            assign_card(tree.left, index, card)

def get_card(tree, size, index):
    mid = size // 2
    if index <= mid:
        return get_card(tree.left, mid, index)
    if index == mid + 1:
        return tree.val[1]
    return get_card(tree.right, size - mid - 1, index - mid - 1)

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
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
