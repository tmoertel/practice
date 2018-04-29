#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2018-04-29

r"""Solution to "Steed 2: Cruise Control" Code Jam problem

https://code.google.com/codejam/contest/8294486/dashboard#s=p0

Problem

The problem says that Annie starts on her horse at position 0 and that there
are N horses ahead of her on the trail to the destination at kilometer D. The
horses ahead of her run at their respective maximum speeds but will slow to
match any horse they would otherwise pass. We are asked to find the fastest
constant speed that Anne's horse can run at to get her to D without passing
any other horse.

Solution

                Annie    /--- horses ahead ---\          Destination
                |
    Horse       A        4     3        2     1           0
    Trail       +--------+-----+--------+-----+-----------|---------->
    Kilometer   0        S[4]  S[3]     S[2]  S[1]        D

Let's ignore Annie for now and focus on the N horses ahead. Say we have sorted
the horses by distance to the finish line at D so that horse 1 is the closest
to D and horse N is the farthest (see diagram above). Now consider horse 1.
It must reach the destination at time t[1] = (D - S[1]) / K[1] because there
are no horses ahead to possibly slow it. Now consider horse 2. If it is going
fast enough to meet horse 1, it will slow to match pace end reach D at the
same time: t[2] = t[1]. Otherwise, it will be "unblocked" and reach D in its
own time: t[2] = (D - S[2]) / K[2]. This logic holds for the next horse, and
so on, giving us the general recurrence

    t[i] = max(t[i - 1], (D - S[i]) / K[i])    for i > 1.

For convenience, we introduce a sentinel horse 0 that starts at D, letting us
use the recurrence for all i > 0. We can solve for all t[i] in linear time by
working from i = 1 to N. Of course, sorting the horses in the first place
takes O(N lg N) time, thus the overall solution has O(N lg N) run time.
Memory consumption is either O(N) or O(1), depending on whether we sort
the horses in place.

Finally, we can solve for Annie's horse's constant pace by finding the speed
that lets it reach D at the exact same time as horse N:

    speed = D / t[N]

"""

import fileinput
import functools

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print('Case #%r: %r' % (i, s))

def solve(problem):
    D, horses = problem
    # The fastest that Annie's horse can travel is the speed that lets her
    # reach point D at the exact same time as the preceding horse.
    return D / best_finish_time(D, horses)

def best_finish_time(D, horses):
    """Computes the best time all horses ahead of Annie's to reach point D."""
    def best_unblocked_time(horse):
        starting_position, max_speed = horse
        return (float(D) - starting_position) / max_speed
    def best_time(best_time_of_preceding_horse, horse):
        return max(best_unblocked_time(horse), best_time_of_preceding_horse)
    horses.sort(reverse=True)
    return functools.reduce(best_time, horses, 0)

def read_problems(lines):
    T = int(lines.next())
    for _ in range(T):
        yield read_problem(lines)

def read_problem(lines):
    D, N = read_ints(lines)
    horses = [read_ints(lines) for _ in range(N)]
    return D, horses

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
