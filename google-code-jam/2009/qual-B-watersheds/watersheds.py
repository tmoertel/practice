#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-02


"""Solution to "Watersheds" Code Jam problem
http://code.google.com/codejam/contest/90101/dashboard#s=p1

"""

import fileinput

# relative position of neighbors, in order of tie-break preference
NEIGHBOR_OFFSETS = [(-1,  0), (0, -1), (0,  1), (1,  0)]

def main():
    for i, (H, W, heights) in enumerate(read_problems(fileinput.input()), 1):
        s = solve(H, W, heights)
        print('Case #%r:\n%s' % (i, s))

def solve(H, W, heights):
    # start w/ cells as singleton sets
    union, find = mk_union_find_domain(heights)

    # merge sets along flows to form basins
    for loc in heights:
        downstream_neighbor, lowest = None, heights[loc]
        for delta in NEIGHBOR_OFFSETS:
            loc1 = loc[0] + delta[0], loc[1] + delta[1]
            if heights.get(loc1, lowest) < lowest:
                downstream_neighbor, lowest = loc1, heights[loc1]
        if downstream_neighbor is not None:
            union(loc, downstream_neighbor)

    # draw map
    labels = {}
    def label(loc):
        return labels.setdefault(find(loc), chr(ord('a') + len(labels)))
    return '\n'.join(' '.join(label((row, col)) for col in range(W))
                     for row in range(H))

def mk_union_find_domain(elems):
    d = dict((e, e) for e in elems)
    def union(u, v):
        d[find(u)] = find(v)
    def find(u):
        urep = d[u]
        if urep != u:
            urep = d[u] = find(urep)
        return urep
    return union, find

def read_problems(lines):
    N = int(next(lines))
    for _ in range(N):
        yield read_problem(lines)

def read_problem(lines):
    H, W = list(map(int, lines.next().split()))
    heights = dict(((row, col), int(s))
                   for row in range(H)
                   for (col, s) in enumerate(lines.next().split()))
    return H, W, heights

if __name__ == '__main__':
    main()
