#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-11-15

"""Solution to "Anonymous Letter" EPI problem

"Problem 12.9 : You are required to write a method which takes an
anonymous letter L and text from a magazine M.  Your method is to
return true iff L can be written using M, i.e., if a letter appears k
times in L, it must appear at least k times in M."  Source: _Elements
of Programming Interviews_.

Discussion.  To write the anonymous letter L, we need to take its
constituent characters from the magazine M.  Thus we can write the
letter only if there are enough intances of each needed letter in the
magazine.  In other words, only if L is a "subdocument" of M.  More
formally, if we let c_D(x) denote the count of occurrences of the
letter x in the document D, we can write the letter iff, forall x in
L, c_L(x) <= c_M(x).  To keep track of the counts, we can use a map
from characters to counts.  Fortunately, the Python collections module
provides a Counter class tailored to this purpose.

"""

from collections import Counter

def is_subdocument(L, M):
    counts_L = Counter(L)
    counts_M = Counter(M)
    return all(n <= counts_M[x] for x, n in counts_L.iteritems())

def test():
    for xs in "", "x", "xx", "xyx", "xyyx":
        for ys in "", "1", "2", "12", "123":
            assert is_subdocument(xs, xs + ys)
            assert is_subdocument(ys, xs + ys)
            assert is_subdocument(xs, ys + xs)
            assert is_subdocument(ys, ys + xs)
            if ys:
                assert not is_subdocument(xs + ys, xs)
                assert not is_subdocument(ys + xs, xs)
            if xs:
                assert not is_subdocument(xs + ys, ys)
                assert not is_subdocument(ys + xs, ys)


if __name__ == '__main__':
    main()
