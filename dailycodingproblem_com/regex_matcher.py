#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to interview problem: select a random element from a stream.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-04-18 (#24) and was classified as Hard.

  Reported source: Facebook.

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


# Simple recursive implementation using string slices.
def match_regex_1(s, r):
    """Returns true if string s is matched by regex r; false otherwise."""
    # Case: string is empty.
    if not s:
        if not r:
            return True
        if r[0] == "*":
            return match_regex_1(s, r[1:])
        return False
    # Case: string is not empty.
    if not r:
        return False
    regex_instruction = r[0]
    if regex_instruction in (".", s[0]):
        return match_regex_1(s[1:], r[1:])
    if regex_instruction == "*":
        return match_regex_1(s[1:], r[1:]) or match_regex_1(s[1:], r)
    return False


# Efficiency optimization that avoids repeatitive work:
# Memoized recursive implementation using substring indices instead of slices.
def match_regex_2(s, r):
    """Returns true if string s is matched by regex r; false otherwise."""
    s_len = len(s)
    r_len = len(r)

    @memoize
    def match(s_idx, r_idx):
        """Matches string s[s_idx:] to regex r[r_idx:]."""
        # Case: string is empty.
        if s_idx == s_len:
            if r_idx == r_len:
                return True
            if r[r_idx] == "*":
                return match(s_idx, r_idx + 1)
            return False
        # Case: string is not empty.
        if r_idx == r_len:
            return False
        regex_instruction = r[r_idx]
        if regex_instruction in (".", s[s_idx]):
            return match(s_idx + 1, r_idx + 1)
        if regex_instruction == "*":
            return match(s_idx + 1, r_idx + 1) or match(s_idx + 1, r_idx)
        return False

    return match(0, 0)


# Variant:
# Simulated recursion using stack machine (avoids Python's stack-depth limit).
def match_regex_3(s, r):
    """Returns true if string s is matched by regex r; false otherwise."""
    s_len = len(s)
    r_len = len(r)
    stack = [(0, 0)]
    while stack:
        s_idx, r_idx = stack.pop()
        # Case: string is empty.
        if s_idx == s_len:
            if r_idx == r_len:
                return True
            if r[r_idx] == "*":
                stack.append((s_idx, r_idx + 1))
            continue
        # Case: string is not empty.
        if r_idx == r_len:
            continue
        regex_instruction = r[r_idx]
        if regex_instruction in (".", s[s_idx]):
            stack.append((s_idx + 1, r_idx + 1))
        if regex_instruction == "*":
            stack.append((s_idx + 1, r_idx + 1))
            stack.append((s_idx + 1, r_idx))
    return False


# Variant:
# Simulated recursion using memoized stack machine; avoids repetitive work.
def match_regex_4(s, r):
    """Returns true if string s is matched by regex r; false otherwise."""
    s_len = len(s)
    r_len = len(r)
    stack = [(0, 0)]
    explored = set()  # States we've already explored.

    def explore(s_idx, r_idx):
        if (s_idx, r_idx) not in explored:
            explored.add((s_idx, r_idx))
            stack.append((s_idx, r_idx))

    while stack:
        s_idx, r_idx = stack.pop()
        # Case: string is empty.
        if s_idx == s_len:
            if r_idx == r_len:
                return True
            if r[r_idx] == "*":
                explore(s_idx, r_idx + 1)
            continue
        # Case: string is not empty.
        if r_idx == r_len:
            continue
        regex_instruction = r[r_idx]
        if regex_instruction in (".", s[s_idx]):
            explore(s_idx + 1, r_idx + 1)
        if regex_instruction == "*":
            explore(s_idx + 1, r_idx + 1)
            explore(s_idx + 1, r_idx)
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
    for M in match_regex_1, match_regex_2, match_regex_3, match_regex_4:
        # Case: empty string and empty regex.
        assert M("", "")
        # Case: non-empty string and empty regex.
        assert M("c", "") == False
        assert M("co", "") == False
        # Case: empty string and non-empty regex.
        assert M("", "*")
        assert M("", "**")
        assert M("", "***")
        assert M("", ".") == False
        assert M("", "*.") == False
        assert M("", ".*") == False
        assert M("", "*.*") == False
        assert M("", "c") == False
        # Case: non-empty string and non-empty regex.
        assert M("ray", "ra.")
        assert M("raymond", "ra.") == False
        assert M("chat", ".*at")
        assert M("chats", ".*at") == False
        assert M("chat", "char") == False
        assert M("chat", "hat") == False
