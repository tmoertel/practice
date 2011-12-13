#!/usr/bin/env python
# Tom Moertel <tom@moertel.org>
# 2011-12-12

"""Solve a simple binary-search-tree exercise.

Problem:

    Given a binary search tree, write code to find a particular
    value.  If you can't find the value, then return me the next
    smallest value.  For example, if the tree contains 1, 2, 3, and 5,
    and I ask for 4, then return 3.

    Source:  http://news.ycombinator.com/item?id=3339418

"""


"""
Claim: find_min(bst, val, next_smallest) returns val if it exists in
the binary search tree bst or, failing that, the next smallest value
in bst or, failing that, next_smallest, assuming next_smallest <=
min(bst).  (Note:  We let None be the smallest possible value.)

Proof:  We proceed by induction on the height of the tree.  Assume we
know that find_min(bst, val, next_smallest) is correct for height(bst)
= N && next_smallest < val && next_smallest <= min(bst).

Base case:  height(bst) = 0.  Trivially correct:  next_smallest.

Now we try height(bst) = N + 1.  There are three cases:

Case 1:  val == bst.val.  Here we return val, which is obviously correct.

Case 2:  val < bst.val.  Here we know that bst.val > val and cannot be
a match or even the next-smallest match.  Therefore, find_min of the left
subtree must be the same as of the whole tree bst:

   find_min(bst, val, next_smallest) = find_min(bst.left, val, next_smallest).

Since next_smallest <= min(bst) <= min(bst.left), our induction hypothesis
still holds.

Case 3: val > bst.val.  Here we know that bst.val < val and cannot be
a match, but it must be an improved next-smallest match, since it's
smaller than val and yet it is at least as large as min(bst), which is
at least as large as our current best next_smallest.  Therefore,
find_min of the right subtree with the improved next_smallest must be
the same as the original call:

   find_min(bst, val, next_smallest) = find_min(bst.right, val, bst.val).

Again, since bst.val <= bst.right, our induction hypothesis still holds.

Q.E.D.

"""

def find_min(bst, val, next_smallest=None):
    if bst is None:
        return next_smallest
    elif val == bst.val:
        return val
    elif val < bst.val:
        return find_min(bst.left, val, next_smallest=next_smallest)
    else:
        return find_min(bst.right, val, next_smallest=bst.val)


def find_min_iterative(bst, val, next_smallest=None):
    while True:
        if bst is None:
            return next_smallest
        elif val == bst.val:
            return val
        elif val < bst.val:
            bst = bst.left
        else:
            bst = bst.right
            next_smallest = bst.val

def find_min_iterative2(bst, val, next_smallest=None):
    while bst is not None:
        if val == bst.val:
            return val
        elif val < bst.val:
            bst = bst.left
        else:
            bst = bst.right
            next_smallest = bst.val
    return next_smallest
