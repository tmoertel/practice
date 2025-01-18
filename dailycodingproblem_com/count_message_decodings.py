#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Solution to interview problem: count the ways a message can be decoded.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-03-26 and was classified as Medium.

  Reported source: Facebook.

  Given the mapping a = 1, b = 2, ..., v = 22, ... z = 26, and an
  encoded message, count the number of ways it can be decoded.

  For example, the message '222' would give 3, since it could be
  decoded as 'bbb', 'vb', and 'bv'.

  You can assume that the messages are decodable. For example, '002'
  is not allowed.


* Solution

Let's start by considering the edge cases. For convenience, let's call
the encoded message S.

If S is empty, there is only one possible decoding (the empty string),
so:

  def count_decodings(S):
      # Base case: empty encoding.
      if S == '':
          return 1

If S isn't empty, it must have a leading digit.

      assert '0' <= S[0] <= '9'

What if the leading digit is 0? Since there are no legal encodings
that start with 0, we know that the number of messages that could have
generated that encoding is zero:

      # Case: encoding starts with 0.
      if S[0] == '0':
          return 0

Assume that the digit isn't 0, 1, or 2. In that case, we can be
certain that it represents a single character in the original message,
so the number of ways to decode S is the same as the number of ways to
decode S[1:] (that is, S with the first digit removed). So:

      # Case: encoding starts with a digit greater than 2.
      if S[:1] > '2':
          return count_decodings(S[1:])

But what if the leading digit is 1? In that case, it could be that the
original message started with "a". If this is true, the number of ways
to decode S is the same as to decode S[1:]. But it could also be that
the 1 starts a two-digit number 1x that maps to the first character of
the original message, in which case the number of ways to decode S
would be the same as to decode S[2:]. Since both possibilities exist,
the number of possible decodings of S is sum of those two options:

      # Case: encoding starts with a 1.
      if S[:1] == '1':
          if S[:2] == '1':
              # No following digit: only one option.
              return count_decodings(S[1:])
          # Following digit: two options.
          assert '0' <= S[1] <= '9'
          return count_decodings(S[1:]) + count_decodings(S[2:])

Next, what if the leading digit is 2? This is similar to the case when
the leading digit is 1, but the second option appears only when the
following digit is between 0 and 6, since 27, 28, and 29 don't
participate in the mapping that defines the encoding.

      # Case: encoding starts with a 2.
      if S[:1] == '2':
          if S[:2] == '2':
              # No following digit: only one option.
              return count_decodings(S[1:])
          # Following digit exists.
          assert '0' <= S[1] <= '9'
          if '0' <= S[1] <= 6:
              # Following digit is 0-6: two options.
              return count_decodings(S[1:]) + count_decodings(S[2:])
          # Following digit is 7-9: one option.
          return count_decodings(S[1:])

And now we've covered all possible cases, leading digits 0-9.

** A recursive solution

This logic gives us a recursive solution to the problem, but as an
implementation, it's woefully inefficient. First, we're likely to call
`count_decodings` on the same substring many, many times. Consider the
calls we make to decode the string '112':

  count_decodings('112')
    = count_decodings('12') + count_decodings('2')
    = count_decodings('12') + count_decodings('')
    = count_decodings('12') + 1
    = count_decodings('2') + count_decodings('') + 1
    = count_decodings('2') + 1 + 1
    = count_decodings('') + 1 + 1
    = 1 + 1 + 1
    = 3

We called count_decodings on the substring '2' twice and on '' thrice.
That may not seem like much waste, but for longer inputs, the waste
increases.

Consider an input string of all 1's, that is '1111...' for some length
n. What's the run time of our solution when applied to this input? Let
T(n) be the cost of our solution applied to a string of length n.
Using our earlier recurrence as a reference, we know that

  T(0) = 1
  T(n) = T(n - 1) + T(n - 2) + O(n)    for n > 0

The last term arises from the string slices we take at each level of
the recursive call tree that our solution generates. (In Python, a
slice of length n has cost O(n).)

If we ignore the string slices, the run-time recurrence is

  T(n) = T(n - 1) + T(n - 2),

which is the recurrence that underlies the Fibonacci sequence. In that
sequence, the nth number F(n) is approximately φ^n / sqrt(5), where φ
is the golden ratio, approximately 1.618. Thus, the time complexity of
our naive recursive solution has a lower bound of Ω(φ^n), in other
words, exponential growth.

** A good candidate for dynamic programming

So what can we do to improve the efficiency of our solution? Looking
at the recursive solution, we see that at each step our recursive
calls take one of two forms,

  count_decodings(S[1:])   or
  count_decodings(S[2:]).

In order to solve the problem for S, we need to know the solutions for
S[1:] and S[2:]. Instead of computing them when we need them, what if
we had already computed them and saved them in a table? Let's create a
table `subcounts` such that subcounts[i] = count_decodings(S[i:]).
Then we can fill in that table, working backward from i = n to i = 0.
When we need to fill in subcounts[i], the subanswers we need will
already be in subcounts[i + 1] and subcounts[i + 2]. When we're
finished, the solution we want is just subcounts[0].

