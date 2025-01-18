#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-06-25

"""Solution to "Ticket Swapping" Code Jam problem
https://code.google.com/codejam/contest/2442487/dashboard

The fare for presenting a card that claims i segments of travel on a
subway line of N stations is

    p(i) = i * N - (i * (i + 1) / 2),    0 <= i < N.

As i increases, the first term in p(i) increases by N but the second
term decreases by (i + 1) / 2.  Since i < N, the first term dominates,
and p(i) is strictly increasing (as expected), but the *rate* of the
increase always slows and thus is strictly decreasing.  So the longer
a card is used, the *less* each additional segment charged to it costs.

Therefore, the strategy that maximizes the city's loss is to ensure
that each additional passenger-segment ridden is charged to the oldest
entry card still available.  As a consequence, when a passenger exits
and must surrender a card, he should choose the youngest available to
prevent additional segments from being charged to it.  (Ideally, he
would obtain a brand-new card from a passenger entering the train at
the same stop.)

The following code implements this strategy, processing the passengers
who share a journey as a single group for efficiency.

"""

import fileinput
from heapq import heappush, heappop


def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print("Case #%r: %d" % (i, s))


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
    # each rider must exit with the youngest card left
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
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)


def read_problem(lines):
    N, M = read_ints(lines)
    journeys = [read_ints(lines) for _ in range(M)]
    return N, journeys


def read_ints(lines):
    return [int(s) for s in lines.next().split()]


if __name__ == "__main__":
    main()
