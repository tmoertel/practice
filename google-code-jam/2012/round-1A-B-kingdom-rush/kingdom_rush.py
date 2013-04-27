#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-26


"""Solution to "Kingdom Rush" Code Jam problem
http://code.google.com/codejam/contest/1645485/dashboard#s=p1

Claims:

Each level must be visited at least once.  Thus the minimum number of
visits is achieved when we minimize the number of levels that must be
visited twice.  Thus we must maximize the number of levels that can be
played with a 2-star rating on their first visit, eliminating the need
to visit them again.  Because the count of stars we have collected is
increasing, and therefore smallest at the outset, we must process
levels in increasing order of 2-star-rating requirement, so that the
smallest requirements are encountered earliest.

But when we don't have enough stars to take the next level at the
2-star requirement, we must select a level at the 1-star requirement.
Then, by similar logic, we should select the level eligible for 1-star
play that has the *highest* requirement for 2-star play.  Since we are
forced to "burn" a level's opportunity for 2-star play on its first
encounter, we must burn the level with the least opportunity; this
preserves all the other levels' opportunities, which are better (or at
least no worse).

"""

import fileinput
from heapq import heappop, heappush

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %s' % (i, s)

def solve(problem):
    N, level_stars = problem
    a, b = zip(*level_stars)
    levels_by_a = sorted(xrange(N), key=a.__getitem__)
    levels_by_b = sorted(xrange(N), key=b.__getitem__)
    visited = set()
    one_star_eligible_levels = []
    stars = visited_twice = next_one_star_level = 0

    for i in levels_by_b:

        # while we can't take a level at 2-star play; try at 1-star play
        while stars < b[i]:

            # (1) expand pool of levels eligible at one star
            while next_one_star_level < N:
                j = levels_by_a[next_one_star_level]
                if stars < a[j]:
                    break
                next_one_star_level += 1
                heappush(one_star_eligible_levels, (-b[j], j))

            # (2) take the best unvisited level from the pool
            while one_star_eligible_levels:
                j = heappop(one_star_eligible_levels)[1]
                if j not in visited:
                    break

            # (3) if we couldn't find a level to play, we have failed
            else:
                return 'Too Bad'

            # (4) otherwise, we visit the level and loop
            visited.add(j)
            stars += 1

        stars += 1 + (i not in visited)
        visited_twice += i in visited
        visited.add(i)

    return str(N + visited_twice)

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    N, = read_ints(lines)
    level_stars = [read_ints(lines) for _ in xrange(N)]
    return N, level_stars

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
