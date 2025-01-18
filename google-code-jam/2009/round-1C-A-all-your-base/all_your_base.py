#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-09


"""Solution to "All Your Base" Code Jam problem
http://code.google.com/codejam/contest/189252/dashboard#s=p0

"""

import fileinput


def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print("Case #%r: %r" % (i, s))


def solve(message):
    base = max(2, len(set(message)))  # select the least possible base
    digit_sched = [1, 0] + list(range(2, base + 1))  # lowest-possible first
    symbol_vals = {}
    total = 0
    for s in message:
        total *= base
        total += symbol_vals.setdefault(s, digit_sched[len(symbol_vals)])
    return total


def read_problems(lines):
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)


def read_problem(lines):
    return lines.next().strip()


if __name__ == "__main__":
    main()
