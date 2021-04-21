from typing import Literal, Optional

Player = Literal['x', 'o']

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
    return board.count(None) == 0


xwins = 0
owins = 0
ndraws = 0


def count_games(board: Board = EMPTY_BOARD) -> int:
    w = winner(board)
    global xwins, owins, ndraws
    if w is not None or is_filled(board):
        if w == 'x':
            xwins += 1
        elif w == 'o':
            owins += 1
        else:
            ndraws += 1
        return 1
    player = next_player(board)

    ngames = 0
    for i, pos in enumerate(board):
        if pos is None:
            new_board = board.copy()
            new_board[i] = player
            ngames += count_games(new_board)

    return ngames


def count_boards(board: Board = EMPTY_BOARD) -> int:
    if winner(board) is not None or is_filled(board):
        return 1
    player = next_player(board)

    nboards = 1
    for i, pos in enumerate(board):
        if pos is None:
            new_board = board.copy()
            new_board[i] = player
            nboards += count_boards(new_board)

    return nboards


ROT90 = [6, 3, 0, 7, 4, 1, 8, 5, 2]
ROT180 = [8, 7, 6, 5, 4, 3, 2, 1, 0]
ROT270 = [2, 5, 8, 1, 4, 7, 0, 3, 6]
FLIP = [2, 1, 0, 5, 4, 3, 8, 7, 6]
TRANS = [[ROT90], [ROT180], [ROT270], [FLIP],
         [ROT90, FLIP], [ROT180, FLIP], [ROT270, FLIP]]


def apply_trans(board: Board, trans: list[list[int]]) -> Board:
    nb: Board = [None] * 9
    for t in trans:
        for fr, to in enumerate(t):
            nb[to] = board[fr]
        # move to the next transformation
        board = nb.copy()

    return nb


# for tr in TRANS:
#     print(apply_trans(['x', 'o', None, None,
#                        None, None, None, None, None], tr))

seen: set[tuple[Optional[Player], ...]] = set()


def count_unique_boards(board: Board = EMPTY_BOARD) -> int:

    if winner(board) is not None or is_filled(board):
        return 1
    player = next_player(board)

    nboards = 1
    for i, pos in enumerate(board):
        if pos is None:
            new_board = board.copy()
            new_board[i] = player

            family = [apply_trans(new_board, tr) for tr in TRANS] + [new_board]
            if any((tuple(member) in seen for member in family)):
                # saw a transformed board before
                continue

            seen.add(tuple(new_board))  # type: ignore
            nboards += count_boards(new_board)

    return nboards


if __name__ == "__main__":

    print(f'total games: {count_games()}')
    print(f'{xwins=}')
    print(f'{owins=}')
    print(f'{ndraws=}')
    print('='*20)
    print(f'{count_boards()=}')
    print(f'{count_unique_boards()=}')
