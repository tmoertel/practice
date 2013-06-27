#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-06-25

"""Solution to "Ticket Swapping" Code Jam problem
https://code.google.com/codejam/contest/2442487/dashboard

Since all passengers must enter and exit at their normal stops, the
only thing that can affect the city's loss is swapping entry cards.
For a swap to have any effect, it must be between people exiting at
different stops and for cards obtained at different stops.

To understand the effect of swaps, let us consider the usual fare for
traveling i segments on a subway line of N stations:

    p(i) = i * N - (i * (i + 1) / 2),    0 <= i < N.

As i increases, the first term in p(i) increases by N but the second
term decreases by (i + 1) / 2.  Since i < N, the first term dominates,
and p(i) is strictly increasing.

Now consider what happens when an exiting passenger swaps his card to
get a non-exiting passenger's more-recently taken card.  If his ticket
was taken at stop i and hers at stop j > i, and if he is exiting now
at stop e and she later at f > e, they would have paid in total

    p(e - i) + p(f - j).           (1a)

But, after swapping, they will instead pay

    p(e - j) + p(f - i).           (1b)

Letting g = f - e and k = j - i and h = e - j, we can rewrite the
fees to see the effect of the swap:

    {- no swap -}
    p(e - i) + p(f - j)
  = p(e - j + k) + p(e + g - j)
  = p(h + k) + p(h + g).           (2a)

    {- swap -}
    p(e - j) + p(f - i)
  = p(h) + p((e + g) + (k - j))
  = p(h) + p((e - j + g) + k)
  = p(h) + p((h + g) + k)          (2b)

Comparing (2a) to the swapping total (2b), we see that the effect is
to reduce the first rider's apparent ride by k segments and to extend
the second's by the same amount but at g > 0 segments farther into the
fare schedule, where changes have diminished effect.  Letting

    q(h) = p(h + k) - p(h),

the additional loss to the city, (2a) - (2b), can be written

    q(h) - q(h + g).

Since p(h) grows more slowly with h for larger values of h, the growth
of -p(h) dominates the growth of p(h + k) in q(h), and q(h) is
strictly decreasing.  Therefore, q(h) > q(h + g) for all h, and a swap
of this kind always results in an additional loss for the city.
Further, the larger k = j - i is, the larger the loss.

This result suggests that we can apply a greedy strategy to maximize
the city's loss:  Before exiting, each passenger swaps to obtain the
most-recently obtained entry card available, including cards from
people entering at the same stop.

Can we prove that this strategy leads to a maximal loss for the city?
We proceed by contradiction.  Assume that the strategy does *not*
cause a maximal loss.  Since the only thing that can affect the loss
is ticket swaps, there must be some additional swap that can be
performed to increase the city's loss.

Let this swap occur between a passenger exiting at e and holding a
card from j and a passenger exiting later at f and holding a card from
a different stop i.  Since up until now the passengers were following
our strategy, we know that j > i.  Therefore, this new swap will cause
the first passenger to receive the card taken at i and the second to
receive the card taken at j.

But, after the swap, these two passengers will satisfy the conditions
for our normal swapping strategy to be effective.  So they should swap
cards a second time to further increase the city's loss.  But swapping
twice is equivalent to not swapping at all!  Therefore the first and
second swaps must have had inverse effects.  Since we know the second
swap must have increased the city's loss -- we've already proved it --
the first must have actually *decreased* the city's loss.  But this
contradicts our assumption a loss-increasing swap was available.
Therefore, the loss caused our greedy strategy must have been maximal
to begin with, and our proof is complete.

"""

import fileinput
from heapq import heappush, heappop

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %d' % (i, s)

def solve(problem):
    N, journeys = problem

    def price(stops):
        """Compute the price of traveling a number of stops."""
        return stops * N - stops * (stops + 1) // 2

    # split journeys into a series of enter and exit events
    events = []
    for origin, end, passenger_count in journeys:
        # order entry events before exit events to ensure that they
        # are processed first when both types occur at the same stop
        heappush(events, (origin, 0, end, passenger_count))
        heappush(events, (end, 1, origin, passenger_count))

    # process events in order, enforcing the maximum-loss policy:
    # each rider must exit with the most-recently-obtained card left
    loss = 0
    most_recent_cards = []
    while events:
        i, is_exit, j, passenger_count = heappop(events)
        if not is_exit:
            # passengers enter at station i, destined for station j
            most_recent_cards.append((i, j, passenger_count))
        else:
            # passengers exit at station i, having entered from station j
            while passenger_count > 0:
                c_entry, c_exit, c_count = most_recent_cards.pop()
                affected_count = min(passenger_count, c_count)
                passenger_count -= affected_count
                c_count -= affected_count
                if c_count > 0:
                    most_recent_cards.append((c_entry, c_exit, c_count))
                loss_per_person = price(i - j) - price(i - c_entry)
                loss = (loss + affected_count * loss_per_person) % 1000002013

    return loss

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    N, M = read_ints(lines)
    journeys = [read_ints(lines) for _ in xrange(M)]
    return N, journeys

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
