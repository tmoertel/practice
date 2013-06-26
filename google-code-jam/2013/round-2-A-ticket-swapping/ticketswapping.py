#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-06-25

"""Solution to "Ticket Swapping" Code Jam problem
https://code.google.com/codejam/contest/2442487/dashboard

As a first stab at solving the problem, think about a single
passenger.  When an exiting customer swaps to get the card that
minimizes his fee, the customer on the other end of that swap ends up
with a card that increases her fee.  Is the benefit to him greater
than the cost to her?

To answer this question, let us think about how fees are calculated.
On a subway line of N stations, the fee for presenting a card that
claims a ride of i segments is

    p(i) = i * N - (i * (i + 1) / 2).

Consider p over the full range of ride lengths 0 <= i < N. As i
increases, the first term in p(i) increases by N but the second term
decreases by (i + 1) / 2.  Since i < N, the first term dominates, and
p(i) is strictly increasing.

When an exiting customer swaps his card to get a non-exiting
customer's more-recently taken card, his apparent ride is reduced and
hers extended.  If his ticket was taken at stop i and hers at stop
j > i, and if he is exiting now at stop e and she later at f > e,
they would have paid in total

    p(e - i) + p(f - j).           (1a)

But, after swapping, they will instead pay

    p(e - j) + p(f - i).           (1b)

Letting g = f - e and k = j - i and h = e - j, we can rewrite the
fees to better see the effect of the swap:

    {- no swap -}
    p(e - i) + p(f - j)
    p(e - j + k) + p(e + g - j)
    p(h + k) + p(h + g).           (2a)

    {- swap -}
    p(e - j) + p(f - i)
  = p(h) + p((g + e) + (k - j))
  = p(h) + p((e - j) + (g + k))
  = p(h) + p(h + (g + k))
  = p(h) + p((h + g) + k)          (2b)

Comparing (2a) to the swapping total (2b), we see that the effect, as
expected, is to reduce the first rider's apparent ride by k segments
and to extend the second's by the same amount.  But *where* along the
fare spectrum each passenger's reduction or extension has its effect
is different.

The fare effect at point h is q(h) = p(h + k) - p(h).  Since p grows
more slowly with h for larger values of h, the growth in the -p(h)
term dominates p(h + k), and q(h) is strictly decreasing.

Using q to express the total loss to the city from the card swap, we
arrive at the formula

    (total loss caused by swap) = q(h) - q(h + g).

Since q is strictly decreasing and g > 0, we have q(h) > q(h + g) for
all h.  Therefore, first customer's gain always exceeds the second
customer's loss and, together, their card swap results in an
additional loss for the city.

This result suggests that we can greedily apply the same swapping
strategy for all customers to arrive at a maximal loss for the city.
Can we prove that the greedy strategy works?

We proceed by contradiction.  Assume that when all passengers follow
the strategy the city does *not* experience a maximal loss.  Since the
only thing that can affect the city's loss is ticket swaps between
people exiting at different stops, there must be some additional swap
that can be performed to increase the city's loss further.

Let this swap occur between a passenger exiting at e and holding a
card from j and a passenger exiting later at f and holding a card from
i.  Since up until now the passengers were following our strategy, we
know that j >= i.  Further, for the swap to have any effect, i and j
can't be the same, so we know j > i.  Therefore, this swap will cause
the first passenger to receive a card taken at an earlier stop and the
second to receive a card taken at a later stop.

But, in that case, these customers could swap cards a second time,
using our normal greedy strategy to increase the city's loss even
more.  But swapping twice is equivalent to not swapping at all!
Therefore the effect of the first swap must be the opposite of our
normal swap: it must actually *decrease* the city's loss.  This
contradicts our assumption a loss-increasing swap was available.
Therefore, the greedy swapping strategy cannot be improved upon and
results in a maximal loss for the city.

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

    # split journeys into a series enter and exit events
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
