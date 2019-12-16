#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Soln to problem: Find the winning starts for a game of Ghost.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-11-29 (#250) and was classified as Medium.

  This problem was asked by Google.

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


"""


import itertools
import sys


def cryptarithmetic_solutions(first, second, total):
    """Yield solutions to a cryptarithmetic puzzle.

       FIRST
    + SECOND
      ------
       TOTAL

    """
    def is_solution(bindings):
        """Returns True iff the given variable bindings satisfy the equation."""
        def to_num(word):
            place = 1
            value = 0
            for variable in reversed(word):
                value += place * bindings[variable]
                place *= 10
            return value
        try:
            return to_num(first) + to_num(second) == to_num(total)
        except KeyError:
            return False

    # Brute force: try all assignments of digits to variables.
    digits = list(range(10))
    variables = sorted(set(first + second + total))
    for digit_sequence in itertools.permutations(digits, len(variables)):
        bindings = dict(zip(variables, digit_sequence))
        if is_solution(bindings):
            yield bindings


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


def test_unsolvable_problem_must_have_no_solutions():
    solns = list(cryptarithmetic_solutions('A', 'B', 'CCC'))
    assert not solns


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
        print ', '.join('%s=%r' % (c, bindings[c]) for c in char_order)


if __name__ == '__main__':
    main()
