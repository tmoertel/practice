#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-13


"""Solution to "Treasure" Code Jam problem
https://code.google.com/codejam/contest/2270488/dashboard#s=p3

"""

from collections import Counter, defaultdict
import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %s' % (i, s)

def solve(problem):
    K, _N, starting_keys, chests = problem

    keys_in_chest = dict((i, keys_i) for i, (_, keys_i) in chests.iteritems())

    chests_unlocked_by = defaultdict(set)
    key_debt = Counter()
    for i, (T_i, _) in chests.iteritems():
        chests_unlocked_by[T_i].add(i)
        key_debt[T_i] += 1

    chests = set(chests)
    keys = Counter(starting_keys)

    def search(keys, key_debt, chests, seq):
        print '%ssearch(seq=%r, keys=%r, debt=%r, chests=%r)' % (
            ' ' * len(seq), seq, keys, key_debt, chests)
        if not chests:
            return seq
        for key in keys:
            for chest in sorted(chests & chests_unlocked_by[key]):
                if key in keys_in_chest[chest] or keys[key] >= key_debt[key]:
                    soln = search(keys - Counter([key]) + keys_in_chest[chest],
                                  key_debt - Counter([key]),
                                  chests - set([chest]),
                                  seq + [chest])
                    if soln is not None:
                        return soln

    soln = search(keys, key_debt, chests, [])

    if soln is None:
        return 'IMPOSSIBLE'
    return ' '.join(str(i) for i in soln)


def selections(xs):
    for i, x in enumerate(xs):
        yield x, xs[:i] + xs[i+1:]



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
        keys_i = Counter(ints[2:])
        return T_i, keys_i
    chests = dict((i, read_chest()) for i in xrange(1, N + 1))
    return K, N, starting_keys, chests

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
