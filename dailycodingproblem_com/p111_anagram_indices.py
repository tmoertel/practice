#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: .

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-75-13 (#111) and was classified as Hard.

  Reported source: Google.

  Given a string S and a word W, find all anagrams of W in S and return
  their starting indices in order.

  For example, given that S = "qxiqxq" and W = "qx", return [0, 3, 4].
                               ^  ^^
"""

import collections


class Histogram(object):
    def __init__(self):
        self.counts = collections.defaultdict(int)

    def add(self, word, increment=1):
        for letter in word:
            self.counts[letter] += increment
            if not self.counts[letter]:
                del self.counts[letter]

    def subtract(self, word, increment=1):
        self.add(word, -increment)

    def __repr__(self):
        return repr(self.counts)

    def __len__(self):
        return len(self.counts)


def anagram_indices(string, word):
    # Handle corner cases.
    if word == "":
        if string == "":
            return [0]
        return list(range(len(string)))
    # Handle the general case -- searching for matches -- knowing that
    # the corner cases have been excluded.
    matches = []
    # Subtract the target word from the initially empty histogram
    # state so that when we add the letters in the window to the
    # histogram, it will be empty when the letters are an anagram of
    # the target word.
    histogram = Histogram()
    histogram.subtract(word)
    # Slide a window of length n across the string, adding and
    # subtracting characters to/from the histogram as they enter/leave
    # the window so that, at any time, the characters that are "in"
    # the histogram will be those spanned by the window.
    n = len(word)
    i = 0
    for j in range(len(string)):
        histogram.add(string[j])
        if j - i + 1 > n:
            histogram.subtract(string[i])
            i += 1
        if not histogram:
            matches.append(i)
    return matches


def test():
    soln = anagram_indices
    assert soln("", "") == [0]
    assert soln("foo", "") == [0, 1, 2]
    assert soln("foo", "x") == []
    assert soln("foo", "f") == [0]
    assert soln("foo", "o") == [1, 2]
    assert soln("foo", "of") == [0]
    assert soln("foo", "fo") == [0]
    assert soln("foo", "foo") == [0]
    assert soln("foo", "oof") == [0]
    assert soln("foo", "oo") == [1]
