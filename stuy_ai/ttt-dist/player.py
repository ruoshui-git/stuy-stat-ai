import sys
from typing import Literal, Optional
from functools import reduce

Player = Literal['x', 'o']
X = 'x'
O = 'o'
EMPTY = None

Board = list[Optional[Player]]

EMPTY_BOARD: Board = [None] * 9

WINS: list[tuple[int, int, int]] = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                                    (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def next_player(board: Board) -> Player:
    if (9 - board.count(None)) % 2 == 0:
        return 'x'
    else:
        return 'o'


def winner(board: Board) -> Optional[Player]:
    for (a, b, c) in WINS:
        if board[a] is not None and board[a] == board[b] == board[c]:
            return board[a]


def is_filled(board: Board) -> bool:
    return all(spot is not None for spot in board)


def actions(board: Board) -> set[int]:
    '''
    Returns set of all possible actions available on the board.
    '''
    # return {(r, c) for r, row in enumerate(board) for c, val in enumerate(row) if val == EMPTY}
    return {i for i, pos in enumerate(board) if pos is None}


def result(board: Board, action: int):
    '''
    Returns the board that results from making move (i, j) on the board.
    '''
    if board[action] != EMPTY:
        raise ValueError(
            f'Cannot make move to position {action}, which is already {board[action]}')
    board = board.copy()
    board[action] = next_player(board)
    return board


def terminal(board: Board) -> bool:
    '''
    Returns True if game is over, False otherwise.
    '''
    return winner(board) is not None or is_filled(board)


def utility(board: Board):
    '''
    Returns 1 if X has won the game, -1 if O has won, 0 if tied. Expects board to be filled.
    '''
    w = winner(board)
    if w == 'x':
        return 1
    elif w == 'o':
        return -1
    else:
        return 0


def maxval(board: Board) -> tuple[int, int]:
    assert next_player(board) == X
    if terminal(board):
        return utility(board), 0
    v = float('-inf'), float('-inf')
    for action in actions(board):
        v = max(v, minval(result(board, action)))
    # print(f'maxval: {v=}, {board=}')
    # max player will have negative distance
    return (int(v[0]), int(v[1]) + -1)


def minval(board: Board) -> tuple[int, int]:
    assert next_player(board) == O
    if terminal(board):
        return utility(board), 0
    v = float('inf'), float('inf')
    for action in actions(board):
        v = min(v, maxval(result(board, action)))
    # print(f'minval: {v=}, {board=}')
    return (int(v[0]), int(v[1]) + 1)


def minimax(board: Board) -> Optional[tuple[tuple[int, int], int]]:
    '''
    Returns the optimal action for the current player on the board.
    '''
    if terminal(board):
        return None
    moves = [a for a in actions(board)]
    if next_player(board) == X:
        # reducer = max
        # return max(moves, key=lambda action: minval(result(board, action)))
        return max([(minval(result(board, (move))), move) for move in moves])
    else:
        # return min(moves, key=lambda action: maxval(result(board, action)))
        return min([(maxval(result(board, (move))), move) for move in moves])
        # return min(((move, maxval(result(board, (move)))) for move in moves))
        # reducer = min
    # return reduce(reduce, )


def parse(board_str: str) -> Board:
    # board = []
    # for c in board_str:
    #     if c == '_':
    #         board.append(None)
    #     else:
    #         board.append(c)
    # return board
    return [None if c == '_' else c for c in board_str]  # type: ignore


POSITIONS = ('Top-left', 'Top-center', 'Top-right', 'Middle-left', 'Middle-center',
             'Middle-right', 'Bottom-left', 'Bottom-center', 'Bottom-right')


def main():
    if len(sys.argv) != 3:
        print('''Usage:
python player.py {result-filename} {board}
''')
        return 1
    outfile = sys.argv[1]
    board = parse(sys.argv[2])
    # poss = [i for i in range(9) if board[i] == '_']
    r = minimax(board)
    assert r is not None
    move, (final, dist) = r
    if final > 0:
        msg = f'{dist} steps to x winning\n'
    elif final < 0:
        msg = f'{dist} steps to o winning\n'
    else:
        msg = f'{dist} steps to a draw\n'

    s = '\n'.join([str(move),
                   POSITIONS[move],
                   msg])
    print(s)
    f = open(outfile, 'w')
    f.write(s)
    f.close()


if __name__ == '__main__':
    main()