And that's a solution based on dynamic programming. I have implemented
this solution in `count_decodings_dp1` below. My implementation also
eliminates the need to take linear-time string slices by just passing
around the index i to indicate the substring of S that we care about.
This implementation runs in O(n) time and space.

As an optimization, we can take advantage of the fact that for any
given i, we will only ever look at two possible locations in the
table: i + 1 and i + 2. Therefore, we don't need to keep the entire
table in memory, just the previous two slots of the table as we work
backward from i = n to i = 0. I have implemented this strategy in
`count_decodings_dp2` below. It runs in O(n) time and O(1) space.

"""


# Complexity: Ω(φ^n) time, O(n^2) space.
def count_decodings(S):
    """Counts the messages that encode to S."""
    # Base case: empty encoding.
    if S == "":
        return 1
    # Non-empty cases follow.
    assert "0" <= S[0] <= "9"
    # Case: encoding starts with a digit greater than 2.
    if S[:1] > "2":
        return count_decodings(S[1:])
    # Case: encoding starts with 0.
    if S[:1] == "0":
        return 0
    # Case: encoding starts with a 1.
    if S[:1] == "1":
        if S[:2] == "1":
            # No following digit: only one option.
            return count_decodings(S[1:])
        # Following digit: two options.
        assert "0" <= S[1] <= "9"
        return count_decodings(S[1:]) + count_decodings(S[2:])
    # Case: encoding starts with a 2.
    if S[:1] == "2":
        if S[:2] == "2":
            # No following digit: only one option.
            return count_decodings(S[1:])
        assert "0" <= S[1] <= "9"
        if "0" <= S[1] <= "6":
            # Following digit is 0-6: two options.
            return count_decodings(S[1:]) + count_decodings(S[2:])
        # Following digit is 7-9: one option.
        return count_decodings(S[1:])


# Complexity: O(n) time and space.
def count_decodings_dp1(encoded_message):
    """Counts the messages that encode to `encoded_message`."""
    n = len(encoded_message)

    # Helper: Returns char at index i (or '' if i is out of bounds).
    def char(i):
        return encoded_message[i : i + 1]

    # Helper: Returns true iff there is a legal 2-digit value at index i.
    def two_digits(i):
        return (char(i) == "1" and "0" <= char(i + 1) <= "9") or (
            char(i) == "2" and "0" <= char(i + 1) <= "6"
        )

    # Compute subcount[i] by working backward from i = n to 0, saving
    # our results along the way. Note that we set subcounts[n] = 1 as
    # it corresponds to the base case for an empty string, which can
    # be generated by only 1 source message. Note also that we preset
    # subcounts[n + 1] = 0 to eliminate the need for some bounds
    # checking by recording the fact that no source messages can
    # generate an encoded message of negative length.
    subcounts = [0] * (n + 2)  # Initialize the memo table to zeroes.
    subcounts[n] = 1  # Base case for empty substring.
    for i in range(n - 1, -1, -1):
        assert "0" <= char(i) <= "9"
        if char(i) > "0":
            subcounts[i] = subcounts[i + 1]
        if two_digits(i):
            subcounts[i] += subcounts[i + 2]
    return subcounts[0]


# Complexity: O(n) time and O(1) space.
def count_decodings_dp2(encoded_message):
    """Counts the messages that encode to `encoded_message`."""
    n = len(encoded_message)

    # Helper: Returns char at index i (or '' if i is out of bounds).
    def char(i):
        return encoded_message[i : i + 1]

    # Helper: Returns true iff there is a legal 2-digit value at index i.
    def two_digits(i):
        return (char(i) == "1" and "0" <= char(i + 1) <= "9") or (
            char(i) == "2" and "0" <= char(i + 1) <= "6"
        )

    # Compute subcount[i] working backward from i = n to 0, retaining
    # only two prior values since no more are needed.
    subcount = subcount_lag_1 = 1
    subcount_lag_2 = 0
    for i in range(n - 1, -1, -1):
        assert "0" <= char(i) <= "9"
        if char(i) == "0":
            subcount = 0
        elif two_digits(i):
            subcount += subcount_lag_2
        subcount_lag_1, subcount_lag_2 = subcount, subcount_lag_1
    return subcount


def test():
    for soln in count_decodings, count_decodings_dp1, count_decodings_dp2:
        print(soln.__name__)
        # Empty message has only one decoding: the empty message.
        assert soln("") == 1
        # Cases inolving zero.
        assert soln("0") == 0
        assert soln("10") == 1
        assert soln("20") == 1
        assert soln("30") == 0
        # Cases involving one and two.
        assert soln("1") == 1
        assert soln("2") == 1
        assert soln("11") == 2
        assert soln("21") == 2
        assert soln("18") == 2
        assert soln("28") == 1
        # Examples from the problem statement.
        assert soln("111") == 3
