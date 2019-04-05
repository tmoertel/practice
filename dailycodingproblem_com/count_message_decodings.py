#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Solution to interview problem: count the ways a message can be decoded.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-03-26 and was classified as Medium.

  This problem was asked by Facebook.

  Given the mapping a = 1, b = 2, ... z = 26, and an encoded message,
  count the number of ways it can be decoded.

  For example, the message '111' would give 3, since it could be
  decoded as 'aaa', 'ka', and 'ak'.

  You can assume that the messages are decodable. For example, '001'
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

Assume that the digit isn't 1 or 2. In that case, we can be certain
that it represents a single character in the original message, so the
number of ways to decode S is the same as the number of ways to decode
S[1:], that is S with the first digit removed. So:

      # Case: encoding starts with a digit other than 1 or 2.
      elif S[:1] > '2':
          return count_decodings(S[1:])

But what if the leading digit is 1? In that case, it could be that the
original message started with "a". If this is true, the number of ways
to decode S is the same as to decode S[1:]. But it could also be that
the 1 starts a two-digit number 1x that maps to the first character of
the original message, in which case the number of ways to decode S
would be the same as to decode S[2:]. Since both possibilities exist,
the number of possible decodings of S is sum of those two options:

      # Case: encoding starts with a 1.
      elif S[:1] == '1':
          if S[:2] == '1':
              # No following digit: only one option.
              return count_decodings(S[1:])
          # Following digit: two options.
          assert '0' <= S[2] <= '9'
          return count_decodings(S[1:]) + count_decodings(S[2:])

And, finally, what if the leading digit is 2? This is similar to the
case when the leading digit is 1, but the second option appears only
when the following digit is between 1 and 6, since 27, 28, and 29
don't participate in the mapping that defines the encoding.

      # Case: encoding starts with a 2.
      else:
          if S[:2] == '2':
              # No following digit: only one option.
              return count_decodings(S[1:])
          # Following digit exists.
          assert '0' <= S[2] <= '9'
          if '0' <= S[2] <= 6:
              # Following digit is 1, 2, 3, 4, 5, or 6: two options.
              return count_decodings(S[1:]) + count_decodings(S[2:])
          # Following digit is 7, 8, or 9: one option.
          return count_decodings(S[1:])

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

TODO: discuss translation of implementation to dynamic programming.

"""

def count_decodings_1(encoded_message):
    n = len(encoded_message)
    # Helper: Returns char at index i (or '' if i is out of bounds).
    def char(i):
        return encoded_message[i : i + 1]
    # Helper: Returns true iff there is a 2-digit value at index i.
    def two_digits_at(i):
        return ((char(i) == '1' and '0' <= char(i + 1) <= '9') or
                (char(i) == '2' and  '0' <= char(i + 1) <= '6'))
    # 
    subcounts = [0] * (n + 2)
    subcounts[n] = 1
    for i in range(n - 1, -1, -1):
        assert '0' <= char(i) <= '9'
        subcounts[i] = subcounts[i + 1]
        if two_digits_at(i):
            subcounts[i] += subcounts[i + 2]
    return subcounts[0]

def count_decodings_2(encoded_message):
    n = len(encoded_message)
    # Helper: Returns char at index i (or '' if i is out of bounds).
    def char(i):
        return encoded_message[i : i + 1]
    # Helper: Returns true iff there is a 2-digit value at index i.
    def two_digits_at(i):
        return ((char(i) == '1' and '0' <= char(i + 1) <= '9') or
                (char(i) == '2' and  '0' <= char(i + 1) <= '6'))
    #
    subcounts_lag_2 = 0
    subcounts = subcounts_lag_1 = 1
    for i in range(n - 1, -1, -1):
        assert '0' <= char(i) <= '9'
        if two_digits_at(i):
            subcounts += subcounts_lag_2
        subcounts_lag_1, subcounts_lag_2 = subcounts, subcounts_lag_1
    return subcounts

def test():
    for soln in count_decodings_1, count_decodings_2:
        print soln.__name__
        # Empty message has only one decoding: the empty message.
        assert soln('') == 1
        assert soln('1') == 1
        assert soln('11') == 2
        # Examples from the problem statement.
        assert soln('111') == 3
    
