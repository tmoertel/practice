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
    fave_custs = collections.defaultdict(set)
    for c, faves in problem.cust_prefs.items():
        for fave in faves:
            fave_custs[fave].add(c)
    wanted_malts = set(shake for shake, is_malted in fave_custs if is_malted)

    def all_satisfied(malts):
        return all(any(is_malted == (1 if shake in malts else 0)
                       for shake, is_malted in faves)
                   for faves in problem.cust.prevs.iteritems())

    lo = 0
    hi = [len(wanted_malts)]

    def search(shake, malts):
        if all_satisfied(malts):
            return malts



    if soln is None:
        return "IMPOSSIBLE"
    return ' '.join(str(is_malt) for is_malt in soln[1])



def read_problems(lines):
    N = int(lines.next())
    for _ in xrange(N):
        yield read_problem(lines)


def read_problem(lines):
    n_flavors = int(lines.next())
    n_customers = int(lines.next())
    cust_prefs = read_cust_prefs(n_customers, lines)
    return Problem(n_flavors, n_customers, cust_prefs)


def read_cust_prefs(n_customers, lines):
    prefs = {}
    for c in xrange(1, n_customers + 1):
        cust_pref = set()
        prefs[c] = cust_pref
        pref_spec = map(int, lines.next().split())
        T = pref_spec.pop(0)
        spec_items = iter(pref_spec)
        for _ in xrange(T):
            cust_pref.add((spec_items.next(), spec_items.next()))
    return prefs


if __name__ == '__main__':
    main()
