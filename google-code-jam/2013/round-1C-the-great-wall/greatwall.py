#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-05-12

"""Solution to "The Great Wall" Code Jam problem
https://code.google.com/codejam/contest/2437488/dashboard#s=p2

"""

from collections import namedtuple
import fileinput
import heapq
from itertools import groupby

Tribe = namedtuple('Tribe', 'd, n, w, e, s, delta_d, delta_p, delta_s')
Attack = namedtuple('Attack', 'd, w, e, s')

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print('Case #%r: %r' % (i, s))

def solve(problem):
    tribes = problem
    daily_attacks = groupby(merge(list(map(tribe_attacks, tribes))), lambda a: a.d)
    successful_attacks = 0
    wall = HeightIntervalSet()
    for _day, attacks in daily_attacks:
        repairs = []
        for attack in attacks:
            if wall.is_vulnerable_over_interval(attack.w, attack.e, attack.s):
                repairs.append(attack)
                successful_attacks += 1
        for attack in repairs:
            wall.set_min_height_for_interval(attack.w, attack.e, attack.s)
    return successful_attacks

def tribe_attacks(tribe):
    """Yield a tribe's attacks."""
    d, n, w, e, s, delta_d, delta_p, delta_s = tribe
    for _ in range(n):
        yield Attack(d, w, e, s)
        d += delta_d
        w += delta_p
        e += delta_p
        s += delta_s

def merge(iterators):
    """Make a lazy sorted iterator that merges lazy sorted iterators."""
    streams = list(map(iterator_to_stream, iterators))
    heapq.heapify(streams)
    while streams:
        stream = heapq.heappop(streams)
        if stream is not None:
            val, stream = stream_next(stream)
            heapq.heappush(streams, stream)
            yield val

def iterator_to_stream(iterator):
    """Convert an iterator into a stream (None if the iterator is empty)."""
    try:
        return next(iterator), iterator
    except StopIteration:
        return None

def stream_next(stream):
    """Get (next_value, next_stream) from a stream."""
    val, iterator = stream
    return val, iterator_to_stream(iterator)

import sys
try:
    # Hide this import to allow pytest to scan this module w/o failing.
    from blist import sorteddict  # http://stutzbachenterprises.com/blist/
except:
    import pytest
    pytest.skip(allow_module_level=True)

class HeightIntervalSet(object):

    def __init__(self, initial_height=0):
        self.heights = sorteddict([(-sys.maxsize - 1, initial_height),
                                   (sys.maxsize, initial_height)])

    def is_vulnerable_over_interval(self, start, end, min_val):
        start *= 2
        end *= 2
        ks = self.heights._sortedkeys
        i = ks.bisect_right(start) - 1
        j = ks.bisect_right(end)
        return any(self.heights[ks[k]] < min_val for k in range(i, j))

    def set_min_height_for_interval(self, start, end, min_height):
        start *= 2
        end *= 2
        ks = self.heights._sortedkeys
        i = ks.bisect_right(start) - 1
        x = ks[i]
        height = self.heights[x]
        current_height = background_height = height
        if height < min_height:
            current_height = min_height
            self.heights[start] = min_height
            if x != start:
                i += 1
        while True:
            i += 1
            x = ks[i]
            height = self.heights[x]
            if x > end:
                if x != end + 1:
                    self.heights[end + 1] = background_height
                break
            background_height = height
            if height < min_height:
                if current_height == min_height:
                    del self.heights[x]
                    i -= 1
                else:
                    self.heights[x] = current_height = min_height
            else:
                current_height = height

def read_problems(lines):
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)

def read_problem(lines):
    N, = read_ints(lines)
    tribes = []
    for _ in range(N):
        tribe = Tribe(*read_ints(lines))
        tribes.append(tribe)
    return tribes

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
