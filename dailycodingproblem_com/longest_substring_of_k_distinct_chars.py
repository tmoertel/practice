#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to interview problem: length of longest substring of k distinct chars.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-04-06 and was classified as Hard.

  Reported source: Amazon.

  Given a string and an integer k, find the length of the longest
  substring that contains no more than k distinct characters.

  For example, consider the string "xyzyx". If k = 2, the longest
  substring with k distinct characters is "yzy", and the answer is
  therefore 3. If k = 3, however, the longest substring would be
  "xyzyx", and the answer would be 5.


* Solution

This solution runs in O(n) time and uses O(k) space, where n is the
string's length.

"""

import collections

def soln(k, s):
    # Helpers to let us track the chars in use.
    used_chars = collections.Counter()
    def add_char_at(i):
        used_chars.update(s[i])
    def remove_char_at(i):
        c = s[i]
        used_chars.subtract(c)
        if not used_chars[c]:
            del used_chars[c]
    # Start with an empty substring.
    max_len = start = 0
    # Advance the end of the substring and then advance the start
    # until no more than k distint chars are used. Repeat until we
    # exhaust the input string.
    for end in range(len(s)):
        add_char_at(end)
        while len(used_chars) > k:
            remove_char_at(start)
            start += 1
        max_len = max(max_len, end - start + 1)
    return max_len


def test():
    # Base case: for all strings s, soln(0, s) = 0.
    for l in range(1, 5):
        assert soln(0, 'x' * l) == 0
    # Base case: for all k >= 0, soln(k, '') = 0.
    for k in range(5):
        assert soln(k, '') == 0
    # Example cases.
    assert soln(2, 'abcba') == 3
    # Property: for all k > 0, l >= 0, and chars c, soln(k, c * l) = l.
    for k in range(1, 5):
        for l in range(8):
            for c in 'abcdef':
                assert soln(k, c * l) == l
    # Property: if s has distinct chars only and len(s) >= k, soln(k, s) == k.
    for k in range(5):
        assert soln(k, 'abcdefghi') == k
