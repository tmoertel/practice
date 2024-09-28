#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-09


"""Solution to "Rotate" Code Jam problem
http://code.google.com/codejam/contest/544101/dashboard#s=p0

"""

import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print('Case #%r: %s' % (i, s))

def solve(problem):
    _, K, board = problem
    board = rotate_board(board)
    winners = find_winners(board, K)
    if not winners:
        return 'Neither'
    if len(winners) == 2:
        return 'Both'
    return list(winners)[0]

def rotate_board(board):
    if board:
        N = len(board)
        pad = '.' * N
        board = [(pad + row.replace('.', ''))[-N:] for row in board]
        board = [list(reversed(row)) for row in zip(*board)]
    return board

def find_winners(board, K):
    # brute-force search (w/o duplicate removal)
    N = len(board)
    winners = set()
    for row in range(N):
        for col in range(N):
            for color in 'Red', 'Blue':
                for rdir in -1, 0, 1:
                    for cdir in -1, 0, 1:
                        if is_winner(board, row, col, color[0], rdir, cdir, K):
                            winners.add(color)

    return winners

def is_winner(board, row, col, color_code, rdir, cdir, k):
    if rdir == cdir == 0:
        return False
    N = len(board)
    while k and 0 <= row < N and 0 <= col < N:
        if board[row][col] != color_code:
            break
        k -= 1
        row += rdir
        col += cdir
    return k == 0

def read_problems(lines):
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)

def read_problem(lines):
    N, K = list(map(int, lines.next().split()))
    board = [lines.next().replace('\n', '') for _ in range(N)]
    return N, K, board

if __name__ == '__main__':
    main()
