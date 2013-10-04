#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-10-01

"""Find the maximum weight path of a directed graph.

Consider the following problem offered at CareerCup:

    Given a weighted directed graph with n vertices where edge weights are
    integers (positive, zero, or negative), determining whether there are
    paths of arbitrarily large weight can be performed in time

    (a) O(n)
    (b) O(n log(n)) but not O(n)
    (c) O(n^1.5) but not O(n log n)
    (d) O(n^3) but not O(n^1.5)
    (e) O(2^n) but not O(n^3)

    Source: http://www.careercup.com/question?id=6111168305299456

That is, given some weight W, is there some path whose weight is at
least W?

A first try at solving the problem might be to think of a direct
recursive approach.  For each vertex v, see if it starts a path that's
weighty enough.  This we do by visiting each of v's neighbors u having
a connecting edge of weight w and asking if there's a path from u that
exceeds W - w, proceeding recursively until we have an answer, and
stopping with the base case that the answer is true for all W <= 0.
This algorithm has some problems, however.  First, it's inefficient,
since nothing prevents it from revisiting vertices.  Second, it can
get stuck in the graph's cycles, forever if they have negative weight!

So let's try a different approach: find the maximum-weight path in the
graph and see if its weight is at least W.  Let m(v) be the maximum
weight of any path starting at v.  Then we have the recurrence

    m(v) = max {w + m(u) | (u, w) in weighted_neighbors(v)}
           (or 0 if v has no neighbors)

Assuming the graph has no cycles, we can compute m(v) for all vertices
v in linear time.  Just sort the graph topologically and visit the
vertices in reverse sorted order.  That way, when we reach a node v,
we will already know m(u) for all its neighbors u.

But if the graph has cycles?  In that case, each cycle must have a net
positive weight or not.  If it does, we can follow it forever to make
a path of infinite weight.  Thus once we find one such cycle, we can
stop because we'll know our answer: the maximum path weight goes to
infinity.  If the cycle weight isn't positive, following the cycle
will always make a path of weight <= 0, and we can ignore it, as a
0-length path is a trivial alternative that's at least as weighty.

Detecting cycles can be done in linear time using the same depth-first
search that we use to order the vertices topologically.  A cycle
occurs iff we encounter a back edge during the DFS.  To determine net
cycle weights, we can keep a running total of path weight as we
search.  As we encounter each new node v, we remember the current
running total as r[v].  Later, if we discover a back edge to v, we can
subtract r[v] from the new running total to compute the net weight of
the cycle.

Combining these ideas gives us a linear-time algorithm to find a
graph's maximum path weight and, consequently, answer the original
question.  Proof: For a graph G = (V, E), the max_path_weight
algorithm opens each vertex v only once and explores v's edges only at
the time v is opened.  Thus each vertex and each edge is explored at
most once, and since the work done for each is O(1), the overall
running time is given by O(|V| + |E|).

"""

import itertools

def has_path_meeting_bound(G, W):
    """Test whether a graph G has a path of weight >= W."""
    try:
        return max_path_weight(G) >= W
    except PositiveWeightCycle:
        return True

def max_path_weight(G):
    """Find weight of maximum-weight path in G.

    Raises PositiveWeightCycle if G contains a positive-weight cycle,
    giving rise to an infinite-weight path.

    """
    max_from_vert = {}
    opening_running_total = {}
    def dfs(v, running_total=0):
        if v in max_from_vert:
            return max_from_vert[v]  # v is closed
        if v in opening_running_total:
            # v open but not closed: found back edge and therefore a cycle
            if running_total - opening_running_total[v] > 0:
                raise PositiveWeightCycle()
            return 0  # non-positive cycle is dominated by 0-length path
        # v hasn't been visited: open it and explore its neighbors
        opening_running_total[v] = running_total
        max_from_vert[v] = zmax(w + dfs(u, running_total + w) for u, w in G[v])
        return max_from_vert[v]
    return zmax(dfs(v) for v in G)

class PositiveWeightCycle(Exception):
    """Signals that a graph has an positive-weight cycle."""

def zmax(xs):
    """Return max of sequence, with 0 as lower bound."""
    return max(itertools.chain([0], xs))

def test():
    from nose.tools import assert_equals as eq
    from nose.tools import raises
    eq(max_path_weight({}), 0)
    eq(max_path_weight({1: []}), 0)
    eq(max_path_weight({1: [(1, 0)]}), 0)  # 0-weight cycle
    eq(max_path_weight({1: [(1, -1)]}), 0)  # neg-weight cycle
    raises(PositiveWeightCycle)(max_path_weight)({1: [(1, 1)]})
    eq(max_path_weight({1: [(2, 1)], 2: []}), 1)
    eq(max_path_weight({1: [(2, 1)], 2: [(1, -1)]}), 1)
    return 'ok'
