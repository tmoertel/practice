#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-13


"""Solution to "Treasure" Code Jam problem
https://code.google.com/codejam/contest/2270488/dashboard#s=p3

"""

from bisect import bisect_left
import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %s' % (i, s)

def solve(problem):
    K, N, starting_keys, chests = problem

    def search(keys, locked_chests, seq):
        if not locked_chests:
            return seq
        if not keys:
            return None
        for i in locked_chests:
            unlock_key, keys_i = chests[i]
            k = bisect_left(keys, unlock_key)
            if k != len(keys) and keys[k] == unlock_key:
                soln = search(sorted(keys_i + keys[:k] + keys[k+1:]),
                              [j for j in locked_chests if j != i],
                              seq + [i])
                if soln is not None:
                    return soln

    soln = search(starting_keys, sorted(chests), [])

    if soln is None:
        return 'IMPOSSIBLE'
    return ' '.join(str(i) for i in soln)



def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    K, N = read_ints(lines)
    starting_keys = sorted(read_ints(lines))
    def read_chest():
        ints = read_ints(lines)
        T_i, _K_i = ints[:2]
        keys_i = sorted(ints[2:])
        return T_i, keys_i
    chests = dict((i, read_chest()) for i in xrange(1, N + 1))
    return K, N, starting_keys, chests

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
