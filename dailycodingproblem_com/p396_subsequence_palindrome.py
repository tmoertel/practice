#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find the length of the longest palindromic subsequence.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2020-04-23 (#396) and was classified as Hard:

  Reported source: Google.

  Given a string, return the length of the longest palindromic
  subsequence in the string.

  For example, given the following string:

    MAPTPTMTPA

  Return 7, since the longest palindromic subsequence in the string is
  APTMTPA. Recall that a subsequence of a string does not have to be
  contiguous!

  Your algorithm should run in O(n^2) time and space.


* Solution

Given a string S, let S[i] denote the ith character of S. In Python
fashion, let i = 0 be the position of the string's first character,
and S[i:j] be the substring of all characters S[k] for i <= k < j.
S[i:] denotes the substring from position i onward, and S[:j] the
substring from position 0 up to but not including j.

Define L(S) to be the length of the longest palindromic subsequence
(henceforth LPS) within the string S. So what is L(S)? Let's consider
the cases:

If S is empty, the answer is obviously 0.

If S is a non-empty, it must have a first character c = S[0], and a
(possibly-empty) remainder S[1:]. Let's consider the possibilities:

  1. The character c is not in any LPS. In that case, L(S) = L(S[1:]).

  2. The character c is in a LPS. If so, there are two possibilities:

     a. The character c has a rightmost counterpart in S at position
        k > 0. Then L(S) = 1 + L(S[1:k]) + 1.

     b. Otherwise, L(S) = 1.

Since these possibilities are exhaustive, if we try them all and take
the maximal result, we have a recursive solution to the problem. For
efficiency, we can memoize the recursion or use dynamic programming to
build the solution from the bottom up.

"""

import functools


# This solution solves the problem recursively. It uses memoization to
# eliminate redundant work. It runs in O(n^3) time and O(n^2) space
# because it builds a memo table of size O(n^2) at a cost of O(n) per
# cell. (Python's str.rfind does a linear search.)
def longest_palindromic_subsequence_length_1(S):
    """Returns the length of the longest palindromic subsequence of a string."""

    # Helper that solves a more general version of the problem over
    # any substring of S.
    @functools.lru_cache()  # Memoize recursive calls.
    def lps_len_between(i, j):
        """Returns the length of the LPS of the substring S[i:j]."""
        if i >= j:
            return 0
        k = S.rfind(S[i], i + 1, j)  # Takes O(j - i) time.
        maxlen_so_far = 2 + lps_len_between(i + 1, k) if k >= 0 else 0
        return max(1, lps_len_between(i + 1, j), maxlen_so_far)

    # Solve the original problem in terms of the generalized problem.
    return lps_len_between(0, len(S))


# This variant of the previous solution reduces the run-time cost from
# O(n^3) to O(n^2) by paying a one-time O(n^2) price to build a dict
# that lets us replace S.rfind(char, i, j) with a constant-time
# lookup. Since the lookup result could be to the left of i, we need
# to test for this possibility after the lookup.
def longest_palindromic_subsequence_length_2(S):
    """Returns the length of the longest palindromic subsequence of a string."""
    # Build a dict D such that D.get((c, j), -1) == S.rfind(c, 0, j).
    # The cost to build the dict is O(n^2) time and space.
    n = len(S)
    rightmost_occurrence_before = dict()
    for i, c in enumerate(S):
        for j in range(i + 1, n + 1):
            rightmost_occurrence_before[(c, j)] = i

    # Helper that solves a more general version of the problem over
    # any substring of S.
    @functools.lru_cache()  # Memoize recursive calls.
    def lps_len_between(i, j):
        """Returns the length of the LPS of the substring S[i:j]."""
        if i >= j:
            return 0
        k = rightmost_occurrence_before.get((S[i], j), -1)
        maxlen_so_far = 2 + lps_len_between(i + 1, k) if k > i else 0
        return max(1, lps_len_between(i + 1, j), maxlen_so_far)

    # Solve the original problem in terms of the generalized problem.
    return lps_len_between(0, len(S))


# This variant uses dynamic programming to solve the problem in O(n^2)
# time and space. Looking at the recursive solutions, we can see that
# the solution for S[i:j] depends only on solutions for S[i+1:j] and
# S[i+1:k] for i < k < j; in other words, only on solutions for
# shorter substrings. So we can build a table of solutions starting
# with solutions for substrings of length 0, then length 1, and so
# on. When building the table entries for length m, we know that all
# of the needed entries for sub-solutions will already be filled.
def longest_palindromic_subsequence_length_3(S):
    """Returns the length of the longest palindromic subsequence of a string."""
    # Build a dict D such that D.get((c, j), -1) == S.rfind(c, 0, j).
    # The cost to build the dict is O(n^2) time and space.
    n = len(S)
    rightmost_occurrence_before = dict()
    for i, c in enumerate(S):
        for j in range(i + 1, n + 1):
            rightmost_occurrence_before[(c, j)] = i

    # Build a table of solutions for all substrings of S such that
    # table[i][j] gives the LPS length of S[i:j]. Again, the cost is
    # O(n^2) time and space.
    table = [[0] * (n + 1) for _ in range(n + 1)]
    for substring_length in range(1, n + 1):
        for i in range(n - substring_length + 1):
            j = i + substring_length
            k = rightmost_occurrence_before.get((S[i], j), -1)
            maxlen_so_far = 2 + table[i + 1][k] if k > i else 0
            table[i][j] = max(1, table[i + 1][j], maxlen_so_far)

    # Solve the original problem in terms of the generalized problem.
    return table[0][n]


# Tests.

# Test all three solution variants.
SOLVERS = (
    longest_palindromic_subsequence_length_1,
    longest_palindromic_subsequence_length_2,
    longest_palindromic_subsequence_length_3,
)


def test_empty_string_has_lps_len_of_zero():
    for solve in SOLVERS:
        assert solve("") == 0


def test_singleton_string_has_lps_len_of_one():
    for solve in SOLVERS:
        assert solve("a") == 1
        assert solve("0") == 1


def test_strings_of_unique_characters_have_lps_len_of_one():
    for solve in SOLVERS:
        assert solve("ab") == 1
        assert solve("abc") == 1
        assert solve("abcd") == 1


def test_strings_of_a_singleton_alphabet_have_lps_equal_to_their_length():
    for solve in SOLVERS:
        for n in range(7):
            assert solve("a" * n) == n


def test_soln_for_given_problem_must_match_given_soln():
    for solve in SOLVERS:
        assert solve("MAPTPTMTPA") == 7
