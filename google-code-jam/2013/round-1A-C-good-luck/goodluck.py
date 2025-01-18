#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-26


"""Solution to "Good Luck" Code Jam problem
http://code.google.com/codejam/contest/2418487/dashboard#s=p2

"""

import fileinput
import functools
from functools import reduce


def memoize(fn):
    cache = dict()

    @functools.wraps(fn)
    def memoized_fn(*args):
        if args in cache:
            return cache[args]
        return cache.setdefault(args, fn(*args))

    return memoized_fn


def trace(fn):
    @functools.wraps(fn)
    def traced_fn(*args):
        try:
            res = fn(*args)
        except Exception as e:
            res = e
        print("%s%r => %r" % (fn.__name__, args, res))
        return res

    return traced_fn


def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print("Case #%r:\n%s" % (i, "\n".join(s)))


def solve(problem):
    _, N, M, K, prodss = problem
    solns = []

    @memoize
    def factors(n, d=M):
        if n == 1:
            yield ""
        while d >= 2:
            if n % d == 0:
                for ds in factors(n // d, d):
                    yield str(d) + ds
            d -= 1

    def candiate_factors(n):
        s = set()
        for f in factors(n):
            if len(f) == N:
                s.add(f)
        return s

    for prods in prodss:
        candidates = [_f for _f in map(candiate_factors, prods) if _f]
        winner = None
        if candidates:
            winners = reduce(set.__rand__, candidates)
            if winners:
                winner = list(winners)[0]
        solns.append(winner or "2" * N)
    return solns


def read_problems(lines):
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)


def read_problem(lines):
    r, n, m, k = read_ints(lines)
    prodss = [read_ints(lines) for _ in range(r)]
    return r, n, m, k, prodss


def read_ints(lines):
    return [int(s) for s in lines.next().split()]


if __name__ == "__main__":
    main()
