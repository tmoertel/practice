#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-03-31
# Solution to "T9 Spelling" problem:
# http://code.google.com/codejam/contest/351101/dashboard#s=p2



import fileinput

#                0    1     2   3   4   5   6   7    8   9
ALPHA_GROUPS = [" ", ""] + "abc def ghi jkl mno pqrs tuv wxyz".split()
KEYPRESS_MAP = dict((char, (key, reps))
                    for (key, grp) in enumerate(ALPHA_GROUPS)
                    for (reps, char) in enumerate(grp, 1))

def main():
    for i, p in enumerate(read_problems(fileinput.input())):
        s = solve(p)
        print 'Case #%r: %s' % (i + 1, s)


def solve(problem):
    msg = problem
    def gen_keys():
        last_key = None
        for c in msg:
            keys = keys_for_char(c)
            if keys[-1:] == last_key:
                yield ' '
            last_key = keys[-1:]
            yield keys
    return ''.join(gen_keys())


def keys_for_char(c):
    key, reps = KEYPRESS_MAP[c]
    return str(key) * reps


def read_problems(lines):
    N = int(lines.next())
    for _ in xrange(N):
        yield read_problem(lines)


def read_problem(lines):
    return lines.next()[:-1]  # strip trailing linefeed


if __name__ == '__main__':
    main()
