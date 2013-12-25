#!/usr/bin/env python

"""My solution to the "two-egg" programming-interview problem.

The problem:

  You are given two eggs, and access to a 100-storey building. Both
  eggs are identical. The aim is to find out the highest floor from
  which an egg will not break when dropped out of a window from that
  floor. If an egg is dropped and does not break, it is undamaged and
  can be dropped again. However, once an egg is broken, that's it for
  that egg.

  If an egg breaks when dropped from floor n, then it would also have
  broken from any floor above that. If an egg survives a fall, then it
  will survive any fall shorter than that.

  The question is: What strategy should you adopt to minimize the
  number egg drops it takes to find the solution?. (And what is the
  worst case for the number of drops it will take?)

  Source:  http://www.datagenetics.com/blog/july22012/index.html

Reasoning behind my solution.  We are looking for N(F=100, E=2), the
worst-case number of trial drops required to find the highest of F
floors from which we can drop an egg without it breaking, given that
we have E eggs to use for trials.  It's obvious that N(F, 1) = F, but
what about when E > 1?

In that case, we could drop one of our spare eggs at the midpoint of
the floors to partition the search space in half, as in a binary
search.  But there's an asymmetry: if the egg breaks, we have only
E - 1 eggs left to finish searching the lower half; but if it doesn't
break, we have all E eggs for the upper half and can search that half
with fewer trials.  So we would be better off dropping our egg not at
the midpoint but a bit lower.  But where exactly?

Since we want to minimize our worst-case cost, we ought to drop the
egg at the floor I that minimizes the maximum of the lower and upper
searches.  In other words:

  N(F, E) = 1 + min max[ N(I-1, E-1), N(F-I, E) ] for i in 1..F-1
                 i

This recurrence relation, along with our base cases

  N(F, 1) = F
  N(0, E) = 0
  N(1, E) = 1

gives us everything we need for a dynamic-programming solution.  Here,
I just memoize the recurrence rather than building the memo table from
the ground up.

Usage:    ./eggs.py F E

Example:  ./eggs.py 100 2
          14

"""

import functools
import sys


def memoize(f):
    cache = {}
    @functools.wraps(f)
    def newfunc(*args):
        args = tuple(args)
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return newfunc


@memoize
def worst_case_trial_count(floors, eggs):
    if eggs == 1 or floors < 2:
        return floors
    return min(1 + max(worst_case_trial_count(i - 1, eggs - 1),
                       worst_case_trial_count(floors - i, eggs))
               for i in xrange(1, floors))


if __name__ == '__main__':
    print worst_case_trial_count(int(sys.argv[1]), int(sys.argv[2]))
