#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-05


"""Solution to "Rope Intranet" Code Jam problem
http://code.google.com/codejam/contest/619102/dashboard#s=p0

"""

import fileinput


def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print("Case #%r: %r" % (i, s))


def solve(wires):
    """Faster O(N^2) brute-force solution (timing: 1.6s)."""
    if not wires:
        return 0
    N = len(wires)
    (lri, lir), (rri, rir) = list(map(ranks, list(zip(*wires))))
    # the following brute-force solution runs in O(N^2) time for N wires
    return sum(len(set(lri[: lir[i]]) & set(rri[rir[i] + 1 :])) for i in range(N))


def ranks(xs):
    rank_to_index = sorted(range(len(xs)), key=xs.__getitem__)
    index_to_rank = [0] * len(xs)
    for rank, i in enumerate(rank_to_index):
        index_to_rank[i] = rank
    return rank_to_index, index_to_rank


def solve1(wires):
    """O(N^2) brute-force solution (timing: 5.1s)."""
    N = len(wires)
    # the following brute-force solution runs in O(N^2) time for N wires
    return sum(
        cmp(wires[i][0], wires[j][0]) != cmp(wires[i][1], wires[j][1])
        for i in range(N)
        for j in range(i)
    )


def solve2(wires):
    """O(N^2) brute-force solution (timing: 5.6s)."""
    N = len(wires)
    # the following brute-force solution runs in O(N^2) time for N wires
    return sum(
        wires[i][0] < wires[j][0] and wires[i][1] > wires[j][1]
        for i in range(N)
        for j in range(N)
    )


def read_problems(lines):
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)


def read_problem(lines):
    N = int(next(lines))
    return [tuple(map(int, lines.next().split())) for _ in range(N)]


if __name__ == "__main__":
    main()
