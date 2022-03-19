# Author: Stew Towle
# Date: November 2021
# Description: Basic functionality for simple Janggi Ai
import JanggiGame
from heapq import heappop, heappush

COLOR_SWITCH = {'blue':'red', 'red':'blue'}

def ai_move_simple(board: JanggiGame, color: str):
    """
    Given a janggi board object and a string for the color of the player ('blue' or 'red')
    Returns a list of move tuples (two move strings, src then dest) sorted by priority
    with no particular order within the priority levels.  It prioritizes moves in this order:
    tier 1: get out of check
    tier 2: Put opponent into checkmate
    tier 3: put opponent in check, capture a piece
    (NOT IMPLEMENTED) tier 4: move a piece toward opponents side
    tier 5: any available move
    NOTE: will not include moves that put self in check
    returns NONE if the given color is not the player whose turn it is.
    Returns an empty list in the unique position that there is no valid moves
    """
    if color != board.get_whose_turn():
        return None

    game_board = board.get_board()
    move_list = list()
    for i in range(len(game_board)):
        for j in range(len(game_board[0])):
            #i will be current row, j current col
            if game_board[i][j] and game_board[i][j].get_color() == color:
                possible_moves = board.list_moves((i,j))
                piece_pos = board.convert_loc_to_str(i,j)
                for move in possible_moves:
                    prioritize_move(board, piece_pos, move, move_list, color)
    return move_list


def prioritize_move(board, piece_pos, move, move_list, color):
    """Given the JanggiBoard, the source piece, potential move and the priority queue of moves
    applies the heuristic and pushes the move to the queue if it is valid
    HELPER FOR ai_move_simple"""
    in_check = board.is_in_check(color)
    # For each potential move, try it with try move
    board.try_move(piece_pos, move)

    # if we are in check and it results in getting out of check push with priority 0
    if in_check:
        if not board.is_in_check(color):
            heappush(move_list, (0, (piece_pos, move)))
        return

    # if it makes result desired color wins push move with 1 priority
    # if results in opponent being in check push with priority 2
    if board.is_in_check(COLOR_SWITCH[color]):
        if board.is_in_checkmate(COLOR_SWITCH[color]):
            heappush(move_list, (1, (piece_pos, move)))
            return
        heappush(move_list, (2, piece_pos, move))
        return
    # restore board
    board.restore_board()

    target_piece = board.get_piece(move)
    # after the try-move possibilites check if move captures an opponents piece (priority 3)
    if target_piece and target_piece.get_color() == COLOR_SWITCH[color]:
        heappush(move_list, (3, piece_pos, move))
    if not target_piece:
        heappush(move_list, (5, piece_pos, move))