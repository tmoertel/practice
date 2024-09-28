#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-05-12

"""Solution to "Consonants" Code Jam problem
https://code.google.com/codejam/contest/2437488/dashboard

Say that in a name of length L, we encounter a consonant run of length
n starting at position l and ending at position r = l + n - 1.  All
substrings name[i:j+1] for 0 <= i <= l, r <= j < L contain this run.
Therefore, if this is the only run, the n-value of the name must be
the size of the set of all i values times the size of the set of all
j values:

    n_value = (l + 1) * (L - l - n + 1)      (1)

But if there is another run at some later l2 > l, the substrings that
contain it are bounded on the left by the indices 0 <= i2 <= l2, which
overlap the earlier run's indices 0 <= i <= l.  To avoid double-
counting, we must only count the substrings whose starting index i2 is
within the non-overlapping range l < i2 <= l2.  Thus this subsequent
run's contribution to the name's n-value is given by

    n_value += (l2 - l) * (L - l2 - n + 1)   (2)

The same logic holds for all subsequent runs.  Thus we can efficiently
compute the n-value of a name by scanning it left-to-right for runs,
keeping track of the previous run's left index, and using formula (2)
to incrementally calculate the n-value.

"""

import fileinput
import sys

LETTERS = set(chr(i) for i in range(ord('a'), ord('z') + 1))
VOWELS = set('aeiou')
CONSONANTS = LETTERS - VOWELS

def main():
    sys.setrecursionlimit(int(1e6 + 2))
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print('Case #%r: %r' % (i, s))

def solve(problem):
    name, n = problem
    L = len(name)
    last_l = -1
    count = runlen = 0
    for (r, c) in enumerate(name):
        if c in CONSONANTS:
            runlen += 1
        else:
            runlen = 0
        if runlen >= n:
            l = r - n + 1
            count += (l - last_l) * (L - l - n + 1)
            last_l = l
    return count

def read_problems(lines):
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)

def read_problem(lines):
    name, strn = lines.next().split()
    n = int(strn)
    return name, n

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
