import sys

from typing import Literal, Optional



# Player = Literal['x', 'o']

X = 'x'

O = 'o'

EMPTY = None



# Board = list[Optional[Player]]



EMPTY_BOARD        = [None] * 9



WINS                             = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),

                                    (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]





def next_player(board       )          :

    if (9 - board.count(None)) % 2 == 0:

        return 'x'

    else:

        return 'o'





def winner(board       )                    :

    for (a, b, c) in WINS:

        if board[a] is not None and board[a] == board[b] == board[c]:

            return board[a]





def is_filled(board       )        :

    return all(spot is not None for spot in board)





def actions(board       )            :

    '''

    Returns set of all possible actions available on the board.

    '''

    # return {(r, c) for r, row in enumerate(board) for c, val in enumerate(row) if val == EMPTY}

    return {i for i, pos in enumerate(board) if pos is None}





def result(board       , action     ):

    '''

    Returns the board that results from making move (i, j) on the board.

    '''

    if board[action] != EMPTY:

        raise ValueError(

            f'Cannot make move to position {action}, which is already {board[action]}')

    board = board.copy()

    board[action] = next_player(board)

    return board





def terminal(board       )        :

    '''

    Returns True if game is over, False otherwise.

    '''

    return winner(board) is not None or is_filled(board)





def utility(board       ):

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





def maxval(board       )       :

    assert next_player(board) == X

    v = float('-inf')

    if terminal(board):

        return utility(board)

    for action in actions(board):

        v = max(v, minval(result(board, action)))

    # print(f'maxval: {v=}, {board=}')

    return int(v)





def minval(board       )       :

    assert next_player(board) == O

    v = float('inf')

    if terminal(board):

        return utility(board)

    for action in actions(board):

        v = min(v, maxval(result(board, action)))

    # print(f'minval: {v=}, {board=}')

    return int(v)





def minimax(board       )                 :

    '''

    Returns the optimal action for the current player on the board.

    '''

    if terminal(board):

        return None

    moves = [a for a in actions(board)]

    if next_player(board) == X:

        return max(moves, key=lambda action: minval(result(board, action)))

    else:

        return min(moves, key=lambda action: maxval(result(board, action)))





def parse(board_str     )         :

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

    move = minimax(board)

    assert move is not None

    s = '\n'.join([str(move),

                   POSITIONS[move],

                   "Don't know how many moves to anything...\n"])

    print(s)

    f = open(outfile, 'w')

    f.write(s)

    f.close()





if __name__ == '__main__':

    main()