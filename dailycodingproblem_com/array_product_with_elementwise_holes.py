#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Solution to a problem about the product all of elements but the current.

* Problem

This problem comes from https://www.dailycodingproblem.com/ on
2019-03-26 and was classified as Hard.

  This problem was asked by Uber.

  Given an array of integers, return a new array such that each
  element at index i of the new array is the product of all the
  numbers in the original array except the one at i.

  For example, if our input was [1, 2, 3, 4, 5], the expected output
  would be [120, 60, 40, 30, 24]. If our input was [3, 2, 1], the
  expected output would be [2, 3, 6].

  Follow-up: what if you can't use division?


* Solutions

The obvious solution is to take the product of all the elements of the
input array and then generate an output array where the value at each
position is the product divided by the corresponding input element.

This works because, for each element x in the input array, if B is the
product of all elements before x, and A is the product of all elements
after x, then the value we want in x's position of the output array is
B * A, which is equal to B * x * A / x, and B * x * A is the product
of all of the input elements. It is important to note, however, that
that this method breaks down when x is zero, since there is no
multiplicative inverse for 0 in the set of integers, so we cannot
divide by zero.

** Corner cases

What if the input array is empty? The problem statement doesn't
actually tell us what to do in this case, but I'd suggest that the
least surprising output would be an empty array. That's because the
problem statement implies that whenever there is an element in the
output array at position i there's a corresponding element in the
input array at the same position.

So we should add this assertion to our test cases:

  assert soln([]) == []

What if the array has just one element? This is a trickier case
because the problem statement says that the "element at index i of the
new array is the product of all the numbers in the original array
except the one at i", but i ranges over just the singleton set {0},
thus there are no other numbers than the one at i.

So what's the product of an empty sequence of numbers? I'd argue that
the least surprising answer is 1. That's because 1 is the identity
value for multiplication on integers. There's also a consistency
argument to be made. The problem statement requires us to multiply a
sequence of numbers. Let's define Π(X) to be the product of the
numbers in the sequence X. It would be useful for Π to have a
consistency property such that if X where equal to the contatenation
of sequences X1 and X2, then Π(X) = Π(X1) * Π(X2). (In other words, Π
is a homomorphism over contatenation on sequences.) That property
implies that the product of an empty sequence is 1 because if we let
X1 be empty and X2 = X, the equation that defines our consistency
property becomes Π(X) = Π(empty) * Π(X), which is satisfied only
if Π(empty) = 1.

So we should add this assertion to our test cases:

  for all x: assert soln([x]) == [1]

This solution is implemented below in `array_of_products_1`.

** Variant: No division allowed

The problem also asks us how we would solve the problem if we were not
allowed to use division. In this case, let's recall that the value we
want to output in position i is Π(X[:i]) * Π(X[i+1:]). Fortunately, we
can precompute the values Π(X[:i]) and Π(X[i+1:]) for all i in linear
time using the multiplication equivalent of running totals.

Working left to right, we can compute an array of running products
l_prods in which l_prods[i] = Π(X[:i]). By our earlier reasoning we
know that l_prods[0] should be 1. Then each successive term just
accumulates the next value from X:

  running_product = 1
  for x in X:
    l_prods.append(running_product)
    running_product *= x
  ...

We can also do the same but working right to left to compute an array
r_prods where r_prods[i] = Π(X[i+1:]). With these two arrays, the
solution array can be generated in linear time:

  for i in range(len(X)):
    output[i] = l_prods[i] * r_prods[i]

This solution is implemented below in `array_of_products_2`.

** Variant: Reduced space use

The previous solution employs two internal arrays to keep track of the
left-to-right and right-to-left running products. As we have seen in
the code samples above, we can compute the left-to-right running
product as we scan from left to right through the input array. Since
the loop we use to populate the output array is also left to right, we
can combine these two steps to eliminate the `l_prods` array:

  l_running_product = 1
  for i in range(len(X)):
    output[i] = l_running_product * r_prods[i]
    l_running_product *= X[i]

Can we use the same idea to get rid of the `r_prods` array? Yes!
Multiplication on integers is associative and commutative, so we can
rearrange the multiplications however we want. We can compute the
left-to-right and right-to-level running products at the same time
and incrementally multiply them into the output arrays:

  l_running_product = r_running_product = 1
  n = len(X)
  result = [1] * n
  for i in range(n):
      result[i] *= l_running_product
      result[n - i - 1] *= r_running_product
      l_running_product *= X[i]
      r_running_product *= X[n - i - 1]
  return result


** Performance analysis

All three solutions run in linear time and space since they consume
O(1) time and space per element of the input array. This performance
is asymptotically optimal.

Proof of optimality: Any solution must run in at least linear time
because it must visit all of the elements of the input array, since
every element must be accounted for in the products in the output
array. Likewise, any solution must run in at least linear space
because it must produce an output array that is the same length as
the input array.

(In truth, a strict reading of the problem statement allows us to
always return an empty array as the solution, as an empty array
trivially satisfies the requirement that "each element at index i of
the new array is the product of all the numbers in the original array
except the one at i." That is, there is no explicitly stated
requirement that the set of indicies i for the output array must be
the same as for the input array. Thus, any output length from 0 to the
length of the input array is technically capable of satisfying the
problem statment. But common sense suggest that a problem that could
be solved by `return []` is probably not what the interviewer meant
when posing the problem. This would be a good opportunity to point out
the loophole and ask the interviewer to clarify the requirements.)

"""

# Solutions.

def array_of_products_1(X):
    assert all(x != 0 for x in X)  # Breaks when X contains 0.
    product = reduce(lambda x, y: x * y, X, 1)
    return [product / x for x in X]

def array_of_products_2(X):
    l_prods = lagged_running_products(X)
    r_prods = reversed(lagged_running_products(reversed(X)))
    return [x * y for x, y in zip(l_prods, r_prods)]

def array_of_products_3(X):
    l_running_product = r_running_product = 1
    n = len(X)
    result = [1] * n
    for i in range(n):
        result[i] *= l_running_product
        result[n - i - 1] *= r_running_product
        l_running_product *= X[i]
        r_running_product *= X[n - i - 1]
    return result

# Helpers.

def lagged_running_products(X):
    """Returns a list Y in which Y[i] is the product of all elems in X[:i].""" 
    products = []
    running_product = 1
    for x in X:
        products.append(running_product)
        running_product *= x
    return products

# Tests.

def test():
    for soln in (array_of_products_1, array_of_products_2, array_of_products_3):
        # Corner case: empty input array.
        assert soln([]) == []
        # Corner case: singleton input array.
        for x in range(1, 10):
            assert soln([x]) == [1]
        # Zero-handling cases.
        if soln != array_of_products_1:
            assert soln([0]) == [1]
            assert soln([1, 0, 2, 0]) == [0, 0, 0, 0]
        # General cases.
        assert soln([1, 2, 3]) == [6, 3, 2]
        assert soln([1, 2, 3, 4, 5]) == [120, 60, 40, 30, 24]
