"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x_count += 1
            elif board[i][j] == O:
                o_count += 1
    if x_count > o_count:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError('Not a valid action')
    else:
        tempBoard = copy.deepcopy(board)
        turn = player(tempBoard)
        tempBoard[action[0]][action[1]] = turn
    return tempBoard

def winner(board):
    """
    return who won
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == "X":
            return "X"
        elif board[i][0] == board[i][1] == board[i][2] == "O":
            return "O"
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == "X":
            return "X"
        elif board[0][j] == board[1][j] == board[2][j] == "O":
            return "O"
    if board[0][2] == board[1][1] == board[2][0] == "X":
        return "X"
    elif board[0][2] == board[1][1] == board[2][0] == "O":
        return "O"
    elif board[0][0] == board[1][1] == board[2][2] == "X":
        return "X"
    elif board[0][0] == board[1][1] == board[2][2] == "O":
        return "O"


    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    return EMPTY not in board[0] and EMPTY not in board[1] and EMPTY not in board[2]       #will return True if there are no empty cells remaining and False otherwise




def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        return Max_Value(board)[1]
    else:
        return Min_Value(board)[1]


def Max_Value(board):
    """
    Returns the optimal action for the max player on the board,
    along with its utility, and number of empty cells as a proxy
    to how fast the given actions led to the reported utility.
    Follows the format (utility, action, numEmpty).
    """
    if terminal(board):
        return  (utility(board), (), numEmpty(board))
    v = (float('-inf'), (), float('-inf'))                  # v(utility, action, numEmpty)
    for action in actions(board):
        newV = Min_Value(result(board, action))
        if max(v[0], newV[0]) != v[0]:                      # If the utility of the new action is better,
            v = (newV[0], action, newV[2])
        elif v[0] == newV[0] and newV[2] > v[2]:            # If the new action leads to an equally optimal utility in fewer moves,
            v = (v[0], action, newV[2])
        if v[0] == 1 and numEmpty(board) == (v[2] + 1):     # If the optimal utility has been found with the fewest moves possible, prune the remaining branches
            return v
    return v


def Min_Value(board):
    """
    Returns the optimal action for the min player on the board,
    along with its utility, and number of empty cells as a proxy
    to how fast the given actions led to the reported utility.
    Follows the format (utility, action, numEmpty).
    """
    if terminal(board):
        return (utility(board), (), numEmpty(board))
    v = (float('inf'), (), float('-inf'))                   # v(utility, action, numEmpty)
    for action in actions(board):
        newV = Max_Value(result(board, action))
        if min(v[0], newV[0]) != v[0]:                      # If the utility of the a new action is better,
            v = (newV[0], action, newV[2])
        elif v[0] == newV[0] and newV[2] > v[2]:            # If the new action leads to an equally optimal outcome in fewer moves,
            v = (v[0], action, newV[2])
        if v[0] == -1 and numEmpty(board) == (v[2] + 1):    # If the optimal utility has been found with the fewest moves possible, prune the remaining branches
            return v
    return v


def numEmpty(board):
    """
    Returns the number of EMPTY cells in a given board.
    Used as an heuristic to pick the shortest path to the desired utility.
    """
    numEmpty = 0
    for u in range(len(board)):
        for y in range(len(board[u])):
            if board[u][y] == EMPTY:
                numEmpty += 1
    return numEmpty
