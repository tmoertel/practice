#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-05-08

"""Solution to "Garbled Email" Code Jam problem
https://code.google.com/codejam/contest/2434486/dashboard#s=p2

"""

from collections import defaultdict
import fileinput
from heapq import heappop, heappush


LETTERS = ''.join(chr(i) for i in xrange(ord('a'), ord('z') + 1))

def main():
    words = prefix_tree(file('garbled_email_dictionary.txt').read().split())
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(words, p)
        print 'Case #%r: %r' % (i, s)

def solve(words, S):
    frontier = [(0, len(S), 0, S, words)]
    seen = set(frontier[0])
    def enqueue(*state):
        if state not in seen:
            seen.add(state)
            heappush(frontier, state)
    while frontier:
        cost, slen, subst_lockout, s, t = heappop(frontier)
        # have we reached the end of the message?
        if not s:
            if EOW in t:
                return cost
            continue
        # have we reached the end of a dictionary word?
        if EOW in t:
            enqueue(cost, slen, subst_lockout, s, words)
        # consume the next character
        c, s = s[0], s[1:]
        if c in t:
            enqueue(cost, slen - 1, min(0, subst_lockout + 1), s, t[c])
        if subst_lockout == 0:
            for l in LETTERS:
                if l != c and l in t:
                    enqueue(cost + 1, slen - 1, -4, s, t[l])

class EOW(object):
    """End-of-word marker."""
    def __repr__(self):
        return '$'
EOW = EOW()

class iddict(defaultdict):
    def __hash__(self):
        return id(self)

def prefix_tree(words):
    """Build a prefix tree representing a set of words."""
    d = iddict(iddict)
    for word in words:
        t = d
        for c in word:
            t = t.setdefault(c, iddict())
        t[EOW] = iddict()  # mark end of word
    return d

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    S = lines.next().strip()
    return S

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
