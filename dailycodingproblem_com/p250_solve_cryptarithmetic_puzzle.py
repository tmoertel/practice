#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find the winning starts for a game of Ghost.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-11-29 (#250) and was classified as Medium.

  Reported source: Google.

  A cryptarithmetic puzzle is a mathematical game where the digits of
  some numbers are represented by letters. Each letter represents a
  unique digit.

  For example, a puzzle of the form:

    SEND
  + MORE
  --------
   MONEY

  may have the solution:

  {'S': 9, 'E': 5, 'N': 6, 'D': 7, 'M': 1, 'O': 0, 'R': 8, 'Y': 2}

  Given a three-word puzzle like the one above, create an algorithm
  that finds a solution.


* Solution

A cryptarithmetic puzzle asks us to find a mapping from the variables
(letters) in the puzzle to the digits 0-9, such that the equation
implied by the puzzle holds. The problem definition says that "each
letter represents a unique digit," so the mapping must be injective.
Therefore, since there only 10 decimal digits, the largest problems
can have no more than 10 variables.

How many ways are there to map 10 variables to 10 digits? Line up the
variables and then write a distinct digit beneath each variable. That's
one mapping. Each possible way to order the digits -- each permutation --
gives another mapping. Since there are 10! = 3,628,800 possible
permutations, that's how many possible mappings there are.

** Brute force

Since 3.6 million is smallish for a modern laptop computer, one option
we have for solving the problem is to try every permutation. In
general, for a puzzle with i variables, we will need to try P(10, i) =
10!/(10-i)! permutations. Let's use Maxima to compute the number
of permutations for puzzles of 1 through 10 variables:

  Maxima 5.38.1 http://maxima.sourceforge.net
  using Lisp GNU Common Lisp (GCL) GCL 2.6.12
  Distributed under the GNU Public License. See the file COPYING.
  Dedicated to the memory of William Schelter.
  The function bug_report() provides bug reporting information.
  (%i1) load(functs)$
  (%i2) create_list(permutation(10, i), i, 1, 10);
  (%o2) [10, 90, 720, 5040, 30240, 151200, 604800, 1814400, 3628800, 3628800]


** Smart search

Even through brute force is a viable approach for this problem, can we
do something more efficient? One approach is to notice that every large
puzzle contains smaller puzzles. For example, consider the puzzle

    SEND
  + MORE
  --------
   MONEY

which contains 8 variables. What if we just looked at least-
significant digits and ignored the carry? Then we would have this much
smaller puzzle:

    D
  + E
  -----  (mod 10)
    Y

This puzzle has only three variables, which admit only 10!/7! = 720
permutations. We can try all of them very quickly to solve the small
puzzle and arrive at a small number of viable mappings for D, E, and
Y. In this example, there are only 72 viable mappings. That means that
when we try to solve the full puzzle, we can skip any possible mapping
that doesn't have D, E, and Y set to one of the viable solutions for
the small problem. We've effectively reduced an 8-variable puzzle into
72 smaller 5-variable puzzles in which 3 digits have already been
claimed, reducing our work by a factor of 10:


  (%i3) permutation(10, 8) / (72 * permutation(7, 5));
  (%o3) 10

But we're not done! We can use the same trick again. Now let's solve
the slightly larger puzzle that contains the two least-significant
digits:

    ND
  + RE
  ------  (mod 100)
    EY

This puzzle contains only 2 new variables, N and R, and since D, E,
and Y are already bound to digits, the number of permutations we'll
have to consider is P(7, 2) = 42 for each viable solution from the
previous smaller puzzle.

Extending to the next digit, we have this puzzle:

    END
  + ORE
  -------  (mod 1000)
    NEY

This puzzle introduces only one new variable, and since five digits have
already been consumed, there's only P(5, 1) = 5 permutations to check for
each viable solution from the previous smaller puzzle.

Moving on:

    SEND
  + MORE
  --------  (mod 10,000)
    ONEY

This puzzle introduces two new variables, S and M, but there are only
4 digits from which to choose, leaving only P(4, 2) = 12 permutations
to check for each viable solution from the previous smaller puzzle.

Moving on:

     SEND
   + MORE
  ---------  (mod 100,000)
    MONEY

By this point, all of the variables have been bound, so we need only
to check the viable solutions from the previous smaller puzzle to make
sure they satisfy the constraints of the larger puzzle.

