#!/usr/bin/env python

def factorial(n):
    if n < 2:
        return 1
    return n * factorial(n - 1)

def factorial1a(n):
    def body(n):
        if n < 2:
            return 1
        return n * factorial(n - 1)
    result = body(n)
    return result

def factorial1b(n):
    def body(n):
        while True:
            if n < 2:
                return 1
            return n * body(n - 1)
            break
    result = body(n)
    return result

def factorial1c(n):
    def body(n, acc):
        while True:
            if n < 2:
                return 1 * acc
            return body(n - 1, acc * n)
            break
    result = body(n, 1)
    return result

def factorial1d(n):
    def body(n, acc):
        while True:
            if n < 2:
                return 1 * acc
            (n, acc) = (n - 1, n * acc)
            continue
            break
    result = body(n, 1)
    return result

def factorial1e(n):
    acc = 1
    while True:
        if n < 2:
            return 1 * acc
        (n, acc) = (n - 1, n * acc)

#####

def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)

def fib1a(n):
    def body(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        return body(n - 1) + body(n - 2)
    result = body(n)
    return result

def fib1b(n):
    def body(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        return body(n - 1) + body(n - 2)
    result = body(n)
    return result

def fib1c(n):
    def body(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        x = body(n - 1)
        y = body(n - 2)
        result = x + y
        return result
    result = body(n)
    return result


def fib1d(n):
    def body(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        return bot1(body(n - 1), n)
    def bot1(x, n):
        y = body(n - 2)
        result = x + y
        return result
    result = body(n)
    return result


def fib1e(n):
    def body(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        return bot1(body(n - 1), n)
    def bot1(x, n):
        return bot2(body(n - 2), x, n)
    def bot2(y, x, n):
        result = x + y
        return result
    result = body(n)
    return result

import functools


def fib1f(n):
    def body(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        return bot1(body(n - 1), n)
    def bot1(x, n):
        return bot2(body(n - 2), x, n)
    def bot2(y, x, n):
        result = x + y
        return result
    result = body(n)
    return result

def fib1g(n):
    def body(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        return bot1cont(n)(body(n - 1))
    def bot1cont(n):
        def bot1(x):
            return bot2cont(x, n)(body(n - 2))
        return bot1
    def bot2cont(x, n):
        def bot2(y):
            result = x + y
            return result
        return bot2
    result = body(n)
    return result

def identity(x):
    return x

def fib1h(n):
    def body(n, cont):
        if n == 0:
            return cont(0)
        if n == 1:
            return cont(1)
        return body(n - 1, bot1cont(n, cont))
    def bot1cont(n, cont):
        def bot1(x):
            return body(n - 2, bot2cont(x, n, cont))
        return bot1
    def bot2cont(x, n, cont):
        def bot2(y):
            result = x + y
            return cont(result)
        return bot2
    result = body(n, identity)
    return result

def call(f):
    """Instruct trampoline to call f with the args that follow."""
    def g(*args, **kwds):
        return f, args, kwds
    return g

def result(value):
    """Instruct trampoline to stop iterating and return a value."""
    return None, value, None

def with_trampoline(f):
    """Wrap a trampoline around a function that expects a trampoline."""
    @functools.wraps(f)
    def g(*args, **kwds):
        h = f
        # the trampoline
        while h is not None:
            h, args, kwds = h(*args, **kwds)
        return args
    return g

def trampoline_factorial(n, acc=1):
    if n < 2:
        return result(acc)
    return call(trampoline_factorial)(n - 1, n * acc)

factorialt = with_trampoline(trampoline_factorial)


import functools
def cps(f):
    """Wrap a function with an interpreter that allows for CPS idioms.

    When you wrap a function with this decorator, that function is
    "promoted" to continuation-passing style and supports CPS idioms
    allowing for (among other things) low-overhead tail calls in Python.

    The function's return value will be evaluated as a CPS expression
    of the form (e, C[@]), where e is an expression to evaluate and
    C[@] is a context with one hole (@) into which e's value should be
    inserted.  Evaluation can result in a simple value, in which case
    it is returned, or another CPS expression, in which case
    evaluation continues.  The process repeats (without consuming
    Python stack) until a simple value results; this is returned to
    the caller.

    CPS expressions can be created using one of four constructors:

      Val(x): the simple value x.

      Exp(f, args): the CPS expression that results from evaluating
        f(*args).

      ValTo(x)(k, kargs): the CPS expression that results from
        evaluating k(x, *kargs).

      ExpTo(f, args)(k, kargs): the CPS expression that results from
        evaluating f(*args), reducing the resulting CPS expression to
        a simple value x, and then evaluating k(x, *kargs).

    The idea is to


    TODO:  Add memoization. Take an additional function is_cachable
        that examines Exp, ValTo, and ExpTo forms and returns either
        None or a cache key.  If the function returns a key, it is
        checked-for in the cache and, if found, the associated value
        is returned.  If it's not found. It's value is computed,
        cached, and then returned.

    """
    @functools.wraps(f)
    def g(*args):
        stack = []
        fun, args, cont, cargs = f(*args)
        while True:
            if fun is None:
                if cont is None:
                    if not stack:
                        return args
                    cont, cargs = stack.pop()
                fun, args, cont, cargs = cont(args, *cargs)
            else:
                if cont:
                    stack.append((cont, cargs))
                fun, args, cont, cargs = fun(*args)
    return g

def Val(x):
    return None, x, None, None

def Exp(f, *args):
    return f, args, None, None

def ValTo(x):
    def g(cont, *cargs):
        return None, x, cont, cargs
    return g

def ExpTo(f, *args):
    def g(cont, *cargs):
        return f, args, cont, cargs
    return g


def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)

def fibcps1(n_):
    def top(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        return top(n - 1) + top(n - 2)
    return top(n_)

def fibcps2(n_):
    def top(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        x = top(n - 1)
        y = top(n - 2)
        result = x + y
        return result
    return top(n_)

def fibcps3(n_):
    def top(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        x = top(n - 1)
        return bot1(x, n)
    def bot1(x, n):
        y = top(n - 2)
        return bot2(y, x, n)
    def bot2(y, x, n):
        result = x + y
        return result
    return top(n_)

@cps
def fibcps4(n_):
    def top(n):
        if n == 0:
            return Val(0)
        if n == 1:
            return Val(1)
        return ExpTo(top, n - 1)(bot1, n)
    def bot1(x, n):
        return ExpTo(top, n - 2)(bot2, x, n)
    def bot2(y, x, n):
        result = x + y
        return Val(result)
    return Exp(top, n_)





# def fib1d(n):
#     def body(n, acc):
#         while True:
#             # top half
#             if n == 0:
#                 return 0 + acc
#             if n == 1:
#                 return 1 + acc
#             x = body(n - 1, acc)
#             # bottom half
#             return body(n - 2, x)
#             break
#     result = body(n, 0)
#     return result
#
#
# def fib1e(n):
#     stack = []
#     def body(n, acc):
#         while True:
#             # top half
#             if n == 0:
#                 return 0 + acc
#             if n == 1:
#                 return 1 + acc
#             x = body(n - 1, acc)
#             # bottom half
#             return body(n - 2, x)
#             break
#     result = body(n, 0)
#     while stack:
#         f = stack.pop()
#         result = f(result)
#     return result
#
#
# def fib1f(n):
#     stack = []
#     def bottom_half(n):
#         def continuation(x):
#             return body(n - 2, x)
#         return continuation
#     def body(n, acc):
#         while True:
#             # top half
#             if n == 0:
#                 return 0 + acc
#             if n == 1:
#                 return 1 + acc
#             stack.append(bottom_half(n))
#             (n, acc) = (n - 1, acc)
#             continue
#             break
#     result = body(n, 0)
#     while stack:
#         f = stack.pop()
#         result = f(result)
#     return result
#
# def fib1g(n):
#     cache = {}
#     stack = []
#     def bottom_half(n):
#         def continuation(x):
#             result = body(n - 2, x)
#             cache[n] = result
#             return result
#         return continuation
#     def body(n, acc):
#         if n in cache:
#             return cache[n] + acc
#         while True:
#             # top half
#             if n == 0:
#                 return 0 + acc
#             if n == 1:
#                 return 1 + acc
#             stack.append(bottom_half(n))
#             (n, acc) = (n - 1, acc)
#     result = body(n, 0)
#     while stack:
#         f = stack.pop()
#         result = f(result)
#     return result
#




### def fib1c(n, acc=0):
###     while True:
###         if n == 0:
###             return 0 + acc
###         if n == 1:
###             return 1 + acc
###         x = fib1c(n - 1)
###         (n, acc) = (n - 2, acc + x)
###         continue
###     return acc
###
### def fib1d(n, acc=0):
###     def body(n, acc):
###         while True:
###             if n == 0:
###                 return 0 + acc
###             if n == 1:
###                 return 1 + acc
###             x = fib1d(n - 1)
###             (n, acc) = (n - 2, acc + x)
###             continue
###     result = body(n, acc)
###     return result
###
### def fib1e(n, acc=0):
###     stack = []
###     def body(n, acc):
###         while True:
###             if n == 0:
###                 return 0 + acc
###             if n == 1:
###                 return 1 + acc
###             x = fib1e(n - 1)
###             (n, acc) = (n - 2, acc + x)
###             continue
###     result = body(n, acc)
###     while stack:
###         f = stack.pop()
###         result = f(result)
###     return result
###
###
### def fib1f(n, acc=0):
###     stack = []
###     def body(n, acc):
###         while True:
###             if n == 0:
###                 return 0 + acc
###             if n == 1:
###                 return 1 + acc
###             x = fib1f(n - 1)
###             (n, acc) = (n - 2, acc + x)
###             continue
###     result = body(n, acc)
###     while stack:
###         f = stack.pop()
###         result = f(result)
###     return result
###






## def fib1c(n, acc=0):
##     while True:
##         if n == 0:
##             acc = 0 + acc
##             break
##         if n == 1:
##             acc = 1 + acc
##             break
##         x = fib1c(n - 1)
##         # bottom half (after recursive call)
##         (n, acc) = (n - 2, acc + x)
##         continue
##     return acc
##
## def nop(x, acc):
##     return x, acc
##
## # def fib1d(n, acc=0):
## #     while True:
## #         if n == 0:
## #             acc = 0 + acc
## #             break
## #         if n == 1:
## #             acc = 1 + acc
## #             break
## #
## #         # x = fib1d(n - 1):
## #         ## push current location as return address
## #         ## push current state (n, acc)
## #         ## set (n, acc) = (n - 1, 0)
## #         ## jump to start of fib1d's function body
## #
## #
## #         # bottom half (after recursive call)
## #         (n, acc) = (n - 2, acc + x)
## #         continue
## #     return acc
##
##
## def identity(x):
##     return x
##
##
## def fib1cps(n, acc=0, k=identity):
##     while True:
##         if n == 0:
##             acc = 0 + acc
##             break
##         if n == 1:
##             acc = 1 + acc
##             break
##         x = fib1cps(n - 1)
##         # bottom half (after recursive call)
##         (n, acc) = (n - 2, acc + x)
##         continue
##     return acc
##
##
##
##
## def fib1d(n, acc=0):
##     stack = []
##     while True:
##         while True:
##             if n == 0:
##                 acc = 0 + acc
##                 break
##             if n == 1:
##                 acc = 1 + acc
##                 break
##             def bottom_half(n, acc):
##                 def continuation(x):
##                     return (n - 2, acc + x)
##                 return continuation
##             stack.append(bottom_half(n, acc))
##             (n, acc) = (n - 1, 0)
##             continue
##         if stack:
##             f = stack.pop()
##             n, acc = f(acc)
##             continue
##         return acc
##
##
## # def fib1d(n, acc=0):
## #     def bottom_half(_returned_n, returned_acc, n, acc):
## #         x = returned_acc
## #         return n - 2, x + acc
## #     stack = [(nop, ())]
## #     while stack:
## #         f, state = stack.pop()
## #         n, acc = f(n, acc, *state)
## #         while True:
## #             if n == 0:
## #                 acc = 0 + acc
## #                 break
## #             if n == 1:
## #                 acc = 1 + acc
## #                 break
## #             # x = fib1d(n - 1)
## #             stack.append((bottom_half, (n, acc)))
## #             (n, acc) = (n - 1, 0)
## #     return acc
## #
## # def fib1e(n, acc=0):
## #     def top_half(n, acc):
## #         while True:
## #             if n == 0:
## #                 acc = 0 + acc
## #                 break
## #             if n == 1:
## #                 acc = 1 + acc
## #                 break
## #             # x = fib1d(n - 1)
## #             stack.append((bottom_half, (n, acc)))
## #             (n, acc) = (n - 1, 0)
## #         return n, acc
## #     def bottom_half(_returned_n, returned_acc, n, acc):
## #         x = returned_acc
## #         return n - 2, x + acc
## #     stack = [(nop, ())]
## #     while stack:
## #         f, state = stack.pop()
## #         n, acc = f(n, acc, *state)
## #         n, acc = top_half(n, acc)
## #     return acc
## #
## # def fib1f(n, acc=0):
## #     def top_half(n, acc):
## #         while True:
## #             if n == 0:
## #                 acc = 0 + acc
## #                 break
## #             if n == 1:
## #                 acc = 1 + acc
## #                 break
## #             # x = fib1d(n - 1)
## #             stack.append((top_half, ()))
## #             stack.append((bottom_half, (n, acc)))
## #             (n, acc) = (n - 1, 0)
## #         return n, acc
## #     def bottom_half(_returned_n, returned_acc, n, acc):
## #         x = returned_acc
## #         return n - 2, x + acc
## #     stack = [(top_half, ())]
## #     while stack:
## #         f, state = stack.pop()
## #         n, acc = f(n, acc, *state)
## #     return acc
## #
## # def fib1g(n, acc=0):
## #     def top_half(n, acc):
## #         while True:
## #             if n == 0:
## #                 acc = 0 + acc
## #                 break
## #             if n == 1:
## #                 acc = 1 + acc
## #                 break
## #             # x = fib1d(n - 1)
## #             rcall(bottom_half, (n, acc))
## #             (n, acc) = (n - 1, 0)
## #         return n, acc
## #     def bottom_half(_returned_n, returned_acc, n, acc):
## #         x = returned_acc
## #         return n - 2, x + acc
## #     stack = [(top_half, ())]
## #     def rcall(f, state):
## #         stack.append((top_half, ()))
## #         stack.append((f, state))
## #     while stack:
## #         f, state = stack.pop()
## #         n, acc = f(n, acc, *state)
## #     return acc
## #
## # def fib1h(n, acc=0):
## #     def top_half(n, acc):
## #         while True:
## #             if n == 0:
## #                 acc = 0 + acc
## #                 break
## #             if n == 1:
## #                 acc = 1 + acc
## #                 break
## #             # x = fib1d(n - 1)
## #             rcall(bottom_half, (n, acc))
## #             (n, acc) = (n - 1, 0)
## #         return n, acc
## #     def bottom_half(_returned_n, returned_acc, n, acc):
## #         x = returned_acc
## #         return n - 2, x + acc
## #     stack = [(top_half, ())]
## #     def rcall(f, state):
## #         stack.append((top_half, ()))
## #         stack.append((f, state))
## #     cache = {}
## #     while stack:
## #         f, state = stack.pop()
## #         n, acc = f(n, acc, *state)
## #     return acc
##
##
## def fib1f(n, acc=0):
##     def top_half(n, acc):
##         while True:
##             if n == 0:
##                 acc = 0 + acc
##                 break
##             if n == 1:
##                 acc = 1 + acc
##                 break
##             # x = fib1d(n - 1)
##             stack.append((bottom_half, (n, acc)))
##             (n, acc) = (n - 1, 0)
##         return n, acc
##     def bottom_half(_returned_n, returned_acc, n, acc):
##         stack.append((top_half, ()))
##         x = returned_acc
##         cache[n] = x
##         return n - 2, x + acc
##     cache = {}
##     def remember(n, acc, slot):
##         cache[slot] = acc
##         return n, acc
##     stack = [(top_half, ())]
##     while stack:
##         f, state = stack.pop()
##         if acc == 0:
##             if n in cache:
##                 acc = cache[n]
##                 print 'hit'
##                 continue
##             # stack.append((remember, (n,)))
##         n, acc = f(n, acc, *state)
##     return acc



class Frame(dict):
    def __getattr__(self, name):
        return self[name]
    def __setattr__(self, name, value):
        self[name] = value

class EOW(object):
    """End-of-word marker."""
    def __repr__(self):
        return '$'
EOW = EOW()
import sys
LETTERS = 'abc'
N = 1
S = 'foo'
max_penalty = sys.maxint >> 1
words = dict()

def mcost(i, delay, tree):
    if i == N:
        return 0 if EOW in tree else max_penalty
    least = max_penalty
    if EOW in tree:
        least = min(least, mcost(i, delay, words))
    if S[i] in tree:
        least = min(least, mcost(i+1, max(0, delay-1), tree[S[i]]))
    if delay == 0:
        for l in LETTERS:
            if l != S[i] and l in tree:
                least = min(least, 1 + mcost(i+1, 4, tree[l]))
    return least



def test():
    fns = dict(globals())
    for fname, f in sorted(fns.iteritems()):
        if fname.startswith('factorial'):
            print('testing {}'.format(fname))
            for n in xrange(5):
                assert f(n) == reduce(int.__mul__, [1] + range(1, n + 1))
        if 'fib' in fname:
            print('testing {}'.format(fname))
            assert map(f, range(10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
if __name__ == '__main__':
    test()
