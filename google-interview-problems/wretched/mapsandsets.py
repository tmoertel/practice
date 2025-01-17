#!/usr/bin/python

"""Sample solution to the Google interview problem "Maps and Sets,"
described in the blog post http://symbo1ics.com/blog/?p=2055:

    Create a data structure that has fast insertion, removal,
    membership testing, and random selection.

Discussion:

First, I'm allowing values in the data structure to be repeated.  So
we're talking about some kind of bag, not a set.

Second, I'm interpreting "random selection" to mean selecting a random
value, with each value instance in the bag receiving equal probability
of being selected.

Depending on the interpretation of "fast", different options are
available.  If O(log N) operations are considered fast, then a fast
implementation can be constructed as a thin wrapper around a balanced
tree with size-annotated nodes.  The annotations can be used to find
the node at index I in O(log N) time, and thus all the required
operations have simple mappings to O(log N)-time tree operations:

    API                   Tree operations (all O(log N))

    insert             => tree insert + update size annotations
    remove             => tree remove + update size annotations
    membership test    => tree value lookup on given value X
    random selection   => tree index lookup on random index I

If constant-time operations are required, then a suitable data
structure can be built out of simpler data structures.  An array (list
type in Python) offers the constant-time index lookups required for
random selection.  It also offers O(1) inserts and removal from its
end.  But value lookups take O(N) time in an array, so we'll need to
use a hash table (dict type in Python) for membership tests.  Removing
a value X from the array requires that we know its array index, so
we'll need to keep track of these indexes in the hash table, too,
maintaining a set of indexes for each value X.  To remove a value X,
then, we can look up one of its indexes in the hash table, swap the
array's final value into that index's slot, and then shrink the array
by one slot.  This gives us constant-time removal while keeping the
array free of holes, making random selection trivial.  The following
Python code gives one possible implementation.

Tom Moertel <tom@moertel.com>
August 2013

"""

import collections
import random


class GrabBag(object):
    """A bag that supports random selection."""

    def __init__(self):
        self.vals = []  # all values in the bag
        self.val_locs = collections.defaultdict(set)  # each value's indexes

    def insert(self, x):
        self.val_locs[x].add(len(self.vals))
        self.vals.append(x)

    def __contains__(self, x):
        return x in self.val_locs

    def random_val(self):
        if not self.vals:
            raise ValueError("bag is empty")
        return random.choice(self.vals)

    def remove(self, x):
        if x not in self.val_locs:
            raise ValueError("the value is not in the bag")
        # swap x with the final value in the array
        x_loc = self.val_locs[x].pop()  # get an x's loc
        final_loc = len(self.vals) - 1
        if x_loc != final_loc:
            y = self.vals[final_loc]
            self.vals[final_loc] = x
            self.vals[x_loc] = y
            self.val_locs[y].remove(final_loc)
            self.val_locs[y].add(x_loc)
        # truncate the array to remove the final value (now x)
        self.vals.pop()
        # remove x's array-index set if it's empty
        if not self.val_locs[x]:
            del self.val_locs[x]

    def __repr__(self):
        return "GrabBag(vals={}, val_locs={})".format(self.vals, self.val_locs)

