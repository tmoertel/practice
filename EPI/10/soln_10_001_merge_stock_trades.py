#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-11-15

"""Solution to "Mege Stock Trades" problem, EPI 10.1.

"Problem 8.1: Design an algorithm that takes a set of files containing
stock trades sorted by increasing trade times, and writes a single
file containing the trades appearing in the individual files sorted in
the same order. The algorithm should use very little RAM, ideally of
the order of a few kilobytes."  Source: _Elements of Programming
Interviews_.

Discussion.  Assume for simplicity that each of the trades is given by
a string of the form "TS XYZ" where TS is a timestamp and XYZ is
trade-related data that, for this problem, can be considered satellite
data.  Further assume that the timestamps have been written in such a
way that sorting the lines lexicographically puts them into time
order.  Thus the problem, boiled to its essence, is that of merging
the already-sorted lines of a given set of files.

In Python, the heapq module's merge function already merges sorted
sequences efficiently, so the solution can be expressed as simply as
follows:

    def merge_files(infiles, outfile):
        with open(outfile, 'w') as f:
            f.writelines(heapq.merge(*map(open, infiles)))

But let's pretend that heapq.merge did not exist and that we had to
use basic min-heap operations to do the work ourselves.

So, starting at the very beginning: How do we find the first line to
output?  One idea is to open all of the input files and throw their
first lines into a heap.  Then, if we extract the minimum value from
the heap, we will have found the globally minimum line, which can then
be emitted as the first line of output.  What about the next line?
The same logic applies, once we insert into the heap the next line
from the file that contributed the first line.  So we can continue in
this fashion -- extracting from the heap the minimum line and emitting
it, inserting into the heap the next line from the file that
contributed the just-emitted line -- until all of the files and,
finally, the heap itself are exhausted.  At this point, all of the
input lines will have been emitted and, since they were each emitted
in sorted order, the output as a whole will have been sorted.

To make this solution more reusable, I've generalized from files to
iterators over any orderable values.  To allow these iterators to be
ordered in the heap, I convert them into streams, which expose the
iterators' next values.  (For more on streams, see [1].)  Using
streams, implementing the logic described in the preceding paragraph
becomes straightforward (see the merge_iterators function).

Performance.  To merge M iterators containing N lines, this algorithm
requires space of size O(M) for the heap.  It also requires O(N)
operations over this heap, each of time O(log M), resulting in an
overall run time of O(N * log M).


Refs:  [1]  http://blog.moertel.com/posts/2013-05-26-python-lazy-merge.html

"""

from heapq import heapify, heappop, heappush


def merge_iters(iters):
    """Merge a series of sorted iterators into a single sorted iterator."""
    streams = [_f for _f in map(iter_to_stream, list(map(iter, iters))) if _f]
    heapify(streams)
    while streams:
        stream = heappop(streams)
        x, stream = stream_next(stream)
        if stream:
            heappush(streams, stream)
        yield x


# Stream abstraction.


def iter_to_stream(iter):
    """Converts an iterator to a stream, which exposes its next value."""
    # Stream ::= None | (value, (iterator_id, iterator))
    #
    # We use the iterator_id as a tiebreaker so that, when two streams
    # are compared, if their values are the same, we are guaranteed to
    # break the tie on their iterator_ids, preventing Python from trying
    # to compare the following iterators (which causes an error since '<'
    # is not defined on list iterators.)
    try:
        return next(iter), (id(iter), iter)
    except StopIteration:
        None  # = empty stream


def stream_next(stream):
    x, (_, iter) = stream
    return x, iter_to_stream(iter)


# Take set of files to merge from the command line.
def main():
    import sys

    in_iters = list(map(open, sys.argv[1:]))
    sys.stdout.writelines(merge_iters(in_iters))


if __name__ == "__main__":
    main()
