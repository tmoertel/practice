#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to interview problem: select a random element from a stream.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-04-08 and was classified as Medium.

  Reported source: Facebook.

  Given a stream of elements too large to store in memory, pick a
  random element from the stream with uniform probability.


"""

import random


def random_element(xs):
    n = 0
    for n, x in enumerate(xs, 1):
        if random.randint(1, n) == 1:
            selection = x
    assert n > 0
    return selection


def test_random_stream_selection():
    for x in range(10):
        assert random_element([x]) == x
