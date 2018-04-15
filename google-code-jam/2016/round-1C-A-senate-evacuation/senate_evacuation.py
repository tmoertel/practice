#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2018-04-15


"""Solution to "Senate Evacuation" Code Jam problem
https://code.google.com/codejam/contest/4314486/dashboard

Problem:

The original problem was defined as follows:

    A small fire started in the senate room, and it needs to be
    evacuated!

    There are some senators in the senate room, each of whom belongs
    to of one of N political parties. Those parties are named after
    the first N (uppercase) letters of the English alphabet.

    The emergency door is wide enough for up to two senators, so in
    each step of the evacuation, you may choose to remove either one
    or two senators from the room.

    The senate rules indicate the senators in the room may vote on any
    bill at any time, even in the middle of an evacuation! So, the
    senators must be evacuated in a way that ensures that no party
    ever has an absolute majority. That is, it can never be the case
    after any evacuation step that more than half of the senators in
    the senate room belong to the same party.

    Can you construct an evacuation plan? The senate is counting on
    you!

For fun, I am adding an additional constraint:

    The evacuation plan must be minimal, i.e., ensuring that all
    senators are evacuated in the fewest possible steps.


Solution

    Proof that solution is minimal:

    Senators can leave in groups of no more than two. Therefore, if
    there are N senators, it is not possible to have a solution of
    fewer than ceil(N/2) steps.

    When N is even, our solution will consist of N/2 groups of two
    because at no step in the evacuation plan will the number of
    remaining senators ever be odd, let alone 3, the only case in
    which we elect to emit a group of only one senator. As N/2 is less
    than or equal to ceil(N/2), our solution is minimal in this case.

    When N is odd, our solution will emit groups of two until the
    number of senators reaches 3, at which point a group of one
    senator will be emitted, followed by a group of two. Therefore
    there will be (N-1)/2 + 1 steps. As (N-1)/2 + 1 = ceil(N/2)
    when N is odd, our solution is minimal in this case too.

    Since our solution is minimal for both even and odd cases,
    it is always minimal. QED.

"""



import collections
import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print('Case #%r: %s' % (i, s))

def solve(problem):
    # Parse the problem instance.
    party_sizes = problem

    # Set up the initial state.
    parties_of_size = collections.defaultdict(list)
    for i, size in enumerate(party_sizes):
        parties_of_size[size].append(chr(ord('A') + i))
    max_size = max(parties_of_size)
    num_senators = sum(party_sizes)
    groups = []

    # Eject senators in groups of one or two, drawing each senator
    # from the party with the most senators left in the building.
    while num_senators > 0:
        # Start a new group of 1 or 2 senators.
        group_members = []
        groups.append(group_members)
        group_size = 1 if num_senators == 3 else 2
        # Fill the group with senators.
        for _ in range(group_size):
            # Eject a senator from a party of maximal remaining size.
            party = parties_of_size[max_size].pop()
            group_members.append(party)
            num_senators -= 1
            # Reduce the selected party's size by one.
            if max_size > 1:
                parties_of_size[max_size - 1].append(party)
            if not parties_of_size[max_size]:
                del parties_of_size[max_size]
                max_size -= 1
        # After each step in our plan, verify that no party has a majority.
        assert max_size <= num_senators - max_size

    # Convert the sequence of groups into the required output format.
    return ' '.join(''.join(group) for group in groups)

def read_problems(lines):
    T = int(lines.next())
    for _ in range(T):
        yield read_problem(lines)

def read_problem(lines):
    N, = read_ints(lines)
    party_sizes = read_ints(lines)
    assert len(party_sizes) == N
    return party_sizes

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
