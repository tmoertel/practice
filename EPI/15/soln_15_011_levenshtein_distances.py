#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-11-08

"""Solution to "Levenshtein Distances" problem, EPI 15.11.

This is problem 15.11 in the book Elements of Programming Interviews.

Problem:  Given two strings A and B, compute the Levenshtein distance
          between them.

The Levenshtein distance is defined to be the minimum number of
single-character insertions, deletions, or replacements needed to
convert the first string into the second.

We can solve this problem by thinking recursively.  Consider just the
first character of each string.  If the two characters are the same,
no edits are required to make them match, and we can remove these
characters without affecting the distance between their respective
strings.  That is, in Haskell notation,

    dist (x:xs) (y:ys) | x == y  =  dist xs ys

Otherwise, we know some editing must be required.  The only choices
are insertion, deletion, and replacement.  Let's consider each.

If we insert a character into the first string, the only character
that it makes sense to insert is the one that matches the leading
character of the second string.  In that case, the inserted character
will match the second string's leading character, and both can be
removed, as before.  Thus, in this case, the first string will end up
unchanged (since it had a character inserted and then immediately
removed) and the second string will have been shortened by its leading
character.  Thus we have the equality,

   dist (x:xs) (y:ys)  =  1 + dist (x:xs) ys   {- if insertion -}

For deletion, it's the other way around.  The first word loses its
leading character, and the second string remains unchanged:

   dist (x:xs) (y:ys)  =  1 + dist xs (y:ys)   {- if deletion -}

For replacement, we will replace the leading character of the first
string with the character that matches the leading character of the
second string.  Both characters can then be removed:

   dist (x:xs) (y:ys)  =  1 + dist xs ys   {- if replacement -}

Since the best option is the one that minimizes the total distance,
we can select the best using min:

    dist (x:xs) (y:ys) | x /= y  =  min [1 + dist (x:xs) ys,
                                         1 + dist xs (y:ys),
                                         1 + dist xs ys]

Thus our overall recurrence is, factoring out the (1 +) since addition
distributes over min, as follows:

    dist (x:xs) (y:ys) | x == y  =  dist xs ys
    dist (x:xs) (y:ys) | x /= y  =  1 + min [dist (x:xs) ys,
                                             dist xs (y:ys),
                                             dist xs ys]

Now for the base cases.  They occur when one of the strings is empty.
In those cases we need a number of insertions or deletions equal to
the length of the other string:

    dist [] ys  =  length ys
    dist xs []  =  length xs

And that completes the recursive solution.

Now I offer three Python implementations:

1.  Top-down recursive (but memoized for efficiency).
    Both time and space use is O(len(A) * len(B)).

2.  Bottom-up dynamic programming w/ full memo table.
    Both time and space use is O(len(A) * len(B)).

3.  Bottom-up dynamic programming, w/ trimmed memo table of 2 rows.
    Time use is O(len(A) * len(B)), but space use improves to O(len(B)).

They all follow closely to the reasoning I give above, so I won't
elaborate further in the comments, reserving them instead for
implementation details.

"""

# recursive

def levenshtein_distance1(A, B):
    @memoize
    def ld(i, j):
        # base cases
        if i == len(A):
            return len(B) - j
        if j == len(B):
            return len(A) - i

        # recursive cases
        if A[i] == B[j]:
            return ld(i + 1, j + 1)
        return 1 + min(ld(i + 1, j),
                       ld(i + 1, j + 1),
                       ld(i, j + 1))
    return ld(0, 0)


# dynamic programming

def levenshtein_distance2(A, B):
    # initialize memo table to all zeroes
    memo = [[0] * (len(B) + 1) for _ in xrange(len(A) + 1)]

    # fill in cells corresponding to base cases
    for i in xrange(len(A)):
        memo[i][-1] = len(A) - i
    for j in xrange(len(B)):
        memo[-1][j] = len(B) - j

    # fill in the remaining cells using recurrence, working bottom up
    for i in xrange(len(A) - 1, -1, -1):
        for j in xrange(len(B) - 1, -1, -1):
            if A[i] == B[j]:
                memo[i][j] = memo[i + 1][j + 1]
            else:
                memo[i][j] = 1 + min(memo[i + 1][j],
                                     memo[i + 1][j + 1],
                                     memo[i][j + 1])

    # the solution is in the topmost cell
    return memo[0][0]


# dynamic programming, trimmed

def levenshtein_distance3(A, B):
    # In this version, I keep only the 2 most-recent rows of the memo
    # table.  Compared to the previous version, prev = memo[i + 1] and
    # cur = memo[i].

    # initialize bottom row of the memo table
    prev = [len(B) - j for j in xrange(len(B) + 1)]

    # allocate a scratch space for the current work row
    cur = [0 for _ in prev]

    # fill in the remaining cells using recurrence, working bottom up
    for i in xrange(len(A) - 1, -1, -1):
        cur[-1] = len(A) - i  # initialize current row
        for j in xrange(len(B) - 1, -1, -1):
            if A[i] == B[j]:
                cur[j] = prev[j + 1]
            else:
                cur[j] = 1 + min(prev[j], prev[j + 1], cur[j + 1])
        prev, cur = cur, prev  # recycle prev as next iteration's work row

    # the solution is in the topmost cell
    return prev[0]


# memoization decorator

import functools

def memoize(f):
    cache = {}
    @functools.wraps(f)
    def g(*args):
        try:
            return cache[args]
        except KeyError:
            ret = cache[args] = f(*args)
        return ret
    return g


# testing

def test():

    from nose.tools import assert_equal as eq

    for ld in (levenshtein_distance1,
               levenshtein_distance2,
               levenshtein_distance3):

        eq(0, ld("", ""))
        eq(0, ld("ab", "ab"))
        eq(0, ld("abc", "abc"))

        eq(1, ld("a", ""))
        eq(1, ld("", "b"))
        eq(1, ld("bc", "abc"))
        eq(1, ld("ac", "abc"))
        eq(1, ld("ab", "abc"))
        eq(1, ld("abc", "bc"))
        eq(1, ld("abc", "ac"))
        eq(1, ld("abc", "ab"))
        eq(1, ld("xbc", "abc"))
        eq(1, ld("axc", "abc"))
        eq(1, ld("abx", "abc"))
        eq(1, ld("abc", "xbc"))
        eq(1, ld("abc", "axc"))
        eq(1, ld("abc", "abx"))

        eq(2, ld("c", "abc"))
        eq(2, ld("a", "abc"))
        eq(2, ld("abc", "c"))
        eq(2, ld("abc", "a"))
        eq(2, ld("xxc", "abc"))
        eq(2, ld("axx", "abc"))
        eq(2, ld("xbx", "abc"))
        eq(2, ld("abc", "xxc"))
        eq(2, ld("abc", "axx"))
        eq(2, ld("abc", "xbx"))
