#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2016-05-31

"""Solution to "BFFs" Code Jam problem
https://code.google.com/codejam/contest/4304486/dashboard#s=p2

Discussion.

Think of the class as a directed graph in which each student is a node
having a single outgoing edge to its BFF. If we start at any node and
follow edges, we must eventually visit a node we've already
visited. (This follows from the number of students being finite:
eventually we'll run out of students we haven't visited before.)
Therefore, every student is part of a BFF chain, and all BFF chains
terminate in a cycle.

Since a cycle is a circle, any cycle is a potential solution. And
since cycles of length two have the property that they have no
"width," any chain that ends in a 2-cycle can be arranged in a
circle. In fact, any *two* chains that terminate in the same 2-cycle
but enter the 2-cycle in opposite nodes can also be arranged in a
circle. Further, any number of these chain-augmented 2-cycles can be
arranged in a circle. These properties do not hold for larger
cycles. (They would result in circles with cycle "warts" attached.)
Therefore, a solution must take one of two forms: (1) one or more
chain-augmented 2-cycles, or (2) a single cycle of length > 2.

Thus we can solve the problem by finding cycles and augmenting the
nodes of any 2-cycles with the longest incoming chain each node
accepts. Then we just select the largest potential solution: the
sum of the sizes of the chain-augmented 2-cycles or the largest
cycle of length > 2.

Implementation.

To find cycles, we can use a depth-first search over the graph, as
we would for a topological sort. To find the longest BFF chains that
terminate into the nodes of 2-cycles, we can simply do another
depth-first search, this time over a reversed-edge version of the
graph in which we've removed the cycle-forming edges. We'll use this
DFS to find the depths of the trees rooted in the nodes of the
2-cycles we identified. (These weakly-connected components must be
trees since we've removed the sole cycle in each.) The depths will
be the same as the lengths of the longest BFF chains into the same
nodes in the original graph.

Efficiency.

For a problem with N students, this implementation will return a
solution in O(N) time and space. (Our algorithm boils down to two
whole-graph depth-first searches, and thus has the same costs.)

"""

import fileinput
import sys

def main():
    # The max problem size is N=1000, which is at the default
    # Python recursion limit, so we raise the limit.
    sys.setrecursionlimit(2000)
    # Read the problems, solve them, and print the solutions.
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %r' % (i, s)

def solve(problem):
    N, bffs = problem
    # Construct BFF graph and find its cycles.
    G = graph_from_edges(enumerate(bffs, 1))
    cycles = find_cycles(G)
    # Construct reverse-edged graph and scan its cycles.
    G_reverse = graph_from_edges((j, i) for i, j in enumerate(bffs, 1))
    max_large_cycle_size = sum_of_2_cycle_sizes = 0
    for size, entry_node in cycles:
        if size == 2:
            # Remove the 2-cycle's edges so that each cycle node roots a tree.
            second_node = list(G[entry_node])[0]
            G_reverse[entry_node].remove(second_node)
            G_reverse[second_node].remove(entry_node)
            # Add the depth of each tree to the augmented cycle's size.
            size += tree_depth(G_reverse, entry_node)
            size += tree_depth(G_reverse, second_node)
            sum_of_2_cycle_sizes += size
        else:
            max_large_cycle_size = max(max_large_cycle_size, size)
    return max(sum_of_2_cycle_sizes, max_large_cycle_size)

def graph_from_edges(edges):
    G = {}
    for i, j in edges:
        G.setdefault(i, set()).add(j)
        G.setdefault(j, set())
    return G

def find_cycles(G):
    opened = {}
    closed = set()
    cycles = []
    def dfs(i, depth=0):
        if i in closed:
            return
        if i in opened:
            cycles.append((depth - opened[i], i))
            return
        opened[i] = depth
        for j in G[i]:
            dfs(j, depth + 1)
        closed.add(i)
    for i in G:
        dfs(i)
    return cycles

# ASSUMES that the subgraph of G rooted in node i is a tree.
def tree_depth(G, i):
    max_depth = [0]
    def dfs(i, depth=0):
        max_depth[0] = max(max_depth[0], depth)
        for j in G[i]:
            dfs(j, depth + 1)
    dfs(i)
    return max_depth[0]

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    N, = read_ints(lines)
    bffs = read_ints(lines)
    return N, bffs

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
