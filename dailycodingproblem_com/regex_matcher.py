#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to interview problem: select a random element from a stream.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-04-18 (#24) and was classified as Hard.

  This problem was asked by Facebook.

  Implement regular expression matching with the following special
  characters:

  . (period) which matches any single character
  * (asterisk) which matches zero or more of the preceding element

  That is, implement a function that takes in a string and a valid
  regular expression and returns whether or not the string matches the
  regular expression.

  For example, given the regular expression "ra." and the string
  "ray", your function should return true. The same regular expression
  on the string "raymond" should return false.

  Given the regular expression ".*at" and the string "chat", your
  function should return true. The same regular expression on the
  string "chats" should return false.

"""

import functools
import random

# Simple recursive implementation using string slices.
def match_regexp_1(s, r):
    """Returns true if string s is matched by regex r; false otherwise."""
    # Case: string is empty.
    if not s:
        if not r:
            return True
        if r[0] == '*':
            return match_regexp_1(s, r[1:])
        return False
    # Case: string is not empty.
    if not r:
        return False
    regexp_instruction = r[0]
    if regexp_instruction in ('.', s[0]):
        return match_regexp_1(s[1:], r[1:])
    if regexp_instruction == '*':
        return match_regexp_1(s[1:], r[1:]) or match_regexp_1(s[1:], r)
    return False

# Efficiency optimization that avoids repeatitive work:
# Memoized recursive implementation using substring indices instead of slices.
def match_regexp_2(s, r):
    """Returns true if string s is matched by regex r; false otherwise."""
    m = len(s)
    n = len(r)
    @memoize
    def match(i, j):
        """Matches string s[i:] to regex r[j:]."""
        # Case: string is empty.
        if i == m:
            if j == n:
                return True
            if r[j] == '*':
                return match(i, j + 1)
            return False
        # Case: string is not empty.
        if j == n:
            return False
        regexp_instruction = r[j]
        if regexp_instruction in ('.', s[i]):
            return match(i + 1, j + 1)
        if regexp_instruction == '*':
            return match(i + 1, j + 1) or match(i + 1, j)
        return False
    return match(0, 0)

# Variant:
# Simulated recursion using stack machine (avoids Python's stack-depth limit).
def match_regexp_3(s, r):
    """Returns true if string s is matched by regex r; false otherwise."""
    m = len(s)
    n = len(r)
    stack = [(0, 0)]
    while stack:
        i, j = stack.pop()
        # Case: string is empty.
        if i == m:
            if j == n:
                return True
            if r[j] == '*':
                stack.append((i, j + 1))
            continue
        # Case: string is not empty.
        if j == n:
            continue
        regexp_instruction = r[j]
        if regexp_instruction in ('.', s[i]):
            stack.append((i + 1, j + 1))
        if regexp_instruction == '*':
            stack.append((i + 1, j + 1))
            stack.append((i + 1, j))
    return False

# Variant:
# Simulated recursion using memoized stack machine; avoids repetitive work.
def match_regexp_4(s, r):
    """Returns true if string s is matched by regex r; false otherwise."""
    m = len(s)
    n = len(r)
    stack = [(0, 0)]
    explored = set()  # States we've already explored.
    def explore(i, j):
        if (i, j) not in explored:
            explored.add((i, j))
            stack.append((i, j))
    while stack:
        i, j = stack.pop()
        # Case: string is empty.
        if i == m:
            if j == n:
                return True
            if r[j] == '*':
                explore(i, j + 1)
            continue
        # Case: string is not empty.
        if j == n:
            continue
        regexp_instruction = r[j]
        if regexp_instruction in ('.', s[i]):
            explore(i + 1, j + 1)
        if regexp_instruction == '*':
            explore(i + 1, j + 1)
            explore(i + 1, j)
    return False

def memoize(f):
    """Make a memoized version of f that returns cached results."""
    cache = {}
    @functools.wraps(f)
    def g(*args):
        ret = cache.get(args, cache)
        if ret is cache:
            ret = cache[args] = f(*args)
        return ret
    return g

def test():
    for M in match_regexp_1, match_regexp_2, match_regexp_3, match_regexp_4:
        assert M('', '')
        assert M('', '*')
        assert M('', '**')
        assert M('', '***')
        assert M('', '.') == False
        assert M('', '*.') == False
        assert M('', '.*') == False
        assert M('', '*.*') == False
        assert M('', 'c') == False
        assert M('ray', 'ra.')
        assert M('raymond', 'ra.') == False
        assert M('chat', '.*at')
        assert M('chats', '.*at') == False
