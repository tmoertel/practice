#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-11-15

"""Solution to "Anonymous Letter" EPI problem

"Problem 12.9 : You are required to write a method which takes an
anonymous letter L and text from a magazine M.  Your method is to
return true iff L can be written using M, i.e., if a letter appears k
times in L, it must appear at least k times in M."  Source: _Elements
of Programming Interviews_.

Discussion.  To write the anonymous letter L, we need to take its
constituent characters from the magazine M.  Thus we can write the
letter only if there are enough instances of each needed letter in the
magazine -- in other words, only if L is a "subdocument" of M.  More
formally, if we let c_D(x) denote the count of occurrences of the
letter x in the document D, we can write the letter iff, forall x in
L, c_L(x) <= c_M(x).  To keep track of the counts, we can use a map
from characters to counts.  Fortunately, the Python collections module
provides a Counter class tailored to this purpose.

More discussion.  After writing the solution I give below, I looked at
the book's suggested solution.  The authors suggest the following
approach, which eliminates one of the maps, and which I have recast
into Python for parity with my solution:

    def is_subdocument(L, M):
        # count char instances in L
        counts_L = Counter(L)
        # for each char instance in M, subtract it from counts_L
        for x in M:
            if x in counts_L:
                counts_L[x] -= 1
                if not counts_L[x]:
                    del counts_L[x]
        # if all of the counts for L have been reduced
        # to 0, then L is a subdocument of M
        return not counts_L

I had considered this approach but decided against it because it
destroys the counts.  The counts are a compact document summary that
could be used over and over (for example, if you want to test multiple
letters against multiple magazines).  Keeping them preserves future
opportunities to eliminate the re-scanning of documents.  Destroying
them to purchase a meager halving of the space used, when the space
used is already small, being O(|A|) where A is the alphabet used in
the documents, seems like a poor trade, at least under the
distribution of practical use cases I can imagine.

Of course, whether it is actually a poor trade depends on your actual
distribution of use cases.  If you're standing in front of a white-
board during an interview and told to reduce the memory footprint of
your existing implementation as far as you can, then your set of
potential use cases collapses into the much smaller set of cases in
which space is the primary concern.  Opportunities for reuse still
matter, but not if you must consume space to preserve them.

Anyway, the reason I bring up the authors' suggested approach is to
compare it to mine and show the underlying correspondence between
them.  If you've ever done programming in assembly language, you know
that comparison is basically subtraction.  That is, the test x <= y is
the same as subtracting y from x and checking whether the result is
zero or negative:

    x <= y

      = { subtract y from both sides }

    x - y <= 0

So in my code, I'm basically counting the occurrences of each
character in the document L, then I'm counting the occurrences of
each character in the document M, then for each character x in L,
I'm comparing its count in L to its count in M:

    c_L(x) <= c_M(x)

By using the same subtraction transformation as above, we can recast
the comparison into

    c_L(x) - c_M(x) <= 0.

Now, how did we arrive at c_M(x)?  We scanned through the characters
of M, and when we encountered an instance of x, we added 1 to our
current total for c_M(x).  Thus,

    c_M(x) = sum(1 for each c in M if c == x).

Substituting this formula into our subtraction test, we get

    c_L(x) - sum(1 for c in M if c == x) <= 0.

In other words, every time we encounter an instance of x in M, we are
going to subtract 1 from c_L(x).  So if we decremented the count
c_L(x) on the fly as we scanned M and encountered instances of x, we
would get the equivalent code

    for c in M:
      if c == x:
        c_L(x) -= 1
    return c_L(x) <= 0

For a complete solution, let's apply this approach not just to the
particular character x but for all characters in the alphabet A:

    for x in A:
      for c in M:
        if c == x:
          c_L(x) -= 1
    return all(c_L(x) <= 0 for x in c_L)

But since every character in M is also in A, we know that for all c in
M there exists an x in A such that c == x.  Thus we can eliminate the
outer loop and the corresponding inner if-guard to get the more
efficient code below:

    for x in M:
      c_L(x) -= 1
    return all(c_L(x) <= 0 for x in c_L)

And that's basically the authors' solution.  The only difference is
that they remove the count for x from the c_L dictionary as soon as it
reaches zero.  Then the final test in the return statement simplifies
to just testing whether the c_L dictionary is empty.  If it is, all of
the counts have been reduced to zero or below, and we know that L is a
subdocument of M.

"""

from collections import Counter


def is_subdocument(L, M):
    counts_L = Counter(L)
    counts_M = Counter(M)
    return all(n <= counts_M[x] for x, n in counts_L.items())
