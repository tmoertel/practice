#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-05-08

"""Solution to "Garbled Email" Code Jam problem
https://code.google.com/codejam/contest/2434486/dashboard#s=p2

The logic behind this solution is straightforward, but the code is a
little convoluted by our need to work around Python's recursion
limitations.  Here's the easier-to-follow recursive version:

def solve(words, S):
    N = len(S)
    dead_penalty = sys.maxint >> 1
    @memoize
    def mincost(i, subst_lockout, tree):
        if i == N:
            return 0 if EOW in tree else dead_penalty
        def possibilities():
            yield dead_penalty
            if EOW in tree:
                yield mincost(i, subst_lockout, words)
            if S[i] in tree:
                yield mincost(i + 1, max(0, subst_lockout - 1), tree[S[i]])
            if subst_lockout == 0:
                for l in LETTERS:
                    if l != S[i] and l in tree:
                        yield 1 + mincost(i + 1, 4, tree[l])
        return min(possibilities())
    return mincost(0, 0, words)

"""

import fileinput
import sys

LETTERS = "".join(chr(i) for i in range(ord("a"), ord("z") + 1))


def main():
    words = prefix_tree(file("garbled_email_dictionary.txt").read().split())
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(words, p)
        print("Case #%r: %r" % (i, s))


def solve(words, S):
    N = len(S)
    dead_penalty = sys.maxsize >> 1

    # the following is an ode to Python's tragic lack of tail-call elimination

    cache = {None: 0}
    root = (0, 0, words)
    stack = [(root, 0, root)]

    def push(*args):
        stack.append(args)

    while stack:
        dest, incr, cell = job = stack.pop()
        # if the answer to this job is known, use it
        if cell in cache:
            cache[dest] = min(cache.get(dest, dead_penalty), cache[cell] + incr)
            continue
        # otherwise, expand this job into its subjobs and let them run
        push(*job)
        push(cell, dead_penalty, None)  # default the cell to a dead end
        i, subst_lockout, tree = cell
        # are we at the end of the message?
        if i == N:
            cache[cell] = 0 if EOW in tree else dead_penalty
            continue
        # is there a possible word ending here?
        if EOW in tree:
            push(cell, 0, (i, subst_lockout, words))
        # is the current char part of a dictionary word?
        if S[i] in tree:
            push(cell, 0, (i + 1, max(0, subst_lockout - 1), tree[S[i]]))
        # can we change the current char to part of a dictionary word?
        if subst_lockout == 0:
            for l in LETTERS:
                if l != S[i] and l in tree:
                    push(cell, 1, (i + 1, 4, tree[l]))
    return cache[root]


class EOW(object):
    """End-of-word marker."""

    def __repr__(self):
        return "$"


EOW = EOW()


class iddict(dict):
    def __hash__(self):
        return id(self)


def prefix_tree(words):
    """Build a prefix tree representing a set of words."""
    d = iddict()
    for word in words:
        t = d
        for c in word:
            t = t.setdefault(c, iddict())
        t[EOW] = iddict()  # mark end of word
    return d


def read_problems(lines):
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)


def read_problem(lines):
    S = lines.next().strip()
    return S


def read_ints(lines):
    return [int(s) for s in lines.next().split()]


if __name__ == "__main__":
    main()
