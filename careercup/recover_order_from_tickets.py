#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-11-07

"""Solution to the following problem:

    You visited a list of [cities] recently, but you do not remember
    the order in which you visited them.  You have with you the
    airplane tickets that you used for traveling.  Each ticket
    contains just the [departure city] and the [arrival city for one
    leg of your journey]. Can you reconstruct your journey?

    Source: http://www.careercup.com/question?id=5072902038749184

Discussion.

Each airline ticket reveals that you traveled from a source city A to
a destination city B.  In other words, it's an edge A -> B in a directed
graph in which vertices are cities and edges are legs of your journey.
Consequently, placing the vertices in topological order reveals the
original order in which you visited the cities.

The following code uses this logic to solve the problem.  It first
computes the directed graph G induced by the tickets.  Then it orders
G's vertices topologically and returns this order as the solution.

I represent a ticket from city A to city B by the ordered pair (A, B).
Cities can be represented by any type that can be used for dictionary
keys.  In my testing code, I used integers but you could just as well
use airport-code strings like "PIT" and "SFO".

To represent a graph in Python, I use the classic adjacency-list
representation:  A dict G maps each vertex (= city) to a list of its
neighboring vertices:

            G
    vertex :-> [vertex]

As for efficiency, this solution consumes O(N) time and space to solve
a problem comprising N tickets.  This can be seen from the following
observations:  In a well-formed journey between N + 1 cities, there
must be exactly N tickets, and each ticket gives rise to one edge in
the graph.  Thus the graph has |V| = N + 1 vertices and |E| = N edges.
The function ticket_graph runs in O(|E|) = O(N) time and produces a
graph of size O(|V| + |E|) = O(N).  The topo_sort function opens each
vertex at most once and, at that time, examines each of its edges
once, doing O(1) work.  Thus its overall running time is O(|V| + |E|)
= O(N).  The function uses O(|V|) space for the ordering list and seen
set and may consume O(|E|) stack space during recursion.  Thus overall
space use is again O(|V| + |E|) = O(N).

"""

from collections import defaultdict

def recover_order(tickets):
    """From airline tickets, recover order in which the cities were visited."""
    G = ticket_graph(tickets)
    ordering = topo_sort(G)
    return list(ordering)

def ticket_graph(tickets):
    """Create graph induced by a set of airline tickets (= edges)."""
    G = defaultdict(list)
    for src, dest in tickets:
        G[src].append(dest)
        G[dest]  # make sure dest vertex exists in graph
    return G

def topo_sort(G):
    """Return vertices of graph in topological order."""
    ordering = []
    seen = set()
    def dfs(v):
        if v in seen:
            return
        seen.add(v)
        for u in G[v]:
            dfs(u)
        ordering.append(v)
    for v in G:
        dfs(v)
    return reversed(ordering)


# tests

def test():

    from itertools import permutations
    from random import sample
    from nose.tools import assert_equal as eq

    max_cities = 10  # test all journeys up to 10 cities in length

    for n in xrange(max_cities):

        if n == 1:
            continue  # can't have any flights between just 1 city

        city_ordering = sample(xrange(n), n)  # a random n-city ordering
        tickets = zip(city_ordering[:-1], city_ordering[1:])

        # for all ticket orderings, we must recover the original city ordering
        for shuffled_tickets in permutations(tickets):
            eq(recover_order(shuffled_tickets), city_ordering)
