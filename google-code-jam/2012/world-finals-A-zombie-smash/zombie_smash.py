#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-02


"""Solution to "Zombie Smash" Code Jam problem
http://code.google.com/codejam/contest/2075486/dashboard

"""


import fileinput



def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print('Case #%r: %r' % (i, s))


def solve(problem):
    zombies = problem

    def best(x, y, t, smasher_charged):
        return


def read_problems(lines):
    N = int(next(lines))
    for _ in range(N):
        yield read_problem(lines)


def read_problem(lines):
    Z = int(next(lines))
    return [list(map(int, lines.next().split())) for _ in range(Z)]

if __name__ == '__main__':
    main()
