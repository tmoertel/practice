#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-03-31


"""Solution to "Milkshakes" problem
http://code.google.com/codejam/contest/32016/dashboard#s=p1

Note that this problem is equivalent to the following binary
integer programming problem:

Let:  i         = 1, 2, ... #Flavors
      j         = 1, 2, ... #Customers
      k         = {0 = unmalted, 1 = malted}
      m_i       = 1 if batch for flavor i is to be malted; else 0
      p_{i,j,k} = 1 if customer j likes flavor i with malt status k; else 0

Minimize sum_i{m_i}
s.t.     forall j. sum_i{p_{i,j,{m_i}}} > 0


m_1 - m_2 > -1

"""



import collections
import fileinput
import sys


Problem = collections.namedtuple('Problem', 'n_flavors n_customers cust_prefs')


def main():
    sys.setrecursionlimit(2000)
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %s' % (i, s)


def solve(problem):
    N, M, cust_faves = problem

    max_cust_flavors = collections.defaultdict(int)
    for cust, shakes in cust_faves.iteritems():
        for flavor, _ in shakes:
            max_cust_flavors[cust] = max(max_cust_flavors[cust], flavor)

    def search(n, malts, unsatisfied_custs):
        if len(malts) > malt_max or len(malts) + N - n < malt_max:
            return None
        if not unsatisfied_custs:
            return malts
        if any(n > max_cust_flavors[cust] for cust in unsatisfied_custs):
            return None
        nomalt_satisfied_custs = set()
        malt_satisfied_custs = set()
        for cust in unsatisfied_custs:
            if (n, False) in cust_faves[cust]:
                nomalt_satisfied_custs.add(cust)
            if (n, True) in cust_faves[cust]:
                malt_satisfied_custs.add(cust)
        soln = search(n + 1, malts, unsatisfied_custs - nomalt_satisfied_custs)
        if soln is not None:
            return soln
        return search(n + 1, malts.union(set([n])),
                      unsatisfied_custs - malt_satisfied_custs)

    malts = search(1, set(), set(xrange(M)))
    if malts is not None:
        return ' '.join(str(int(flavor in malts)) for flavor in xrange(1, N+1))
    return 'IMPOSSIBLE'


def read_problems(lines):
    C = int(lines.next())
    for _ in xrange(C):
        yield read_problem(lines)


def read_problem(lines):
    N = int(lines.next())  # flavor count
    M = int(lines.next())  # customer count
    cust_faves = read_cust_faves(M, lines)
    return N, M, cust_faves


def read_cust_faves(M, lines):
    faves = collections.defaultdict(set)
    for cust in xrange(M):
        pref_spec = map(int, lines.next().split())
        T = pref_spec.pop(0)
        spec_items = iter(pref_spec)
        for _ in xrange(T):
            faves[cust].add((spec_items.next(), bool(spec_items.next())))
    return faves


if __name__ == '__main__':
    main()
