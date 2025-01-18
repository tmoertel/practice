#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-08


"""Solution to "File Fix-It" Code Jam problem
http://code.google.com/codejam/contest/635101/dashboard#s=p0

"""

import fileinput
import itertools


def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print("Case #%r: %r" % (i, s))


def solve(problem):
    existing, wanted = problem
    count = 0
    for path in sorted(wanted, key=len):
        while path and path not in existing:
            count += 1
            existing.add(path)
            path, _ = path.rsplit("/", 1)
    return count


def read_problems(lines):
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)


def read_problem(lines):
    N, M = list(map(int, lines.next().split()))
    existing = set(s.strip() for s in itertools.islice(lines, N))
    wanted = set(s.strip() for s in itertools.islice(lines, M))
    return existing, wanted


if __name__ == "__main__":
    main()