In general, when solving a puzzle having n decimal places, we'll want
to check the full puzzle modulo 10^(n+1) to ensure we filter out any
unwanted carries. For example, consider the puzzle

     A
   + B
  ------
     C

For this puzzle, {A=5, B=6, C=1} is not a valid solution because 5 + 6
== 11 != 1. But if we check the puzzle modulo 10, it appears to be
valid:

     5
   + 6
  ------  (mod 10)
     1

That's why we must also check our proposed n-digit solutions modulo
10^(n+1) to filter out solutions with nonmatching carries:

     5 + 6 != 1  (mod 100);  therefore we reject {A=5, B=6, C=1}.



"""

import itertools
import sys

def brute_force_solutions(first, second, total, modulus=None, bindings=None):
    """Yields solutions to a cryptarithmetic puzzle.

       FIRST
    + SECOND
      ------
       TOTAL

    """
    def mod(n):
        return n % modulus if modulus else n

    def is_solution(bindings):
        """Returns True iff the given variable bindings satisfy the equation."""
        def to_num(word):
            place = 1
            value = 0
            for variable in reversed(word):
                value += place * bindings[variable]
                place *= 10
            return value
        return mod(to_num(first) + to_num(second)) == mod(to_num(total))

    # Brute force: try all assignments of free digits to free variables.
    bindings = bindings or {}  # Some variables may already be bound.
    free_digits = list(set(range(10)) - set(bindings.values()))
    free_vars = sorted(set(first + second + total) - set(bindings))
    for digit_sequence in itertools.permutations(free_digits, len(free_vars)):
        new_bindings = dict(zip(free_vars, digit_sequence))
        new_bindings.update(bindings)
        if is_solution(new_bindings):
            yield new_bindings


def cryptarithmetic_solutions(first, second, total):
    """Returns solutions to a cryptarithmetic puzzle."""
    solutions = [{}]
    # Work from 1 to n + 1 decimal places, solving successively larger puzzles.
    for places in range(1, max(map(len, [first, second, total])) + 2):
        def solve_from_partial_solution(solution):
            return brute_force_solutions(
                first[-places:], second[-places:], total[-places:],
                10**places, solution)
        solutions = itertools.chain.from_iterable(
            map(solve_from_partial_solution, solutions))
    return solutions


# Tests.

from nose.tools import assert_dict_equal

def normalize_bindings(bindings):
    return sorted(bindings.items())

def test_example_soln_must_match_problem_statement():
    solutions = [
        normalize_bindings(soln)
        for soln in cryptarithmetic_solutions('SEND', 'MORE', 'MONEY')]
    for soln in solutions:
        print 'soln: {}'.format(soln)
    expected = {'S': 9, 'E': 5, 'N': 6, 'D': 7, 'M': 1, 'O': 0, 'R': 8, 'Y': 2}
    expected = normalize_bindings(expected)
    assert expected in solutions


def test_single_digit_solution_must_match_common_sense():
    for bindings in cryptarithmetic_solutions('A', 'B', 'C'):
        assert bindings['A'] + bindings['B'] == bindings['C']


def test_unsolvable_equation_must_have_no_solutions():
    solns = list(cryptarithmetic_solutions('A', 'B', 'CCC'))
    assert not solns

def test_puzzle_with_more_than_ten_variables_must_have_no_solutions():
    solns = list(cryptarithmetic_solutions('ABCD', 'GHIJ', 'KLMN'))
    assert not solns

def test_empty_puzzle_must_have_only_the_empty_solution():
    solns = list(cryptarithmetic_solutions('', '', ''))
    assert solns == [{}]


# Command-line solver.

def main():
    if len(sys.argv) != 4:
        print 'Usage: {} first_word second_word total_word'.format(sys.argv[0])
        sys.exit(1)

    # Preserve the character ordering from the given words.
    words = sys.argv[1:4]
    seen = set()
    char_order = []
    for char in ''.join(words):
        if char not in seen:
            seen.add(char)
            char_order.append(char)

    # Print each solution on its own line, using the initial ordering.
    for bindings in cryptarithmetic_solutions(*words):
        variable_map = ', '.join('%s=%r' % (c, bindings[c]) for c in char_order)
        solution = ''.join(str(bindings.get(c, c)) for c in ' '.join(words))
        print '{} / {}'.format(variable_map, solution)


if __name__ == '__main__':
    main()
