from engines import Engine
from copy import deepcopy

class OneplyEngine(Engine):
    """
    Game engine which implements a simple fitness function maximizing the
    difference in # of pieces in the given color's favor.
    """
    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """
        Returns a move for the given color which maximizes the difference in
        # of pieces for that color.
        """
        # Get a list of all the legal moves.
        moves = board.get_legal_moves(color)
        # Find the best move according to our simple utility function:
        # what move yields the largest different in # of pieces for us vs.
        # the opponent?
        
        # Return the "best" move.
        return max(moves, key=lambda move: self._get_cost(board, color, move))

    def _get_cost(self, board, color, move):
        """ 
        Returns the difference in # of pieces after the given move is executed.
        """
        # create a deepcopy of the board to preserve state of the actual board
        newboard = deepcopy(board)
        newboard.execute_move(move, color)

        # Count the # of pieces of each color on the board.
        num_pieces_op = len(newboard.get_squares(color*-1))
        num_pieces_me = len(newboard.get_squares(color))

        # Return the difference in pieces
        return num_pieces_me - num_pieces_op
        
engine = OneplyEngine
