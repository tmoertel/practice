#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2018-05-07

'''Solution to "Slides!" Code Jam problem

Problem

Paraphrasing from the official description of the problem [1], you are given
B > 1 buildings, labeled 1..B. Building 1 is the start; building B the end.
Between any two buildings i != j, you may build a single directional slide
from i to j, provided that i is not the end. Your goal is to build slides so
that there are exactly M distinct paths from the start to the end. If you can
reach the goal, print "POSSIBLE" followed by an adjacency matrix specifying
the slides in your solution. Otherwise, print "IMPOSSIBLE".

[1] https://code.google.com/codejam/contest/4314486/dashboard#s=p1


Solution

Let's think of the buildings as vertices in a graph, and the slides as
directed edges. Can we have cycles in the graph? No. If we could, each cycle
would generate an infinite number of distinct paths, and the problem requires
that the total number of paths be exactly M. Therefore the graph is a DAG.

At this point, it's helpful to think about bounding cases to gain intuition
about the problem. It's clear that zero is the fewest paths a graph of B
vertices could have, but what about the most? So: What is the maximum number
of distinct paths we can have from start to end in a DAG of B vertices? Let
F[B] denote this number.

Let's consider F[2], corresponding to the smallest legal problem. In a DAG
with two vertices, one constrained to act as a source (the start building) and
one constrained to act as a sink (the end building), we can add only one edge,
giving rise to a single path. Thus F[2] = 1.

What about F[3]? In this case, we can generate a maximum of two distinct
start-to-end paths. Here's the corresponding graph:

    1 ---> 2 ---> 3     Graph for F[3].
       \______/

The paths are 1 -> 2 -> 3 and 1 -> 3.

What about F[4]? Let's think about this case as starting with the graph for
F[3] and adding a new start vertex -- let's label it 0 -- to the left of the
existing graph:

    0      1 ---> 2 ---> 3     Graph for F[3] augmented with a new start
              \______/

If we add no additional edges to this augmented graph, there would be zero
paths from start to end, since 0 is now the start. But we can add up to
three new edges, 0 -> 1, 0 -> 2, and 0 -> 3. Let's consider each one.

Adding edge 0 -> 1 gives us two paths from start to end (0 -> 1 -> 3 and
0 -> 1 -> 2 -> 3):

    0 ---> 1 ---> 2 ---> 3
              \______/

Adding edge 0 -> 2 gives us one start-to-end path, 0 -> 2 -> 3:
      ___________
     /           \
    0      1 ---> 2 ---> 3
              \______/

Adding edge 0 -> 3 gives us one start-to-end path, 0 -> 3.

    0      1 ---> 2 ---> 3
      \       \______//
       \_____________/

Returning to our earlier question about F[4], we can maximize the number of
paths for this case by adding all three of edges we considered above. Thus
F[4] = 2 + 1 + 1 = 4.

There's a pattern emerging. Whenever we augment an existing maximum-path graph
of size B by adding a new starting vertex, we get a graph of size B+1 that,
initially, has zero paths from start to end (since the new start has no
outgoing edges). But we can add edges from the new start to any of the other
vertices. If we add an edge to the *previous* start, we pick up its F[B]
paths. If we add an edge to the previous previous start, we pick up its F[B-1]
paths. And so on. This trend continues until we add an edge from the new start
directly to the end, creating one new path. So, if we add *all* of these
edges, we get the maximal number of paths, F[B+1]. Thus F[B+1] must equal the
sum of those individual edge's contributions:

    F[B+1] = F[B] + F[B-1] + ... + F[2] + 1.

Let's try to put this formula into a closed form. We can eliminate all but one
of the terms by subtracting the expansion for F[B] from F[B+1]:

   F[B+1]        = F[B] + F[B-1] + ... + F[2] + 1
          - F[B] =      - F[B-1] - ... - F[2] - 1
  -----------------------------------------------
   F[B+1] - F[B] = F[B]

Thus, F[B+1] = 2 F[B]. In other words, successive values of F are increasing
powers of 2:

    F[2] =  1
    F[3] =  2
    F[4] =  4
    F[5] =  8
    F[6] = 16
    .... . ..

Looking at the progression, we can guess that F[B] = 2^(B-2). (It's fairly
obvious that our guess is correct, but we can prove it, if needed, by
induction on B. For the base case, we have F[2] = 1, which we've already
proved. As our induction hypothesis, assume that our guess for F[B] is
correct. Now we will show that it is correct for F[B+1] = 2 * F[B]. By our
induction hypothesis we have F[B+1] = 2 * 2^(B-2). But that's just 2^(B-1),
which we can also write as 2^((B+1)-2). Thus our guess is also correct for
F[B+1]. And that's the proof.)

All of these successive powers of two look very much like a binary numbering
system. This fact suggests a solution to the original Code Jam problem that
allows us to generate exactly M distinct paths, as required.

Say we must solve an instance of the problem for B buildings labeled 1..B.
Start by building a maximal-path solution for the sub-problem formed by
buildings 2..B (considering 2 the new start). We can do this by building up
from smaller maximal-path subgraphs, as we did in our earlier explorations,
but a simpler method is to just build a slide from building i to building j
for all 1 < i < j <= B. (Exercise: Prove that this method gives a maximal-path
solution for the subgraph.)

At this point, the graph for the original problem for buildings 1..B generates
no paths, because we have no slides from building 1, and all legal paths must
start there. But we have the option to build slides from building 1 to any or
all of the other buildings 2..B, which we've just populated with slides. If we
build a slide directly to the end at building B, we gain 1 path from start to
end. If we build a slide to building B-1 we gain F[2] = 1 paths. If we build a
slide to building B-2, we gain F[3] = 2 paths. And so on. If we build slides
to *all* of the other buildings we gain 1 + F[2] + F[3] + ... + F[B-1] = F[B]
paths. (For convenience, let's define F[1] = 1, so that the formula will read
F[1] + F[2] + ... + F[B-1] = F[B].) Thus by choosing which slides to build we
can generate any number of paths M, for M between 1 and F[B] = 2^(B-2),
inclusive.

Unsurprisingly, our implementation for choosing which slides to build is
similar to the logic for representing an natural number in binary with B-1
bits, with the exception that our binary number system has two least-
significant bits to accommodate the fact that F[1] and F[2] both equal 1.

The overall solution, then, is to build slides i -> j for all 1 < i < j <= B
and then build slides 1 -> i for all 1 < i <= B where i corresponds to one of
the bits we need to set. If it turns out we can't represent the given value of
M with the B-1 bits we have available, we know the instance is impossible to
solve. The code below implements this solution.

Our solution has a run time of O(B^2), which is optimal since the problem
statement requires us to output a B*B adjacency matrix, placing a O(B^2) lower
bound on the run time of any solution. Nevertheless, we use only O(B) memory
because we build and output the adjacency matrix one row at a time. (In fact,
we could, in theory, use only O(1) memory since we can compute the first row's
values in a streaming fashion, and the remaining row's values are all given by
the i < j rule. But this approach would make it hard to see the solution's
inner logic, so I opted for clarity instead.)

'''

import fileinput


def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print("Case #{}: ".format(i), end="")
        for line in s:
            print(line)


def solve(problem):
    buildings, needed_paths = problem
    # Start at the most-significant bit and work toward the least,
    # setting each bit needed to represent M = `needed_paths`.
    bits = ["0"] * buildings
    bit_value = 1 if buildings < 3 else 1 << (buildings - 3)
    for building in range(1, buildings):
        if bit_value <= needed_paths:
            bits[building] = "1"
            needed_paths -= bit_value
        bit_value = (bit_value + 1) >> 1
    if needed_paths > 0:
        yield "IMPOSSIBLE"
        return

    # Emit the solution as a streamed series of lines to avoid having
    # to hold the full adjacency matrix in memory.
    def has_edge(i, j):
        if i == 0:
            return bits[j]
        return "1" if i < j else "0"

    yield "POSSIBLE"
    for i in range(buildings):
        yield "".join(has_edge(i, j) for j in range(buildings))


def read_problems(lines):
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)


def read_problem(lines):
    B, M = read_ints(lines)
    return B, M


def read_ints(lines):
    return [int(s) for s in lines.next().split()]


if __name__ == "__main__":
    main()
